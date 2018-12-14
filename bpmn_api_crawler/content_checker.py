from bpmn_api_crawler.db_handler import DbHandler
import requests


class FileContChecker:

    DB_TABLE = "projects_bpmn"

    def check_all_files(self, urls_file, target_strs):
        with open(urls_file, 'r') as file:
            lines = file.readlines()
        for line in lines:
            file_content = requests.get(line[:-1]).content
            for target in target_strs:
                if target in str(file_content):
                    file_name = line.split("/")[-1]
                    file_name = file_name.split("\n")[0]
                    repos = self.get_repos(line)
                    (stored_id, language) = self.get_stored_id_language(repos)[0]
                    self.write_to_db(self.DB_TABLE, repos, stored_id, language, file_name, line.split("\n")[0])
                    print(line)

    def get_repos(self, url):
        url_head = "https://raw.githubusercontent.com/"
        (_, tail) = url.split(url_head)
        tail_list = tail.split("/")
        return tail_list[0:2]

    def get_stored_id_language(self, repos):
        db_handler = DbHandler()
        query = "SELECT id, language FROM login_and_project_name WHERE login='" + repos[0] + "' AND name='" + repos[1] + "';"
        return db_handler.connect_db_run_query(query)

    def write_to_db(self, table, repos, old_id, language, name_bpmn_file, file_path):
        db_handler = DbHandler()
        columns = "(stored_id, login, project_name, language, name_bpmn_file, link_bpmn_file)"
        query = "INSERT INTO " + table + columns + " VALUES(" + str(old_id) + ", '" + repos[0] + "', '" + repos[1] + "', '" + language + "', '" + name_bpmn_file + "', '" + file_path + "');"
        print(query)
        db_handler.connect_db_run_query(query, False)

