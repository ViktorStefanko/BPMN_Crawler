from src_bpmn_crawler.db_handler import DbHandler
import subprocess
import os


db_path = "data_GH_projects/databases/result.db"
db_handler = DbHandler()
db_conn_source = db_handler.create_connection(db_path)
bpmn_paths_table = "result_bpmn"
result_table = "result"
dup_table = "files_copy"


def copy_most_duplicated_bpmn():
    my_dir = "data_GH_projects/projects_without_git"
    store_dir = "data_GH_projects\\the_most_popular_bpmn"
    query = "SELECT * FROM (SELECT duplicate, count(*) AS dup FROM result_bpmn, files_copy" \
            " WHERE result_bpmn.path_bpmn_file=files_copy.path_bpmn_file AND" \
            " duplicate IS NOT NULL GROUP BY duplicate) WHERE dup > 20;"
    duplicated_list = db_handler.execute_query(db_conn_source, query, True)

    for dup in duplicated_list:
        query = "SELECT path_bpmn_file FROM files_copy WHERE duplicate=" + str(dup[0]) + ";"
        paths_list = db_handler.execute_query(db_conn_source, query, True)
        file_path = paths_list[0][0]

        if os.path.isdir(my_dir):
            cmd = "cp " + my_dir + "/" + file_path + " " + store_dir + "/"\
                  + str(dup[1]) + "_copy_" + file_path.split("/")[-1].split(".")[0] + ".bpmn"
            print(cmd)
            pipe = subprocess.Popen(cmd, shell=True)
            pipe.wait()
