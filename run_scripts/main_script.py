from src.db_handler import DbHandler
from src.rep_crawler import RepCrawler
from src.tree_crawler import TreeCrawler
import src.other_functions as my_functions
import sys
import time


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
    # Paths to DB that contains (user_id, username, name of repository and status)
    db_source_path = "data_GH_projects/databases/log_repos" + str(sys.argv[1]) + ".db"
    # Paths to DB, where will be stored results
    db_result_path = "data_GH_projects/databases/result_bpmn" + str(sys.argv[1]) + ".db"

    # Directory where all temporary files will be stored
    temp_dir = my_functions.make_dir("temp" + str(sys.argv[1]))

    # Two DB tables for input and output
    log_rep_table = "log_repos" + str(sys.argv[1])
    res_bpmn_table = "result_bpmn" + str(sys.argv[1])

    # GH-key for max number of accesses: 5000/hour
    GH_KEY = str(sys.argv[2]) + "&" + str(sys.argv[3])

    # Instances of required classes
    db_handler = DbHandler()
    rep_crawler = RepCrawler(GH_KEY)
    tree_crawler = TreeCrawler(res_bpmn_table)

    print("Connection to DB")
    db_conn_source = db_handler.create_connection(db_source_path)
    db_conn_result = db_handler.create_connection(db_result_path)
    min_id_query = "SELECT min(new_id) FROM " + log_rep_table + " WHERE status=0;"
    max_id_query = "SELECT max(new_id) FROM " + log_rep_table + " WHERE status=0;"
    min_id = db_handler.execute_query(db_conn_source, min_id_query, True)[0][0]
    max_id = db_handler.execute_query(db_conn_source, max_id_query, True)[0][0]

    print("Search between min_id: " + str(min_id) + " and max_id: " + str(max_id))
    if min_id != max_id:
        step = 50
        for begin in range(min_id, max_id, step):
            t1 = time.time()
            start = str(begin)
            end = str(min(begin + step - 1, max_id))
            query = "SELECT login, name FROM " + log_rep_table + " WHERE new_id BETWEEN " + start + " AND " + end + ";"
            # repo_list is a list of (username, repository_name) tuples
            repo_list = db_handler.execute_query(db_conn_source, query, True)

            if repo_list:
                master_dir = my_functions.make_dir(temp_dir + "/master" + str(sys.argv[1]))
                default_dir = my_functions.make_dir(temp_dir + "/default" + str(sys.argv[1]))
                trees_dir = my_functions.make_dir(temp_dir + "/trees" + str(sys.argv[1]))

                print("Get json files from GH API")
                # Get json files with repositories information and store them into temp subdirectories
                rep_crawler.traverse_gh_repositories(repo_list, master_dir, default_dir, trees_dir, GH_KEY)

                print("Search for BPMN files")
                trees_repo_list = tree_crawler.get_repo_list(trees_dir)
                if not tree_crawler.search_files(db_conn_result, trees_repo_list, trees_dir, default_dir):
                    print("Exception in tree_crawler!")
                    break
                # Remove temp subdirectories
                my_functions.remove_dir(master_dir)
                my_functions.remove_dir(default_dir)
                my_functions.remove_dir(trees_dir)

                # Change status of searched repositories from 0 to 1
                update_query = "UPDATE " + log_rep_table + " SET status = 1 WHERE new_id BETWEEN " + start + " AND " + end + ";"
                if db_handler.execute_query(db_conn_source, update_query, False):
                    print("Has updated between " + str(start) + " and " + str(end))
                else:
                    break
                took_sec = time.time() - t1
                print("It took " + str(took_sec) + " sec to investigate " + str(step) + " repositories\n")
else:
    print("Usage: arg1 - number of db; arg2 - GH_client_id; arg3 - GH_client_password")


