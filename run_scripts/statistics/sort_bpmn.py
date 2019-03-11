from src.db_handler import DbHandler
import os.path

db_path = "data_GH_projects/databases/result.db"
table_res = "result"
table_bpmn = "result_bpmn"
db_handler = DbHandler()
db_conn = db_handler.create_connection(db_path)
query = "SELECT login, project_name, path_bpmn_file FROM " + table_res + \
        " WHERE path_bpmn_file LIKE '%.bpmn'" + \
        " OR path_bpmn_file LIKE '%.xml'" + \
        " OR path_bpmn_file LIKE '%.bpmn2'" + \
        " OR path_bpmn_file LIKE '%.bpmn2d'" + \
        " OR path_bpmn_file LIKE '%.bpmn20';"

all_paths = db_handler.execute_query(db_conn, query, True)

bpmn_schema = 'http://www.omg.org/spec/BPMN/20100524/MODEL'
for (login, project_name, rel_file_path) in all_paths:
    file_path = os.path.join("projects_without_git", rel_file_path)
    if os.path.exists(file_path):
        if open(file_path, encoding="utf8", errors='ignore').read().find(bpmn_schema) != -1:
            query = "INSERT INTO " + table_bpmn + \
                    " VALUES ('" + login + "', '" + project_name + "', '" + \
                    rel_file_path + "');"
            db_handler.execute_query(db_conn, query, False)
    else:
        print("Error, path doesn't exist: " + file_path)
