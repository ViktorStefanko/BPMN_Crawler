from bpmn_api_crawler.db_handler import DbHandler
import json
import os


class TreeCrawler:
    GITHUB_API = "https://api.github.com/repos/"
    START = "https://raw.githubusercontent.com/"
    DB_TABLE = "projects_bpmn"

    # Common extensions for BPMN files
    BPMN_EXTENSIONS = ["bpmn"]
    # (1) Common filenames for BPMN files AND (see (2))
    KEYWORD_LIST = ["bpmn"]
    # (2) with following extensions
    OTHER_EXTENSIONS = ["xml"]

    def get_repo_list(self, trees_dir):
        user_dir_list = os.listdir(trees_dir)
        repo_list = []

        for user_dir in user_dir_list:
            repo_jsons = os.listdir(trees_dir + "/" + user_dir)
            for json_file in repo_jsons:
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

    def extension(self, path):
        # Given a path, return its extension
        tmp_list = path.split('.')
        if len(tmp_list) > 1:
            return tmp_list[-1].lower()
        else:
            return ""

    def filename(self, path):
        """"
        Given a path, return its filename (without extension)
        """
        tmp_list = path.split('/')
        if len(tmp_list) > 1:
            full_name = tmp_list[-1]  # with extension
            if '.' in full_name:
                full_name = '.'.join(full_name.split('.')[:-1])
            return full_name.lower()
        else:
            return ""

    def interesting(self, path):
        ext = self.extension(path)
        if ext in self.BPMN_EXTENSIONS:
            return 1
        if ext in self.OTHER_EXTENSIONS:
            for keyword in self.KEYWORD_LIST:
                if keyword in self.filename(path):
                    return 1
            return 0
        else:
            return 0

    def write_to_db(self, username, repo, file_path):
        db_handler = DbHandler()
        columns = "(login, project_name, link_bpmn_file)"
        query = "INSERT INTO " + self.DB_TABLE + columns + " VALUES('" + username + "', '" + repo + "', '" + file_path + "');"
        print(query)
        db_handler.connect_db_run_query(query, False)

    def search_files(self, repo_list, trees_dir, default_dir):
        for repo in repo_list:
            with open(trees_dir + "/" + repo[0] + "/" + repo[0] + "__" + repo[1] + ".json") as data_file:
                data = json.load(data_file)
            try:
                tree = data["tree"]
            except KeyError:
                print("KeyError: " + str(repo[0]) + "/" + str(repo[1]))
                continue
            print(tree)

            for file_dict in tree:
                if file_dict["type"] != "tree":
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
                        self.write_to_db(username, repo, total)

    def make_file(self, file_name):
        if not os.path.isfile(file_name):
            f = open(file_name, "w+")
            f.close()
        return file_name
