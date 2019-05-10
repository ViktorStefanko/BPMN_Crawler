import os
import subprocess
import requests
import time


class UsefulFunctions:

    @staticmethod
    def make_dir(my_dir):
        """ Make directory if it doesn't exist """
        if not os.path.isdir(my_dir):
            os.mkdir(my_dir)
        return my_dir

    @staticmethod
    def remove_dir(my_dir):
        """ Remove directory if it exists """
        if os.path.isdir(my_dir):
            cmd = "rm -rf " + my_dir
            pipe = subprocess.Popen(cmd, shell=True)
            pipe.wait()

    @staticmethod
    def get_limit(gh_key):
        url_limit = 'https://api.github.com/rate_limit?' + gh_key
        try:
            data = requests.get(url_limit).json()
            rate = data["rate"]
            return [int(rate["remaining"]), int(rate["reset"])]
        except:
            print("Exception in get_limit()")
            time.sleep(120)
            UsefulFunctions.get_limit(gh_key)

    # Clone a GH repository
    @staticmethod
    def clone_repository(user_name, rep_name, store_dir):
        cmd = "git clone https://github.com/" + user_name + "/" + rep_name
        pipe = subprocess.Popen(cmd, cwd=store_dir, shell=True)
        pipe.wait()
        rep_path = store_dir + "/" + rep_name
        if os.path.isdir(rep_path):
            return True
        else:
            print("Error in clone_repository")
            print(cmd)
            return False

    @staticmethod
    def copy_all_files(db_handler, db_conn,
                       table_res="result_files",
                       store_table="copy_result_files",
                       files_directory="data_GH_projects/projects_without_git",
                       target_dir="data_GH_projects/all_files"):

        query1 = "SELECT path_file FROM " + table_res + ";"
        paths_to_files = db_handler.execute_query(db_conn, query1, True)
        os.environ["COMSPEC"] = 'powershell'

        for i in range(0, len(paths_to_files)):
            file_name = paths_to_files[i][0].split("/")[-1]
            file_path = os.path.join(files_directory, paths_to_files[i][0])

            if os.path.exists(file_path):
                new_file_name = str(i) + "_" + file_name
                new_file_path = os.path.join(target_dir, new_file_name)

                cmd = "cp '" + file_path + "' " + new_file_path
                print(cmd)

                pipe = subprocess.Popen(cmd, shell=True)
                pipe.wait()

                if os.path.exists(new_file_path):
                    query2 = "INSERT INTO " + store_table + "(path_file, path_copy_file) VALUES('" + \
                             paths_to_files[i][0] + "', '" + new_file_name + "');"
                    db_handler.execute_query(db_conn, query2, False)

            else:
                print("Error. Path doesn't exist: " + file_path)

