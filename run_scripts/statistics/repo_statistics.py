from src.db_handler import DbHandler
from functions_for_code_maat import *
import os

db_path = "data_GH_projects/databases/result.db"
table = "projects"
db_handler = DbHandler()
db_conn_source = db_handler.create_connection(db_path)

query = "SELECT login, project_name FROM " + table + ";"
repo_list = db_handler.execute_query(db_conn_source, query, True)
projects_dir = "projects_only_git"
code_maat_path = "C:\\Users\\viktor\\Documents\education\\bachelorarbeit\\code-maat\\target\\code-maat-1.1-SNAPSHOT-standalone.jar"

for repo in repo_list:
    repo_path = os.path.join(os.path.join(projects_dir, repo[0]), repo[1])
    if os.path.exists(repo_path):
        log_file_path = os.path.join(repo_path, "logfile.log")

        name_csv_file = "repo_stat.csv"
        csv_path = os.path.join(repo_path, name_csv_file)
        make_repo_statistics(code_maat_path, log_file_path, csv_path)

        csv_reader = open(csv_path, encoding="utf8")
        lines = csv_reader.readlines()
        csv_reader.close()
        if len(lines) > 2:
            query = "UPDATE " + table + " SET created_at='" + lines[1].split(",", 1)[0] + \
                    "', last_commit_at='" + lines[-1].split(",", 1)[0] + \
                    "' WHERE login='" + repo[0] + "' AND project_name='" + repo[1] + "';"
            db_handler.execute_query(db_conn_source, query, False)
        elif len(lines) == 2:
            query = "UPDATE " + table + " SET created_at='" + lines[1].split(",", 1)[0] + \
                    "', last_commit_at='" + lines[1].split(",", 1)[0] + \
                    "' WHERE login='" + repo[0] + "' AND project_name='" + repo[1] + "';"
            db_handler.execute_query(db_conn_source, query, False)
    else:
        print("Error path doesn't exist: " + repo_path)
