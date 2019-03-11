from src.db_handler import DbHandler
from functions_for_code_maat import *
import os

db_path = "data_GH_projects/databases/result.db"
table = "projects"
db_handler = DbHandler()
db_conn_source = db_handler.create_connection(db_path)

query1 = "SELECT DISTINCT login, project_name FROM " + table + ";"
repo_list = db_handler.execute_query(db_conn_source, query1, True)
projects_dir = "data_GH_projects/projects_only_git"

for repo in repo_list:
    print(repo)
    repo_path = os.path.join(os.path.join(projects_dir, repo[0]), repo[1])
    if os.path.exists(repo_path):
       log_file_path = os.path.join(repo_path, "logfile.log")
       create_log_file(repo_path, log_file_path)
    else:
        print("Error path doesn't exist: " + repo_path)
