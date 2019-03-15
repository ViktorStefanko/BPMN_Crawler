from src.db_handler import DbHandler

db_path = "data_GH_projects/databases/result.db"
store_table = "files_copy"
db_handler = DbHandler()
db_conn_source = db_handler.create_connection(db_path)
query1 = "SELECT path_copy_bpmn_file FROM " + store_table + ";"
paths_copy_files = db_handler.execute_query(db_conn_source, query1, True)

dupf_result = "scripts\statistics\duplicate_statistics\dupf_result.txt"

reader = open(dupf_result, "r", encoding='utf16')
i = 0
for line in reader.readlines():
    if line == "\n":
        continue
    elif line.find("- Equal") != -1:
        i = i + 1
    else:
        dup_file = line.split("\\")[2].split("\"")[0]
        query2 = "UPDATE " + store_table + " SET duplicate=" + str(i) + \
                 " WHERE path_copy_bpmn_file='" + dup_file + "';"
        db_handler.execute_query(db_conn_source, query2, False)
