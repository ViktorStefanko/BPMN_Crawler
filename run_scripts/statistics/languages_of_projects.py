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


def make_csv(languages_list, file_name):
    number_repos_with_language = len(languages_list)
    languages_dict = {}

    for language in languages_list:
        if language in languages_dict:
            languages_dict[language] = languages_dict[language] + 1
        else:
            languages_dict[language] = 1

    languages_dict = OrderedDict(sorted(languages_dict.items(), key=operator.itemgetter(1), reverse=True))

    with open(file_name, mode='w+', newline='') as csv_file:
        f_writer = csv.writer(csv_file, delimiter=';', quotechar='"')#, quoting=csv.QUOTE_ALL)
        f_writer.writerow([' ', 'Programmiersprache', 'Anzahl', 'Prozentsatz'])

        i = 0
        other = 0
        for key, value in languages_dict.items():
            if (value * 100) / number_repos_with_language >= 5:
                i = i + 1
                f_writer.writerow([i, str(key), str(value), round((value * 100) / number_repos_with_language, 4)])
            else:
                other = other + value
        i = i + 1
        f_writer.writerow([i, "andere", str(other), " "])


def make_csv_all_repos(name_csv):
    query = "SELECT language FROM " + table + ";"
    languages_list = db_handler.execute_query(db_conn_source, query, True)
    make_csv(languages_list, name_csv)


def make_csv_special_repos(spec_table, name_csv):
    query = "SELECT DISTINCT language, " + table + ".login, " + table +\
            ".project_name FROM " + table + ", " + spec_table +\
            " WHERE " + table + ".login=" + spec_table + ".login AND " +\
            table + ".project_name=" + spec_table + ".project_name;"

    languages_list = db_handler.execute_query(db_conn_source, query, True)
    make_csv(languages_list, name_csv)

add_languages_to_table()


"""
make_csv_all_repos('statistics/csv_files/languages_all_repos.csv')
make_csv_special_repos('result_xml', 'statistics/csv_files/languages_xml_repos.csv')
make_csv_special_repos('result_bpmn', 'statistics/csv_files/languages_bpmn_repos.csv')
make_csv_special_repos('result_bpmn2', 'statistics/csv_files/languages_bpmn2_repos.csv')
make_csv_special_repos('result_png', 'statistics/csv_files/languages_png_repos.csv')
make_csv_special_repos('result_json', 'statistics/csv_files/languages_json_repos.csv')
"""