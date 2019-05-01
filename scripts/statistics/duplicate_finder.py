from scripts.gh_api_crawler.db_handler import DbHandler
import os
import subprocess


class DuplicateFinder:

    def __init__(self, db_path="databases/ghbpmn.db",
                 table_res="result_files",
                 store_table="copy_result_files",
                 files_directory="data_GH_projects/projects_without_git",
                 target_dir="C:/Users/viktor/Documents/education/bachelorarbeit/BPMN_"
                            "Crawler/data_GH_projects/all_files"):

        self.db_path = db_path
        self.table_res = table_res
        self.store_table = store_table
        self.db_handler = DbHandler()
        self.db_conn = self.db_handler.create_connection(db_path)
        self.files_directory = files_directory
        self.target_dir = target_dir

    def copy_all_files(self):
        query1 = "SELECT path_file FROM " + self.table_res + ";"
        paths_to_files = self.db_handler.execute_query(self.db_conn, query1, True)
        os.environ["COMSPEC"] = 'powershell'

        for i in range(0, len(paths_to_files)):
            file_name = paths_to_files[i][0].split("/")[-1]
            file_path = os.path.join(self.files_directory, paths_to_files[i][0])

            if os.path.exists(file_path):
                new_file_name = str(i) + "_" + file_name
                new_file_path = os.path.join(self.target_dir, new_file_name)

                cmd = "cp '" + file_path + "' " + new_file_path
                print(cmd)

                pipe = subprocess.Popen(cmd, shell=True)
                pipe.wait()

                if os.path.exists(new_file_path):
                    query2 = "INSERT INTO " + self.store_table + "(path_file, path_copy_file) VALUES('" + \
                             paths_to_files[i][0] + "', '" + new_file_name + "');"
                    self.db_handler.execute_query(self.db_conn, query2, False)

            else:
                print("Error. Path doesn't exist: " + file_path)

    def find_duplicates(self):
        dupf_result = "dupf_result.txt"

        os.environ["COMSPEC"] = 'powershell'
        cmd = "dupf '" + self.target_dir + "' > " + dupf_result
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
                query2 = "UPDATE " + self.store_table + " SET duplicate=" + str(i) + \
                         " WHERE path_copy_file='" + dup_file + "';"
                self.db_handler.execute_query(self.db_conn, query2, False)
