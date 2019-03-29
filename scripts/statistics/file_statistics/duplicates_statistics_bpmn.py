from src_bpmn_crawler.db_handler import DbHandler
from collections import OrderedDict
import operator
import csv

db_path = "data_GH_projects/databases/result.db"
db_handler = DbHandler()
db_conn_source = db_handler.create_connection(db_path)
bpmn_paths_table = "result_bpmn"
result_table = "result"
dup_table = "files_copy"


def compute_number_bpmn_that_were_duplicated():
    query = "SELECT COUNT(*) FROM (SELECT * FROM " + bpmn_paths_table + ", " + dup_table + \
            " WHERE " + bpmn_paths_table + ".path_bpmn_file=" + dup_table + \
            ".path_bpmn_file GROUP BY duplicate);"

    number_duplicated = db_handler.execute_query(db_conn_source, query, True)[0][0]
    return number_duplicated


def compute_how_many_times_duplicated():
    query = "SELECT duplicate, count(*) FROM " + bpmn_paths_table + ", " + dup_table + \
            " WHERE " + bpmn_paths_table + ".path_bpmn_file=" + dup_table + \
            ".path_bpmn_file AND duplicate IS NOT NULL GROUP BY duplicate;"

    number_duplicated_list = db_handler.execute_query(db_conn_source, query, True)
    return number_duplicated_list


def write_csv_duplicate(number_duplicated_list, csv_file_name, min_percentage=5):
    number_duplicated_dict = {}

    for duplicated in number_duplicated_list:
        if duplicated[1] in number_duplicated_dict:
            number_duplicated_dict[duplicated[1]] = number_duplicated_dict[duplicated[1]] + 1
        else:
            number_duplicated_dict[duplicated[1]] = 1

    number_duplicated_dict = OrderedDict(sorted(number_duplicated_dict.items(), key=operator.itemgetter(1), reverse=True))

    with open(csv_file_name, mode='w+', newline='') as csv_file:
        f_writer = csv.writer(csv_file, delimiter=';', quotechar='"')  # , quoting=csv.QUOTE_ALL)
        f_writer.writerow([' ', 'Anzahl von BPMN Dateien', 'Duplizierungen', 'Prozentsatz'])

        i = 0
        other = 0
        for key, value in number_duplicated_dict.items():
            if key and (value * 100) / len(number_duplicated_list) >= min_percentage:
                i = i + 1
                f_writer.writerow([i, str(value), str(key), round((value * 100) / len(number_duplicated_list), 4)])
            else:
                other = other + value
        i = i + 1
        f_writer.writerow([i, str(other), "Andere", round((other * 100) / len(number_duplicated_list), 4)])


