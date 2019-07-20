from scripts.gh_api_crawler.db_handler import DbHandler
from scripts.statistics.functions_for_code_maat import CodeMaatFunctions
import requests
import operator
import os
import pytz


class RepositoryStatistics:

    def __init__(self, gh_key, db_result_path="databases/ghbpmn.db",
                 table_result_projects="result_projects",
                 table_all_gh_users="users",
                 projects_dir="data_GH_projects/projects_only_git",
                 code_maat_path="C:/Users/viktor/Documents/education/bachelorarbeit/code-"
                                "maat/target/code-maat-1.1-SNAPSHOT-standalone.jar"):

        self.db_result_path = db_result_path
        self.table_result_projects = table_result_projects
        self.table_all_gh_users = table_all_gh_users
        self.GH_KEY = gh_key
        self.db_handler = DbHandler()
        self.db_conn_source = self.db_handler.create_connection(self.db_result_path)
        self.projects_dir = projects_dir
        self.code_maat_path = code_maat_path

    def add_languages(self):
        query = "SELECT login, name FROM " + self.table_result_projects + ";"
        repo_list = self.db_handler.execute_query(self.db_conn_source, query, True)

        for repo in repo_list:
            url = "https://api.github.com/repos/" + repo[0] + "/" + repo[1] + "/languages?" + self.GH_KEY
            try:
                data = requests.get(url).json()
                language = max(data.items(), key=operator.itemgetter(1))[0]
                query = "UPDATE " + self.table_result_projects + " SET language='" + language + \
                        "' WHERE login='" + repo[0] + \
                        "' AND name='" + repo[1] + "';"
                self.db_handler.execute_query(self.db_conn_source, query, False)
            except:
                print("ERROR: " + str(url))

    def add_repo_location(self):
        query1 = "SELECT login, name FROM " + self.table_result_projects + ";"
        repo_list = self.db_handler.execute_query(self.db_conn_source, query1, True)

        for repo in repo_list:
            url1 = "https://api.github.com/repos/" + repo[0] + "/" + repo[1] + "/contributors?" + self.GH_KEY
            contributors_list = requests.get(url1).json()
            locations_list = []
            try:
                for contributor in contributors_list:
                    query = "SELECT country_code FROM " + self.table_all_gh_users + \
                            " WHERE login='" + str(contributor['login']) + "';"
                    location_result = self.db_handler.execute_query(self.db_conn_source, query, True)
                    if location_result:
                        location = location_result[0][0]
                        if location and not location == '\\N' and location not in locations_list:
                            locations_list.append(location)
                if locations_list:
                    new_list = list()
                    for loc in locations_list:
                        new_list.append(pytz.country_names[loc])
                    query2 = 'UPDATE ' + self.table_result_projects + ' SET location_country="' + str(new_list) + \
                             '" WHERE login="' + repo[0] + \
                             '" AND name="' + repo[1] + '";'
                    self.db_handler.execute_query(self.db_conn_source, query2, False)
            except:
                print(f'exception for {repo}')

    def add_commits(self):
        query = "SELECT login, name FROM " + self.table_result_projects + ";"
        repo_list = self.db_handler.execute_query(self.db_conn_source, query, True)

        for repo in repo_list:
            repo_path = os.path.join(os.path.join(self.projects_dir, repo[0]), repo[1])
            if os.path.exists(repo_path):
                log_file_path = os.path.join(repo_path, "logfile.log")
                if not os.path.exists(log_file_path):
                    CodeMaatFunctions.create_log_file(repo_path, log_file_path)
                else:
                    name_csv_file1 = "repo_stat.csv"
                    name_csv_file2 = "repo_stat_summary.csv"

                    csv_path1 = os.path.join(repo_path, name_csv_file1)
                    csv_path2 = os.path.join(repo_path, name_csv_file2)
                    if not os.path.exists(csv_path1) or not os.path.exists(csv_path2):
                        CodeMaatFunctions.collect_repo_informations(self.code_maat_path, log_file_path,
                                                                    csv_path1, csv_path2)
                    else:
                        csv_reader = open(csv_path1, encoding="utf8")
                        lines = csv_reader.readlines()
                        csv_reader.close()
                        if len(lines) > 2:
                            query = "UPDATE " + self.table_result_projects + " SET created_at='" + \
                                    lines[1].split(",", 1)[
                                        0] + \
                                    "', last_commit_at='" + lines[-1].split(",", 1)[0] + \
                                    "' WHERE login='" + repo[0] + "' AND name='" + repo[1] + "';"
                            self.db_handler.execute_query(self.db_conn_source, query, False)
                        elif len(lines) == 2:
                            query = "UPDATE " + self.table_result_projects + " SET created_at='" + \
                                    lines[1].split(",", 1)[
                                        0] + \
                                    "', last_commit_at='" + lines[1].split(",", 1)[0] + \
                                    "' WHERE login='" + repo[0] + "' AND name='" + repo[1] + "';"
                            self.db_handler.execute_query(self.db_conn_source, query, False)

                        csv_reader = open(csv_path2, encoding="utf8")
                        lines = csv_reader.readlines()
                        csv_reader.close()
                        if len(lines) > 1:
                            try:
                                n_commits = lines[1].split('\n')[0].split('number-of-commits,')[1]

                                query = "UPDATE " + self.table_result_projects + " SET n_commits='" + \
                                        n_commits + "' WHERE login='" + repo[0] + "' AND name='" + repo[1] + "';"
                                self.db_handler.execute_query(self.db_conn_source, query, False)
                            except:
                                print("Error: " + str(lines))
            else:
                print("Error path doesn't exist: " + repo_path)