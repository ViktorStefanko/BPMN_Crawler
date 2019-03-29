from src_bpmn_crawler.db_handler import DbHandler
from scripts.statistics.other_scripts.functions_for_code_maat import *
import operator
from collections import OrderedDict
import os
import csv

db_path = "data_GH_projects/databases/result.db"
table = "result"
db_handler = DbHandler()
db_conn_source = db_handler.create_connection(db_path)


def write_csv_n_authors(n_authors_list, csv_name):
    n_authors_dict = {}

    for n_authors in n_authors_list:
        if n_authors in n_authors_dict:
            n_authors_dict[n_authors] = n_authors_dict[n_authors] + 1
        else:
            n_authors_dict[n_authors] = 1

    n_authors_dict = OrderedDict(sorted(n_authors_dict.items(), key=operator.itemgetter(1), reverse=True))

    with open(csv_name, mode='w+', newline='') as csv_file:
        f_writer = csv.writer(csv_file, delimiter=';', quotechar='"')  # , quoting=csv.QUOTE_ALL)
        f_writer.writerow([' ', 'Autoren', 'Anzahl', 'Prozentsatz'])

        i = 1
        for key, value in n_authors_dict.items():
            f_writer.writerow([i, str(key), str(value), round((value * 100) / len(n_authors_list), 4)])
            i = i + 1


def write_csv_file_n_authors(csv_name):
    query = "SELECT n_authors FROM " + table + ";"
    n_authors_list = db_handler.execute_query(db_conn_source, query, True)
    n_authors_list = [i[0] for i in n_authors_list]
    write_csv_n_authors(n_authors_list, csv_name)


def write_csv_file_bpmn_n_authors(csv_name):
    bpmn_paths_table = "result_bpmn"

    query = "SELECT n_authors FROM " + table + \
            " WHERE path_bpmn_file IN (" + "SELECT path_bpmn_file FROM " + bpmn_paths_table + ");"
    n_authors_list = db_handler.execute_query(db_conn_source, query, True)
    n_authors_list = [i[0] for i in n_authors_list]
    write_csv_n_authors(n_authors_list, csv_name)


def write_csv_n_revs(n_revs_list, csv_name, min_percentage=0.01):
    n_revs_dict = {}

    for n_revs in n_revs_list:
        if n_revs in n_revs_dict:
            n_revs_dict[n_revs] = n_revs_dict[n_revs] + 1
        else:
            n_revs_dict[n_revs] = 1

    n_revs_dict = OrderedDict(sorted(n_revs_dict.items(), key=operator.itemgetter(1), reverse=True))

    with open(csv_name, mode='w+', newline='') as csv_file:
        f_writer = csv.writer(csv_file, delimiter=';', quotechar='"')  # , quoting=csv.QUOTE_ALL)
        f_writer.writerow([' ', 'Änderungen', 'Anzahl', 'Prozentsatz'])

        i = 0
        other = 0
        for key, value in n_revs_dict.items():
            if key and (value * 100) / len(n_revs_list) >= min_percentage:
                i = i + 1
                f_writer.writerow([i, str(key), str(value), round((value * 100) / len(n_revs_list), 4)])
            else:
                other = other + value
        i = i + 1
        f_writer.writerow([i, "andere", str(other), round((other * 100) / len(n_revs_list), 4)])


def write_csv_file_n_revs(csv_name, min_percentage):
    query = "SELECT n_revs FROM " + table + ";"
    n_revs_list = db_handler.execute_query(db_conn_source, query, True)
    n_revs_list = [i[0] for i in n_revs_list]
    write_csv_n_revs(n_revs_list, csv_name, min_percentage)


def write_csv_file_bpmn_n_revs(csv_name, min_percentage):
    bpmn_paths_table = "result_bpmn"

    query = "SELECT n_revs FROM " + table + \
            " WHERE path_bpmn_file IN (" + "SELECT path_bpmn_file FROM " + bpmn_paths_table + ");"
    n_revs_list = db_handler.execute_query(db_conn_source, query, True)
    n_revs_list = [i[0] for i in n_revs_list]
    write_csv_n_revs(n_revs_list, csv_name, min_percentage)


def write_csv_age_months(age_months_list, csv_name, min_percentage=0.01):
    age_months_dict = {}
    for age_months in age_months_list:
        if age_months in age_months_dict:
            age_months_dict[age_months] = age_months_dict[age_months] + 1
        else:
            age_months_dict[age_months] = 1

    age_months_dict = OrderedDict(sorted(age_months_dict.items(), key=operator.itemgetter(1), reverse=True))

    with open(csv_name, mode='w+', newline='') as csv_file:
        f_writer = csv.writer(csv_file, delimiter=';', quotechar='"')  # , quoting=csv.QUOTE_ALL)
        f_writer.writerow([' ', 'Alter in Monaten', 'Anzahl', 'Prozentsatz'])

        i = 0
        other = 0
        for key, value in age_months_dict.items():
            if key and (value * 100) / len(age_months_list) >= min_percentage:
                i = i + 1
                f_writer.writerow([i, str(key), str(value), round((value * 100) / len(age_months_list), 4)])
            else:
                other = other + value
        i = i + 1
        f_writer.writerow([i, "andere", str(other), round((other * 100) / len(age_months_list), 4)])


