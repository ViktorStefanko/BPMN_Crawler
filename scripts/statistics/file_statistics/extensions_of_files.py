from collections import OrderedDict
from operator import itemgetter
from src_bpmn_crawler.db_handler import DbHandler
import csv


def get_all_extensions():
    db_path = "data_GH_projects/databases/result.db"
    table_res = "result"
    db_handler = DbHandler()
    db_conn_source = db_handler.create_connection(db_path)
    query = "SELECT link_bpmn_file FROM " + table_res + ";"
    links_to_files = db_handler.execute_query(db_conn_source, query, True)
    extensions_dict = {}
    for link in links_to_files:
        extension_ele = link[0].rsplit(".", 1)[1].lower()
        if extension_ele not in extensions_dict:
            extensions_dict[extension_ele] = 1
        else:
            extensions_dict[extension_ele] = extensions_dict[extension_ele] + 1
    extensions_dict = OrderedDict(sorted(extensions_dict.items(), key=itemgetter(1), reverse=True))
    return [extensions_dict, len(links_to_files)]


def write_extensions_to_csv(extensions_dict, numb_of_files, min_percentage=1, csv_file='scripts/statistics/csv_files/extensions_of_all_files.csv'):
    with open(csv_file, mode='w+', newline='') as csv_file:
        f_writer = csv.writer(csv_file, delimiter=';', quotechar='"')  # quoting=csv.QUOTE_MINIMAL)
        f_writer.writerow([" ", "Dateiendung", "Anzahl", "Prozentsatz"])

        i = 0
        other = 0
        for key, value in extensions_dict.items():
            if (value * 100) / numb_of_files > min_percentage:
                i = i + 1
                f_writer.writerow([i, str(key), str(value), round((value * 100) / numb_of_files, 4)])
            else:
                other = other + value
        i = i + 1
        f_writer.writerow([i, "andere", str(other), round((other * 100) / numb_of_files, 4)])



