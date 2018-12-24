from src.db_handler import DbHandler
from src.rep_crawler import RepCrawler
from src.tree_crawler import TreeCrawler
import src.other_functions as my_functions
import sys

if len(sys.argv) == 4:
    # Paths to the databases
    db_source_path = "databases/log_repos" + str(sys.argv[1]) + ".db"
    db_result_path = "databases/result_bpmn" + str(sys.argv[1]) + ".db"

    # Two DB tables for input and output
    log_rep_table = "log_repos" + str(sys.argv[1])
    res_bpmn_table = "result_bpmn" + str(sys.argv[1])

    # GH-key for max limit 5000/hour
    GH_KEY = str(sys.argv[2]) + "&" + str(sys.argv[3])
    print(GH_KEY)

    # Instances of required classes
    db_handler = DbHandler()
    rep_crawler = RepCrawler(GH_KEY)
    tree_crawler = TreeCrawler(res_bpmn_table)

    print("Connection to DB: \n")
    db_conn_source = db_handler.create_connection(db_source_path)
    min_id_query = "SELECT min(new_id) FROM " + log_rep_table + " WHERE status=0;"
    max_id_query = "SELECT max(new_id) FROM " + log_rep_table + " WHERE status=0;"
    min_id = db_handler.execute_query(db_conn_source, min_id_query, True)[0][0]
    max_id = db_handler.execute_query(db_conn_source, max_id_query, True)[0][0]

    print("min_id: " + str(min_id))
    print("max_id: " + str(max_id))
    if min_id != max_id:
        step = 2400
        for size in range(min_id, max_id, step):
            start = str(size)
            end = str(min(size + step, max_id))
            print("\nSelect between: " + start + " AND " + end)
            query = "SELECT login, name FROM " + log_rep_table + " WHERE new_id BETWEEN " + start + " AND " + end + ";"
            # repo_list is a list of (username, repository_name) tuples
            repo_list = db_handler.execute_query(db_conn_source, query, True)
            if repo_list:
                print("Make tree: \n")
                temp_dir = my_functions.make_dir("temp" + str(sys.argv[1]))
                master_dir = my_functions.make_dir(temp_dir + "/master" + str(sys.argv[1]))
                default_dir = my_functions.make_dir(temp_dir + "/default" + str(sys.argv[1]))
                trees_dir = my_functions.make_dir(temp_dir + "/trees" + str(sys.argv[1]))
                rep_crawler.traverse_gh_repositories(repo_list, master_dir, default_dir, trees_dir, GH_KEY)

                print("Search in trees for bpmn files: \n")
                trees_repo_list = tree_crawler.get_repo_list(trees_dir)
                db_conn_result = db_handler.create_connection(db_result_path)
                tree_crawler.search_files(db_conn_result, trees_repo_list, trees_dir, default_dir)

                # Remove temp subdirectories
                my_functions.remove_dir(master_dir)
                my_functions.remove_dir(default_dir)
                my_functions.remove_dir(trees_dir)

                update_query = "UPDATE " + log_rep_table + " SET status = 1 WHERE new_id BETWEEN " + start + " AND " + end + ";"
                db_handler.execute_query(db_conn_source, update_query, False)
                print("Has updated between " + str(start) + " and " + str(end))
else:
    print("Usage: param1 - number of db; param2 - id; param3 - password")
