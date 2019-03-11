from src.db_handler import DbHandler
from functions_for_code_maat import *
import os
import csv

db_path = "data_GH_projects/databases/result.db"
table = "result"
db_handler = DbHandler()
db_conn_source = db_handler.create_connection(db_path)

query1 = "SELECT DISTINCT login, project_name FROM " + table + " WHERE n_authors IS NULL " + \
         " AND login NOT LIKE 'hboutemy' AND login NOT LIKE 'JanuaryA2';"
repo_list = db_handler.execute_query(db_conn_source, query1, True)
projects_dir = "projects_only_git"
code_maat_path = "C:\\Users\\viktor\\Documents\education\\bachelorarbeit\\code-maat\\target\\code-maat-1.1-SNAPSHOT-standalone.jar"
statistics_file_utf16_csv = "files_stat_utf16.csv"
age_file_utf16_csv = "age_files_utf16.csv"

for repo in repo_list:
    repo_path = os.path.join(os.path.join(projects_dir, repo[0]), repo[1])
    if os.path.exists(repo_path):
        query2 = "SELECT path_bpmn_file FROM " + table + \
                 " WHERE login='" + repo[0] + \
                 "' AND project_name='" + repo[1] + "';"
        bpmn_file_list = db_handler.execute_query(db_conn_source, query2, True)

        log_file_path = os.path.join(repo_path, "logfile.log")
        statistics_utf16_csv_path = os.path.join(repo_path, statistics_file_utf16_csv)
        age_utf16_csv_path = os.path.join(repo_path, age_file_utf16_csv)
        make_files_statistics(code_maat_path, log_file_path, statistics_utf16_csv_path,
                              age_utf16_csv_path)

        data = open(statistics_utf16_csv_path, encoding="utf16")
        reader = csv.reader(data)
        for line_list in reader:
            if line_list[0].lower().find("bpmn") != -1:
                if line_list[0].find("{") == -1 and line_list[0].find("=>") == -1:
                    git_file_path = repo[0] + "/" + repo[1] + "/" + line_list[0]
                elif line_list[0].find("{") != -1:
                    first_split = line_list[0].split("{")
                    second_split = first_split[1].split("}")
                    middle_split = second_split[0].split("=> ")
                    if not middle_split[1]:
                        str_line = first_split[0] + second_split[1].split("/", 1)[1]
                    else:
                        str_line = first_split[0] + middle_split[1] + second_split[1]
                    git_file_path = repo[0] + "/" + repo[1] + "/" + str_line
                else:
                    middle_split = line_list[0].split("=> ")
                    git_file_path = repo[0] + "/" + repo[1] + "/" + middle_split[1]

                for bpmn_file in bpmn_file_list:
                    if git_file_path == bpmn_file[0]:
                        query3 = "UPDATE " + table + " SET n_authors='" + line_list[1] + \
                                 "', n_revs='" + line_list[2] + \
                                 "' WHERE path_bpmn_file='" + bpmn_file[0] + "';"
                        db_handler.execute_query(db_conn_source, query3, False)
                        break

        data = open(age_utf16_csv_path, encoding="utf16")
        reader = csv.reader(data)
        for line_list in reader:
            if line_list[0].lower().find("bpmn") != -1:
                if line_list[0].find("{") == -1 and line_list[0].find("=>") == -1:
                    git_file_path = repo[0] + "/" + repo[1] + "/" + line_list[0]
                elif line_list[0].find("{") != -1:
                    first_split = line_list[0].split("{")
                    second_split = first_split[1].split("}")
                    middle_split = second_split[0].split("=> ")
                    if not middle_split[1]:
                        str_line = first_split[0] + second_split[1].split("/", 1)[1]
                    else:
                        str_line = first_split[0] + middle_split[1] + second_split[1]
                    git_file_path = repo[0] + "/" + repo[1] + "/" + str_line
                else:
                    middle_split = line_list[0].split("=> ")
                    git_file_path = repo[0] + "/" + repo[1] + "/" + middle_split[1]
                for bpmn_file in bpmn_file_list:
                    if git_file_path == bpmn_file[0]:
                        query4 = "UPDATE " + table + " SET age_months='" + line_list[1] + \
                                 "' WHERE path_bpmn_file='" + bpmn_file[0] + "';"
                        db_handler.execute_query(db_conn_source, query4, False)
                        break
    else:
        print("Error path doesn't exist: " + repo_path)
