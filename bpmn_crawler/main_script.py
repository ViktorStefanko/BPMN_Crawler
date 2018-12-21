from src.db_handler import DbHandler
from src.rep_crawler import RepCrawler
from src.tree_crawler import TreeCrawler
import src.other_functions as my_functions
import sys

if len(sys.argv) == 3:
    GH_KEY = str(sys.argv[1]) + "&" + str(sys.argv[2])
    print(GH_KEY)
    # Path to the database
    db_dir = "database"
    db_name = "sqliteBPMN.db"
    db_path = db_dir + "/" + db_name

    # Two DB tables for input and output
    log_rep_table = "log_repos"
    projects_bpmn = "projects_bpmn"

    # Instances of required classes
    db_handler = DbHandler()
    rep_crawler = RepCrawler(GH_KEY)
    tree_crawler = TreeCrawler(projects_bpmn)

    print("Connection to DB: \n")
    db_conn = db_handler.create_connection(db_path)
    min_id_query = "SELECT min(id) FROM " + log_rep_table + ";"
    max_id_query = "SELECT max(id) FROM " + log_rep_table + ";"
    min_id = db_handler.execute_query(db_conn, min_id_query, True)[0][0]
    max_id = db_handler.execute_query(db_conn, max_id_query, True)[0][0]
    print("min_id: " + str(min_id))
    print("max_id: " + str(max_id))
    if min_id != max_id:
        step = 2400
        for size in range(min_id, max_id, step):
            start = str(size)
            end = str(min(size + step, max_id))
            print("\nSelect between: " + start + " AND " + end)
            query = "SELECT login, name FROM " + log_rep_table + " WHERE id BETWEEN " + start + " AND " + end + ";"
            # repo_list is a list of (username, repository_name) tuples
            repo_list = db_handler.execute_query(db_conn, query, True)
            if repo_list:
                print("Make tree: \n")
                temp_dir = my_functions.make_dir("temp")
                master_dir = my_functions.make_dir(temp_dir + "/master")
                default_dir = my_functions.make_dir(temp_dir + "/default")
                trees_dir = my_functions.make_dir(temp_dir + "/trees")
                rep_crawler.traverse_gh_repositories(repo_list, master_dir, default_dir, trees_dir, GH_KEY)

                print("Search in trees for bpmn files: \n")
                trees_repo_list = tree_crawler.get_repo_list(trees_dir)
                db_conn = db_handler.create_connection(db_path)
                tree_crawler.search_files(db_conn, trees_repo_list, trees_dir, default_dir)

                # Remove temp directories
                my_functions.remove_dir(master_dir)
                my_functions.remove_dir(default_dir)
                my_functions.remove_dir(trees_dir)