def write_csv_file_age_months(csv_name, min_percentage):
    query = "SELECT age_months FROM " + table + ";"
    age_months_list = db_handler.execute_query(db_conn_source, query, True)
    age_months_list = [i[0] for i in age_months_list]
    write_csv_age_months(age_months_list, csv_name, min_percentage)


def write_csv_file_bpmn_age_months(csv_name, min_percentage):
    bpmn_paths_table = "result_bpmn"

    query = "SELECT age_months FROM " + table + \
            " WHERE path_bpmn_file IN (" + "SELECT path_bpmn_file FROM " + bpmn_paths_table + ");"
    age_months_list = db_handler.execute_query(db_conn_source, query, True)
    age_months_list = [i[0] for i in age_months_list]
    write_csv_age_months(age_months_list, csv_name, min_percentage)


def compute_file_statistics():
    query1 = "SELECT DISTINCT login, project_name FROM " + table + " WHERE n_authors IS NULL " + \
             " AND login NOT LIKE 'hboutemy' AND login NOT LIKE 'JanuaryA2';"
    repo_list = db_handler.execute_query(db_conn_source, query1, True)
    projects_dir = "projects_only_git"
    code_maat_path = "C:\\Users\\viktor\\Documents\education\\bachelorarbeit\\code-maat\\target\\code-maat-1.1-SNAPSHOT-standalone.jar"
    statistics_file_utf16_csv = "files_stat_utf16.csv"
    age_file_utf16_csv = "age_files_utf16.csv"

    for repo in repo_list:
        repo_path = os.path.join(os.path.join(projects_dir, repo[0]), repo[1])
        if os.path.exists(repo_path):
            query2 = "SELECT path_bpmn_file FROM " + table + \
                     " WHERE login='" + repo[0] + \
                     "' AND project_name='" + repo[1] + "';"
            bpmn_file_list = db_handler.execute_query(db_conn_source, query2, True)

            log_file_path = os.path.join(repo_path, "logfile.log")
            statistics_utf16_csv_path = os.path.join(repo_path, statistics_file_utf16_csv)
            age_utf16_csv_path = os.path.join(repo_path, age_file_utf16_csv)
            make_files_statistics(code_maat_path, log_file_path, statistics_utf16_csv_path,
                                  age_utf16_csv_path)

            data = open(statistics_utf16_csv_path, encoding="utf16")
            reader = csv.reader(data)
            for line_list in reader:
                if line_list[0].lower().find("bpmn") != -1:
                    if line_list[0].find("{") == -1 and line_list[0].find("=>") == -1:
                        git_file_path = repo[0] + "/" + repo[1] + "/" + line_list[0]
                    elif line_list[0].find("{") != -1:
                        first_split = line_list[0].split("{")
                        second_split = first_split[1].split("}")
                        middle_split = second_split[0].split("=> ")
                        if not middle_split[1]:
                            str_line = first_split[0] + second_split[1].split("/", 1)[1]
                        else:
                            str_line = first_split[0] + middle_split[1] + second_split[1]
                        git_file_path = repo[0] + "/" + repo[1] + "/" + str_line
                    else:
                        middle_split = line_list[0].split("=> ")
                        git_file_path = repo[0] + "/" + repo[1] + "/" + middle_split[1]

                    for bpmn_file in bpmn_file_list:
                        if git_file_path == bpmn_file[0]:
                            query3 = "UPDATE " + table + " SET n_authors='" + line_list[1] + \
                                     "', n_revs='" + line_list[2] + \
                                     "' WHERE path_bpmn_file='" + bpmn_file[0] + "';"
                            db_handler.execute_query(db_conn_source, query3, False)
                            break

            data = open(age_utf16_csv_path, encoding="utf16")
            reader = csv.reader(data)
            for line_list in reader:
                if line_list[0].lower().find("bpmn") != -1:
                    if line_list[0].find("{") == -1 and line_list[0].find("=>") == -1:
                        git_file_path = repo[0] + "/" + repo[1] + "/" + line_list[0]
                    elif line_list[0].find("{") != -1:
                        first_split = line_list[0].split("{")
                        second_split = first_split[1].split("}")
                        middle_split = second_split[0].split("=> ")
                        if not middle_split[1]:
                            str_line = first_split[0] + second_split[1].split("/", 1)[1]
                        else:
                            str_line = first_split[0] + middle_split[1] + second_split[1]
                        git_file_path = repo[0] + "/" + repo[1] + "/" + str_line
                    else:
                        middle_split = line_list[0].split("=> ")
                        git_file_path = repo[0] + "/" + repo[1] + "/" + middle_split[1]
                    for bpmn_file in bpmn_file_list:
                        if git_file_path == bpmn_file[0]:
                            query4 = "UPDATE " + table + " SET age_months='" + line_list[1] + \
                                     "' WHERE path_bpmn_file='" + bpmn_file[0] + "';"
                            db_handler.execute_query(db_conn_source, query4, False)
                            break
        else:
            print("Error path doesn't exist: " + repo_path)
