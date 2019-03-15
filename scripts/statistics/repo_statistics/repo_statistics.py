from src.db_handler import DbHandler
from scripts.statistics.file_statistics.functions_for_code_maat import *
import os
import csv

db_path = "data_GH_projects/databases/result.db"
projects_table = "projects"
db_handler = DbHandler()
db_conn_source = db_handler.create_connection(db_path)


def compute_repo_statistics():
    query = "SELECT login, project_name FROM " + projects_table + ";"
    repo_list = db_handler.execute_query(db_conn_source, query, True)
    projects_dir = "data_GH_projects\\projects_only_git"
    code_maat_path = "C:\\Users\\viktor\\Documents\education\\bachelorarbeit\\code-maat\\target\\code-maat-1.1-SNAPSHOT-standalone.jar"

    for repo in repo_list:
        repo_path = os.path.join(os.path.join(projects_dir, repo[0]), repo[1])
        if os.path.exists(repo_path):
            log_file_path = os.path.join(repo_path, "logfile.log")

            name_csv_file = "repo_stat.csv"
            csv_path = os.path.join(repo_path, name_csv_file)
            make_repo_statistics(code_maat_path, log_file_path, csv_path)

            csv_reader = open(csv_path, encoding="utf8")
            lines = csv_reader.readlines()
            csv_reader.close()
            if len(lines) > 2:
                query = "UPDATE " + projects_table + " SET created_at='" + lines[1].split(",", 1)[0] + \
                        "', last_commit_at='" + lines[-1].split(",", 1)[0] + \
                        "' WHERE login='" + repo[0] + "' AND project_name='" + repo[1] + "';"
                db_handler.execute_query(db_conn_source, query, False)
            elif len(lines) == 2:
                query = "UPDATE " + projects_table + " SET created_at='" + lines[1].split(",", 1)[0] + \
                        "', last_commit_at='" + lines[1].split(",", 1)[0] + \
                        "' WHERE login='" + repo[0] + "' AND project_name='" + repo[1] + "';"
                db_handler.execute_query(db_conn_source, query, False)
        else:
            print("Error path doesn't exist: " + repo_path)


def write_csv_projects_created_at(csv_name, min_percentage):
    query = "SELECT created_at FROM " + projects_table + ";"
    created_at_list = db_handler.execute_query(db_conn_source, query, True)
    created_at_list = [i[0] for i in created_at_list]

    date_dic = {}
    for i in range(0, (2019 - 2005)):
        date_dic[(str(2005 + i) + "-01-01", str(2005 + i) + "-05-31")] = 0
        date_dic[(str(2005 + i) + "-06-01", str(2005 + i) + "-12-31")] = 0
    date_dic[("2019-01-01", "2019-05-31")] = 0

    for created_at in created_at_list:
        for key, value in date_dic.items():
            if str(created_at) > str(key[0]) and str(created_at) < str(key[1]):
                date_dic[key] = date_dic[key] + 1
    make_csv(date_dic, len(created_at_list), csv_name, min_percentage)


def write_csv_projects_last_commit_at(csv_name, min_percentage):
    query = "SELECT last_commit_at FROM " + projects_table + ";"
    last_commit_at_list = db_handler.execute_query(db_conn_source, query, True)
    last_commit_at_list = [i[0] for i in last_commit_at_list]

    date_dic = {}
    for i in range(0, (2019 - 2005)):
        date_dic[(str(2005 + i) + "-01-01", str(2005 + i) + "-05-31")] = 0
        date_dic[(str(2005 + i) + "-06-01", str(2005 + i) + "-12-31")] = 0
    date_dic[("2019-01-01", "2019-05-31")] = 0

    for last_commit_at in last_commit_at_list:
        for key, value in date_dic.items():
            if str(last_commit_at) > str(key[0]) and str(last_commit_at) < str(key[1]):
                date_dic[key] = date_dic[key] + 1
    make_csv(date_dic, len(last_commit_at_list), csv_name, min_percentage)


def make_csv(statistics_dic, number_repos, csv_file_name, min_percentage=5):

    with open(csv_file_name, mode='w+', newline='') as csv_file:
        f_writer = csv.writer(csv_file, delimiter=';', quotechar='"')  # , quoting=csv.QUOTE_ALL)
        f_writer.writerow([' ', 'Zeit', 'Anzahl von Projekten', 'Prozentsatz'])

        i = 0
        other = 0
        for key, value in statistics_dic.items():
            if key and (value * 100) / number_repos >= min_percentage:
                i = i + 1
                f_writer.writerow([i, str(key), str(value), round((value * 100) / number_repos, 4)])
            else:
                other = other + value
        i = i + 1
        f_writer.writerow([i, "andere", str(other), round((other * 100) / number_repos, 4)])
