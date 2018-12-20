import subprocess
import os
import multiprocessing
import time
from bpmn_crawler.api_code_crawler import ApiCodeCrawler

class Crawler:
    @staticmethod
    def traverse_all_repositories(log_rep_list, store_dir, store_file, db_cursor, target_file):
        print("Length of log_rep_list: " + str(len(log_rep_list)))
        counter = 0
        for log_rep in log_rep_list:
            clone_result = True
            # Start git_clone() as a process
            p = multiprocessing.Process(target=Crawler.clone_repository, name="Clone_repository", args=(log_rep[0], log_rep[1], store_dir))
            p.start()

            # Wait 10 seconds for foo
            time.sleep(10)

            # If thread is active
            if p.is_alive():
                print("Clone_repository is running... let's kill it...")

                # Terminate clone_repository()
                p.terminate()
                # Cleanup
                s = "http://www.omg.org/spec/BPMN/20100524/MODEL"
                ApiCodeCrawler.traverse_user_rep([log_rep], store_dir, store_file, db_cursor, s)
                continue
            p.join()



            #clone_result = Crawler.clone_repository(log_rep[0], log_rep[1], store_dir)
            print(clone_result)
            if clone_result:
                counter += 1
                print(counter)
                result = Crawler.find_files(store_dir, log_rep[1], store_file, target_file)
                if result:
                    try:
                        sql = "INSERT INTO projects_bpmn (login, project_name, language, stored_id) VALUES (%s, %s, %s, %s)"
                        val = (log_rep[0], log_rep[1], log_rep[2], log_rep[3])
                        db_cursor.execute(sql, val)
                    except:
                        print("Error!")
                Crawler.remove_repository(store_dir, log_rep[1])

    # Clone a GH repository
    @staticmethod
    def clone_repository(user_name, rep_name, store_dir):
        cmd = "git clone https://github.com/" + user_name + "/" + rep_name
        pipe = subprocess.Popen(cmd, cwd=store_dir, shell=True)
        pipe.wait()
        rep_path = store_dir + "\\" + rep_name
        if os.path.isdir(rep_path):
            return True
        else:
            return False

    # Find files and store their paths to the text file
    @staticmethod
    def find_files(store_dir, rep_name, store_f, target_f):
        rep_path = store_dir + "\\" + rep_name
        f = open(store_f, "a+", encoding='utf-8')
        for root, dirs, files in os.walk(rep_path):
            for file in files:
                if file.endswith(target_f[0]) or file.endswith(target_f[1]):
                    if Crawler.is_bpmn_file(os.path.join(root, file)):
                        f.write(os.path.join(root, file)[len(store_dir) + 1:] + "\n")
                        f.close()
                        return True

    @staticmethod
    def is_bpmn_file(xml_file):
        datafile = open(xml_file, "r", encoding='utf-8')
        for line in datafile:
            if "http://www.omg.org/spec/BPMN/20100524/MODEL" in line:
                return True
        return False

    # Remove repository
    @staticmethod
    def remove_repository(store_dir, rep_name):
        to_remove = store_dir + "\\" + rep_name
        if os.path.isdir(to_remove):
            cmd = "rm -rf " + to_remove
            pipe = subprocess.Popen(cmd, shell=True)
            pipe.wait()