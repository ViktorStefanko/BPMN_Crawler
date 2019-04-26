from scripts.gh_api_crawler.db_handler import DbHandler
from scripts.gh_api_crawler.rep_crawler import RepositoryCrawler
from scripts.gh_api_crawler.tree_crawler import TreeCrawler
from scripts.gh_api_crawler.other_functions import UsefulFunctions
import sys


class BPMNCrawler:

    def __init__(self, progr_numb, client_id, client_secret):
        # Paths to DB that contains (user_id, username, name of repository and status)
        self.db_source_path = "data_GH_projects/databases/log_repos" + str(progr_numb) + ".db"
        # Paths to DB, where will be stored results
        self.db_result_path = "data_GH_projects/databases/result_bpmn" + str(progr_numb) + ".db"
        # Directory where all temporary files will be stored
        self.temp_dir = UsefulFunctions.make_dir("temp" + str(progr_numb))
        # Two DB tables for input and output
        self.log_rep_table = "log_repos" + str(progr_numb)
        self.res_bpmn_table = "result_bpmn" + str(progr_numb)
        # GH-key for max number of accesses: 5000/hour
        self.GH_KEY = str(client_id) + "&" + str(client_secret)
        # Instances of required classes
        self.db_handler = DbHandler()
        self.rep_crawler = RepositoryCrawler(self.GH_KEY)
        self.tree_crawler = TreeCrawler(self.res_bpmn_table)

    def run_bpmn_crawler(self, step=50):
        print("Connection to DB")
        db_conn_source = self.db_handler.create_connection(self.db_source_path)
        db_conn_result = self.db_handler.create_connection(self.db_result_path)
        min_id_query = "SELECT min(new_id) FROM " + self.log_rep_table + " WHERE status=1;"
        max_id_query = "SELECT max(new_id) FROM " + self.log_rep_table + " WHERE status=1;"
        min_id = self.db_handler.execute_query(db_conn_source, min_id_query, True)[0][0]
        max_id = self.db_handler.execute_query(db_conn_source, max_id_query, True)[0][0]

        print("Search between min_id: " + str(min_id) + " and max_id: " + str(max_id))
        if min_id != max_id:
            for begin in range(min_id, max_id, step):
                start = str(begin)
                end = str(min(begin + step - 1, max_id))
                query = "SELECT login, name FROM " + self.log_rep_table + " WHERE new_id BETWEEN " + start + " AND " +\
                        end + ";"
                # repo_list is a list of (username, repository_name) tuples
                repo_list = self.db_handler.execute_query(db_conn_source, query, True)

                if repo_list:
                    master_dir = UsefulFunctions.make_dir(self.temp_dir + "/master" + str(sys.argv[1]))
                    default_dir = UsefulFunctions.make_dir(self.temp_dir + "/default" + str(sys.argv[1]))
                    trees_dir = UsefulFunctions.make_dir(self.temp_dir + "/trees" + str(sys.argv[1]))

                    print("Get json files from GH API")
                    # Get json files with repositories information and store them into temp subdirectories
                    self.rep_crawler.traverse_gh_repositories(repo_list, master_dir, default_dir, trees_dir,
                                                              self.GH_KEY)

                    print("Search for BPMN files")
                    trees_repo_list = self.tree_crawler.get_repo_list(trees_dir)
                    if not self.tree_crawler.search_files(db_conn_result, trees_repo_list, trees_dir, default_dir):
                        print("Exception in tree_crawler!")
                        break
                    # Remove temp subdirectories
                    UsefulFunctions.remove_dir(master_dir)
                    UsefulFunctions.remove_dir(default_dir)
                    UsefulFunctions.remove_dir(trees_dir)

                    # Change status of searched repositories from 0 to 1
                    update_query = "UPDATE " + self.log_rep_table + " SET status = 1 WHERE new_id BETWEEN " + start + \
                                   " AND " + end + ";"
                    if self.db_handler.execute_query(db_conn_source, update_query, False):
                        print("Has updated between " + str(start) + " and " + str(end))
                    else:
                        break


"""
This script runs the program, that does GitHub-Repository-Mining concerning BPMN-diagrams 
It requires 3 parameter
:param argv[1]: the number of program/DB (E.g.: 1, 2, ..)
:param argv[2]: client_id of application to use the GitHub API
                (authentication increases limit from 60 up to 5000 hits per hour)
:param argv[3]: client_secret of application to use the GitHub API
Results will be stored in database
"""
if len(sys.argv) == 4:
    BPMNCrawler = BPMNCrawler(sys.argv[1], sys.argv[2], sys.argv[3])
    BPMNCrawler.run_bpmn_crawler()
else:
    print("Usage: arg1 - number of db; arg2 - GH_client_id; arg3 - GH_client_password")
