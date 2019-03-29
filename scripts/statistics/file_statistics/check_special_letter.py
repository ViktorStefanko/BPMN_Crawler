from src_bpmn_crawler.db_handler import DbHandler
import subprocess
import os

repo_path = "data_GH_projects/projects_without_git"
db_path = "data_GH_projects/databases/result.db"
table_res_bpmn = "result_bpmn"
db_handler = DbHandler()
db_conn = db_handler.create_connection(db_path)

query = "SELECT path_bpmn_file FROM " + table_res_bpmn + ";"
bpmn_paths_list = db_handler.execute_query(db_conn, query, True)


def check_special_letter():
    # For each repository analyse all bpmn-files
    for bpmn_file_path in bpmn_paths_list:
        bpmn_schema = 'http://www.omg.org/spec/BPMN/20100524/MODEL'
        file_path = os.path.join("data_GH_projects\projects_without_git", bpmn_file_path[0])
        if os.path.exists(file_path):
            print(file_path)
            if open(file_path, encoding="utf8").read().find(bpmn_schema) != -1:
                print(bpmn_file_path[0])
            else:
                print("Error: " + bpmn_file_path[0])
        else:
            print("Error, path doesn't exist: " + file_path)
