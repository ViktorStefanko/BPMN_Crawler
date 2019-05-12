from scripts.gh_api_crawler.db_handler import DbHandler
from scripts.statistics.functions_for_code_maat import CodeMaatFunctions
import subprocess
import os
import csv


class FileStatistics:
    def __init__(self, db_path="databases/ghbpmn.db",
                 table_result_files="result_files",
                 table_result_bpmn="result_bpmn",
                 projects_dir="data_GH_projects/projects_only_git",
                 code_maat_path="C:/Users/viktor/Documents/education/bachelorarbeit/code-maat/target/code-maat-"
                                "1.1-SNAPSHOT-standalone.jar",
                 statistics_file_utf16_csv="files_stat_utf16.csv",
                 age_file_utf16_csv="age_files_utf16.csv",
                 all_files_dir="data_GH_projects/all_files",
                 table_copy_result_files="copy_result_files"
                 ):

        self.db_path = db_path
        self.table_result_files = table_result_files
        self.table_result_bpmn = table_result_bpmn
        self.db_handler = DbHandler()
        self.db_conn = self.db_handler.create_connection(self.db_path)
        self.projects_dir = projects_dir
        self.code_maat_path = code_maat_path
        self.statistics_file_utf16_csv = statistics_file_utf16_csv
        self.age_file_utf16_csv = age_file_utf16_csv
        self.all_files_dir = all_files_dir
        self.table_copy_result_files = table_copy_result_files

    """
    It computes age in months, number of changes and author's number for each file 
    """
    def add_file_statistics(self):
        query1 = "SELECT DISTINCT login, name FROM " + self.table_result_files + ";"
        repo_list = self.db_handler.execute_query(self.db_conn, query1, True)

        for repo in repo_list:
            repo_path = os.path.join(os.path.join(self.projects_dir, repo[0]), repo[1])
            if os.path.exists(repo_path):
                query2 = "SELECT path_file FROM " + self.table_result_files + \
                         " WHERE login='" + repo[0] + \
                         "' AND name='" + repo[1] + "';"
                bpmn_file_list = self.db_handler.execute_query(self.db_conn, query2, True)
                log_file_path = os.path.join(repo_path, "logfile.log")
                if not os.path.exists(log_file_path):
                    CodeMaatFunctions.create_log_file(repo_path, log_file_path)
                else:
                    statistics_utf16_csv_path = os.path.join(repo_path, self.statistics_file_utf16_csv)
                    age_utf16_csv_path = os.path.join(repo_path, self.age_file_utf16_csv)
                    if not os.path.exists(statistics_utf16_csv_path) or not os.path.exists(age_utf16_csv_path):
                        CodeMaatFunctions.collect_file_informations(self.code_maat_path, log_file_path,
                                                                statistics_utf16_csv_path, age_utf16_csv_path)
                    else:
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
                                        query3 = "UPDATE " + self.table_result_files + " SET n_authors='" + line_list[
                                            1] + \
                                                 "', n_revs='" + line_list[2] + \
                                                 "' WHERE path_file='" + bpmn_file[0] + "';"
                                        self.db_handler.execute_query(self.db_conn, query3, False)
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
                                        query4 = "UPDATE " + self.table_result_files + " SET age_months='" + line_list[
                                            1] + "' WHERE path_file='" + bpmn_file[0] + "';"
                                        self.db_handler.execute_query(self.db_conn, query4, False)
                                        break
            else:
                print("Error path doesn't exist: " + repo_path)

    def find_bpmn_diagram_from_xml(self):
        bpmn_schema = 'http://www.omg.org/spec/BPMN/20100524/MODEL'
        query = "SELECT login, name, path_file FROM " + self.table_result_files + \
                " WHERE path_file LIKE '%.bpmn'" + \
                " OR path_file LIKE '%.xml'" + \
                " OR path_file LIKE '%.bpmn2'" + \
                " OR path_file LIKE '%.bpmn20';"
        all_paths = self.db_handler.execute_query(self.db_conn, query, True)
        for (login, project_name, rel_file_path) in all_paths:
            file_path = os.path.join("data_GH_projects/projects_without_git", rel_file_path)
            if os.path.exists(file_path):
                if open(file_path, encoding="utf8", errors='ignore').read().find(bpmn_schema) != -1:
                    query = "INSERT INTO " + self.table_result_bpmn + "(path_file) VALUES ('" + rel_file_path + "');"
                    self.db_handler.execute_query(self.db_conn, query, False)
            else:
                print("Error, path doesn't exist: " + file_path)

    def find_duplicates(self):
        dupf_result = "data_GH_projects/dupf_result.txt"

        os.environ["COMSPEC"] = 'powershell'
        cmd = "dupf '" + self.all_files_dir + "' > " + dupf_result
        print(cmd)
        pipe = subprocess.Popen(cmd, shell=True)
        pipe.wait()
        reader = open(dupf_result, "r", encoding='utf16')
        i = 0
        for line in reader.readlines():
            if line == "\n":
                continue
            elif line.find("- Equal") != -1:
                i = i + 1
            else:
                dup_file = line.split("\\")[-1].split("\"")[0]
                query2 = "UPDATE " + self.table_result_files + " SET duplicate=" + str(i) + \
                         " WHERE path_file=(SELECT path_file from " + self.table_copy_result_files + \
                         " WHERE path_copy_file='" + dup_file + "');"
                self.db_handler.execute_query(self.db_conn, query2, False)
