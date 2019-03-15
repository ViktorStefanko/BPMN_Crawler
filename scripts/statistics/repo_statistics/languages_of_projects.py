from src.db_handler import DbHandler
import requests
import operator
from collections import OrderedDict
import csv

db_path = "data_GH_projects/databases/result.db"
table = "projects"
GH_KEY = ""
db_handler = DbHandler()
db_conn_source = db_handler.create_connection(db_path)


def add_languages_to_table():
    query = "SELECT login, project_name FROM " + table + ";"
    repo_list = db_handler.execute_query(db_conn_source, query, True)

    for repo in repo_list:
        # Lists languages for the specified repository.
        # The value shown for each language is
        # the number of bytes of code written in that language.
        url = "https://api.github.com/repos/" + repo[0] + "/" + repo[1] + "/languages?" + GH_KEY
        try:
            data = requests.get(url).json()
            language = max(data.items(), key=operator.itemgetter(1))[0]
            query = "UPDATE " + table + " SET language='" + language + \
                    "' WHERE login='" + repo[0] + \
                    "' AND project_name='" + repo[1] + "';"
            db_handler.execute_query(db_conn_source, query, False)
        except:
            print("ERROR: " + str(url))


def make_csv(languages_list, csv_file_name, min_percentage=5):
    number_repos_with_language = len(languages_list)
    languages_dict = {}

    for language in languages_list:
        if language[0] in languages_dict:
            languages_dict[language[0]] = languages_dict[language[0]] + 1
        else:
            languages_dict[language[0]] = 1

    languages_dict = OrderedDict(sorted(languages_dict.items(), key=operator.itemgetter(1), reverse=True))

    with open(csv_file_name, mode='w+', newline='') as csv_file:
        f_writer = csv.writer(csv_file, delimiter=';', quotechar='"')#, quoting=csv.QUOTE_ALL)
        f_writer.writerow([' ', 'Programmiersprache', 'Anzahl', 'Prozentsatz'])

        i = 0
        other = 0
        for key, value in languages_dict.items():
            if key and (value * 100) / number_repos_with_language >= min_percentage:
                i = i + 1
                f_writer.writerow([i, str(key), str(value), round((value * 100) / number_repos_with_language, 4)])
            else:
                other = other + value
        i = i + 1
        f_writer.writerow([i, "andere", str(other), round((other * 100) / number_repos_with_language, 4)])


def make_csv_languages_all_repos(csv_file_name, min_percentage=5):
    query = "SELECT language FROM " + table + ";"
    languages_list = db_handler.execute_query(db_conn_source, query, True)
    make_csv(languages_list, csv_file_name, min_percentage)


def make_csv_languages_bpmn_repos(csv_file_name, min_percentage=5):
    bpmn_paths_table = "result_bpmn"
    result_table = "result"
    projects_table = "projects"

    query = "SELECT language FROM " + projects_table + \
            " WHERE (login, project_name) IN (SELECT DISTINCT login, project_name FROM " + result_table + \
             " WHERE path_bpmn_file IN (" + "SELECT path_bpmn_file FROM " + bpmn_paths_table + "));"
    languages_list = db_handler.execute_query(db_conn_source, query, True)
    make_csv(languages_list, csv_file_name, min_percentage)
