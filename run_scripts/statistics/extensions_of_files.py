from collections import OrderedDict
from operator import itemgetter
from src.db_handler import DbHandler
import csv


db_path = "data_GH_projects/databases/result.db"
table_res = "result"
table_proj = "projects"
db_handler = DbHandler()
db_conn_source = db_handler.create_connection(db_path)

query = "SELECT link_bpmn_file FROM " + table_res + ", " + table_proj + \
        " WHERE " + table_res + ".login=" + table_proj + ".login AND " + \
                    table_res + ".project_name=" + table_proj + ".project_name AND " + \
                    table_proj + ".is_deleted=0;"

links_to_files = db_handler.execute_query(db_conn_source, query, True)

typ_dict = {}
for link in links_to_files:
    extension_ele = link[0].rsplit(".", 1)[1].lower()
    if extension_ele not in typ_dict:
        typ_dict[extension_ele] = 1
    else:
        typ_dict[extension_ele] = typ_dict[extension_ele] + 1
size = len(links_to_files)
typ_dict = OrderedDict(sorted(typ_dict.items(), key=itemgetter(1), reverse=True))

image_list = ["png", "gif", "jpeg", "jpg", "svg", "pdf"]
bpmn_list = ["bpmn", "xml", "bpmn2", "bpmn2d", "bpmn20"]

grouped_typ_dict = {"image": 0, "bpmn": 0, "other": 0}

for key, value in typ_dict.items():
    if key in image_list:
        grouped_typ_dict["image"] = grouped_typ_dict["image"] + value

"""
for link in links_to_files:
    extension_ele = link[0].rsplit(".", 1)[1].lower()
    if extension_ele in bpmn_list:
        

with open('statistics/csv_files/extensions_of_files.csv', mode='w+', newline='') as csv_file:
    f_writer = csv.writer(csv_file, delimiter=';', quotechar='"')# quoting=csv.QUOTE_MINIMAL)
    f_writer.writerow([" ", "Dateiendung", "Anzahl", "Prozentsatz"])

    i = 0
    other = 0
    for key, value in typ_dict.items():
        if (value * 100) / size > 1:
            i = i + 1
            f_writer.writerow([i, str(key), str(value), round((value * 100) / size, 4)])
        else:
            other = other + value
    i = i + 1
    f_writer.writerow([i, "andere", str(other), round((other * 100) / size, 4)])

"""

