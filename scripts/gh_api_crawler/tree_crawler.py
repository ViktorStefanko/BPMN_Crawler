from scripts.gh_api_crawler.db_handler import DbHandler
from scripts.gh_api_crawler.other_functions import UsefulFunctions
import json
import os


class TreeCrawler:
    GITHUB_API = "https://api.github.com/repos/"
    START = "https://raw.githubusercontent.com/"
    KEYWORD = "bpmn"
    db_handler = DbHandler()

    def __init__(self, res_table):
        self.DB_TABLE = res_table

    def get_repo_list(self, trees_dir):
        """
        :param trees_dir: it contains subdirectories for each user. Subdirectory
        contains JSON file/files with the tree structure of repository
        :return: list of tuples (username, repository_name)
        """

        user_dir_list = os.listdir(trees_dir)
        repo_list = []

        for user_dir in user_dir_list:
            repo_jsons = os.listdir(trees_dir + "/" + user_dir)
            for json_file in repo_jsons:
                delimiter = user_dir + "__"
                elements = json_file.split(delimiter)
                repo = ""
                if len(elements) == 2:
                    repo = elements[1]
                else:
                    for i in elements[1:]:
                        if i:
                            repo += str(i)
                        else:
                            repo += delimiter
                repo_list.append((user_dir, repo[:-5]))
        return repo_list

    def obtain_branch(self, username, repo, default_dir):
        """
        :return: default branch of repository
        """
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

    def is_interesting(self, path):
        """
        :param path: full path of file
        :return: True if file's name or its extension contains KEYWORD; False otherwise
        """

        tmp_list = path.split('/')
        if len(tmp_list) > 1:
            full_name = tmp_list[-1]  # with extension
            if self.KEYWORD in full_name.lower():
                return True
            else:
                return False
        else:
            return False

    def write_to_db(self, conn, username, repo, file_link, file_path):
        """
        Writes result into database
        :return: True, if wrote without exceptions; False otherwise
        """
        columns = "(login, name, link_file, path_file)"
        query = "INSERT INTO " + self.DB_TABLE + " " + columns + \
                " VALUES('" + username + "', '" + repo + "', '" + file_link + "', '" + file_path + "');"
        if self.db_handler.execute_query(conn, query, False):
           return True
        else:
            return False

    def search_files(self, conn, repo_list, trees_dir, default_dir):
        UsefulFunctions.make_dir("cloned_repositories")
        """
        For each JSON file with the tree structure of repository search for BPMN file.
        If found, write username, repo_name and path of file's content into database.
        """
        for repo in repo_list:
            with open(trees_dir + "/" + repo[0] + "/" + repo[0] + "__" + repo[1] + ".json") as data_file:
                data = json.load(data_file)
            try:
                tree = data["tree"]
            except KeyError:
                print("KeyError: " + str(repo[0]) + "/" + str(repo[1]))
                continue
            contains_bpmn = False
            for file_dict in tree:
                try:
                    if file_dict["type"] != "tree":
                        if self.is_interesting(file_dict["path"]):
                            contains_bpmn = True
                            url = str(file_dict["url"])
                            (_, blob) = url.split("https://api.github.com/")
                            blob_list = blob.split('/')
                            username = blob_list[1]
                            proj_name = blob_list[2]
                            branch = self.obtain_branch(username, proj_name, default_dir)
                            if not branch:
                                continue
                            total_link = self.START + username + "/" + proj_name + "/" + branch + "/" + str(
                                file_dict["path"])
                            path = username + "/" + proj_name + "/" + str(file_dict["path"])
                            if not self.write_to_db(conn, username, proj_name, total_link, path):
                                return False
                except:
                    print("Exception in tree_crawler " + str(repo))
                    continue
            if contains_bpmn:
                UsefulFunctions.make_dir("cloned_repositories/" + str(repo[0]))
                UsefulFunctions.clone_repository(repo[0], repo[1], "cloned_repositories/" + str(repo[0]))
        return True
