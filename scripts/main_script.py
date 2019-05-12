from scripts.gh_api_crawler.db_handler import DbHandler
from scripts.gh_api_crawler.rep_crawler import RepositoryCrawler
from scripts.gh_api_crawler.tree_crawler import TreeCrawler
from scripts.gh_api_crawler.other_functions import UsefulFunctions
import sys


class GitHubApiCrawler:
    db_path = "databases/ghbpmn.db"
    # Two DB tables for input and output
    log_rep_table = "to_query_projects"
    res_table = "result_files"

    def __init__(self, progr_numb, client_id, client_secret):
        # GH-key for max number of accesses: 5000/hour
        self.GH_KEY = str(client_id) + "&" + str(client_secret)
        # Instances of required classes
        self.db_handler = DbHandler()
        self.rep_crawler = RepositoryCrawler(self.GH_KEY)
        self.tree_crawler = TreeCrawler(GitHubApiCrawler.res_table)
        self.temp_dir = UsefulFunctions.make_dir("temp" + str(progr_numb))

    def run_api_crawler(self, start_id, end_id, step=50):
        print("Connection to DB")
        db_conn = self.db_handler.create_connection(GitHubApiCrawler.db_path)
        min_id_query = "SELECT min(id) FROM " + GitHubApiCrawler.log_rep_table + " WHERE " \
                       "id BETWEEN " + str(start_id) + " AND " + str(end_id) + " AND status=0;"
        max_id_query = "SELECT max(id) FROM " + GitHubApiCrawler.log_rep_table + " WHERE " \
                       "id BETWEEN " + str(start_id) + " AND " + str(end_id) + " AND status=0;"
        min_id = self.db_handler.execute_query(db_conn, min_id_query, True)[0][0]
        max_id = self.db_handler.execute_query(db_conn, max_id_query, True)[0][0]

        print("Search between min_id: " + str(min_id) + " and max_id: " + str(max_id))
        if min_id and max_id:
            for begin in range(min_id, max_id + 1, step):
                start = str(begin)
                end = str(min(begin + step - 1, max_id))
                query = "SELECT login, name FROM " + GitHubApiCrawler.log_rep_table + " WHERE id BETWEEN " + start +\
                        " AND " + end + " AND status=0;"
                # repo_list is a list of (username, repository_name) tuples
                repo_list = self.db_handler.execute_query(db_conn, query, True)

                if repo_list:
                    master_dir = UsefulFunctions.make_dir(self.temp_dir + "/master")
                    default_dir = UsefulFunctions.make_dir(self.temp_dir + "/default")
                    trees_dir = UsefulFunctions.make_dir(self.temp_dir + "/trees")

                    print("Get json files from GH API")
                    # Get json files with repositories information and store them into temp subdirectories
                    self.rep_crawler.traverse_gh_repositories(repo_list, master_dir, default_dir, trees_dir,
                                                              self.GH_KEY)

                    print("Search for BPMN files")
                    trees_repo_list = self.tree_crawler.get_repo_list(trees_dir)
                    if not self.tree_crawler.search_files(db_conn, trees_repo_list, trees_dir, default_dir):
                        print("Exception in tree_crawler!")
                        break
                    # Remove temp subdirectories
                    UsefulFunctions.remove_dir(master_dir)
                    UsefulFunctions.remove_dir(default_dir)
                    UsefulFunctions.remove_dir(trees_dir)

                    # Change status of searched repositories from 0 to 1
                    update_query = "UPDATE " + GitHubApiCrawler.log_rep_table + " SET status = 1 WHERE id BETWEEN " \
                                   + start + " AND " + end + ";"
                    if self.db_handler.execute_query(db_conn, update_query, False):
                        print("Has updated between " + str(start) + " and " + str(end))
                    else:
                        break


"""
This script runs the program, that does GitHub-Repository-Mining concerning BPMN diagrams 
It requires 3 parameter
:param argv[1]: the number of program (E.g.: 1, 2, ..)
:param argv[2]: client_id of application to use the GitHub API
                (authentication increases limit from 60 up to 5000 hits per hour)
:param argv[3]: client_secret of application to use the GitHub API
:param argv[4]: min id of repository in database 
:param argv[5]: max id of repository in database 
Results will be stored in database
"""
if len(sys.argv) == 6:
    BPMNCrawler = GitHubApiCrawler(sys.argv[1], sys.argv[2], sys.argv[3])
    BPMNCrawler.run_api_crawler(sys.argv[4], sys.argv[5])
else:
    print("Usage: arg1 - number of program; arg2 - GH_client_id; arg3 - GH_client_password "
          "arg4 and arg5 are min and max id of repositories to investigate")
