from src.db_handler import DbHandler
import os.path

db_path = "data_GH_projects/databases/result.db"
table_repos = "projects"
table_res = "result"
db_handler = DbHandler()
db_conn = db_handler.create_connection(db_path)
query = "SELECT login, project_name FROM " + table_repos + ";"
repos = db_handler.execute_query(db_conn, query, True)
store_dir = "data_GH_projects/projects_without_git"

for repo in repos:
    query = "SELECT link_bpmn_file FROM " + table_res + \
            " WHERE login='" + repo[0] +\
            "' AND project_name='" + repo[1] + "';"
    links = db_handler.execute_query(db_conn, query, True)

    repo_path = ""
    for link in links:
        link_sp = link[0].split(repo[0] + "/" + repo[1] + "/master")
        if len(link_sp) == 1:
            link_1 = link[0].split("https://raw.githubusercontent.com/" + repo[0] + "/" + repo[1])
            link_sp = link_1[1].split("/", 2)
            repo_path = repo[0] + "/" + repo[1] + "/" + link_sp[2]
            full_path = store_dir + "/" + repo_path
        else:
            repo_path = repo[0] + "/" + repo[1] + link_sp[1]
            full_path = store_dir + "/" + repo_path

        if os.path.exists(full_path):
            query = "UPDATE " + table_res + " SET path_bpmn_file='" + \
                    repo_path + "' WHERE link_bpmn_file='" + link[0] + "';"
            db_handler.execute_query(db_conn, query, False)
        else:
            print("Path doesn't exist: " + full_path)

