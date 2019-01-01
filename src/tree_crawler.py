from src.db_handler import DbHandler
import json
import os


class TreeCrawler:
    GITHUB_API = "https://api.github.com/repos/"
    START = "https://raw.githubusercontent.com/"

    def __init__(self, projects_bpmn_table):
        self.DB_TABLE = projects_bpmn_table

    KEYWORD = "bpmn"

    def get_repo_list(self, trees_dir):
        user_dir_list = os.listdir(trees_dir)
        repo_list = []

        for user_dir in user_dir_list:
            repo_jsons = os.listdir(trees_dir + "/" + user_dir)
            for json_file in repo_jsons:
                print(json_file)
                (_, repo) = json_file.split(user_dir + "__")
                repo_list.append((user_dir, repo[:-5]))
        return repo_list

    def obtain_branch(self, username, repo, default_dir):
        file_path = default_dir + "/" + username + "/" + username + "__" + repo + ".json"
        if os.path.isfile(file_path):
            with open(file_path) as data_file:
                data = json.load(data_file)
                try:
                    return data["default_branch"]
                except KeyError:
                    print("ERROR:", file_path)
                    return 0
        return "master"

    def interesting(self, path):
        tmp_list = path.split('/')
        if len(tmp_list) > 1:
            full_name = tmp_list[-1]  # with extension
            if self.KEYWORD in full_name:
                return 1
            else:
                return 0
        else:
            return 0

    def write_to_db(self, conn, username, repo, file_path):
        db_handler = DbHandler()
        columns = "(login, project_name, link_bpmn_file)"
        query = "INSERT INTO " + self.DB_TABLE + " " + columns + " VALUES('" + username + "', '" + repo + "', '" + file_path + "');"
        if db_handler.execute_query(conn, query, False):
           return True
        else:
            return False

    def search_files(self,conn, repo_list, trees_dir, default_dir):
        for repo in repo_list:
            with open(trees_dir + "/" + repo[0] + "/" + repo[0] + "__" + repo[1] + ".json") as data_file:
                data = json.load(data_file)
            try:
                tree = data["tree"]
            except KeyError:
                print("KeyError: " + str(repo[0]) + "/" + str(repo[1]))
                continue
            for file_dict in tree:
                if file_dict["type"] != "tree":
                    try:
                        if self.interesting(file_dict["path"]):
                            url = str(file_dict["url"])
                            (_, blob) = url.split("https://api.github.com/")
                            blob_list = blob.split('/')
                            username = blob_list[1]
                            repo = blob_list[2]
                            branch = self.obtain_branch(username, repo, default_dir)
                            if not branch:
                                continue
                            total = self.START + username + "/" + repo + "/" + branch + "/" + str(file_dict["path"])
                            if not self.write_to_db(conn, username, repo, total):
                                return False
                    except:
                        print("Exception in tree_crawler " + str(repo))
                        continue
        return True
