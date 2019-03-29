from src_bpmn_crawler.db_handler import DbHandler
import os
import subprocess

db_path = "data_GH_projects/databases/result.db"
table_res = "result"
store_table = "files_copy"
db_handler = DbHandler()
db_conn_source = db_handler.create_connection(db_path)

query1 = "SELECT path_bpmn_file FROM " + table_res + ";"
paths_to_files = db_handler.execute_query(db_conn_source, query1, True)

files_directory = "data_GH_projects\projects_without_git"
target_dir = "all_files"
os.environ["COMSPEC"] = 'powershell'

for i in range(0, len(paths_to_files)):
    file_name = paths_to_files[i][0].split("/")[-1]
    file_path = os.path.join(files_directory, paths_to_files[i][0])

    if os.path.exists(file_path):
        new_file_name = str(i) + "_" + file_name
        new_file_path = os.path.join(target_dir, new_file_name)

        cmd = "cp '" + file_path + "' " + new_file_path
        pipe = subprocess.Popen(cmd, shell=True)
        pipe.wait()

        if os.path.exists(new_file_path):
            query2 = "INSERT INTO " + store_table + " VALUES('" + paths_to_files[i][0] + \
                 "', '" + new_file_name + "');"
            db_handler.execute_query(db_conn_source, query2, False)
    else:
        print("Error. Path doesn't exist: " + file_path)
