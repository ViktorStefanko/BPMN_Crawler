from src_bpmn_crawler.db_handler import DbHandler
import os.path
import csv


def get_files_type(extensions_dict):
    image_list = ["png", "gif", "jpeg", "jpg", "svg", "pdf"]
    bpmn_list = ["bpmn", "xml", "bpmn2", "bpmn2d", "bpmn20"]

    grouped_typ_dict = {"Bild": 0, "xml": 0, "Andere": 0}

    for key, value in extensions_dict.items():
        if key in image_list:
            grouped_typ_dict["Bild"] = grouped_typ_dict["Bild"] + value
        elif key in bpmn_list:
            grouped_typ_dict["xml"] = grouped_typ_dict["xml"] + value
        else:
            grouped_typ_dict["Andere"] = grouped_typ_dict["Andere"] + value
    return grouped_typ_dict


def write_all_types_to_csv(types_dict, numb_of_files, csv_file='scripts/statistics/csv_files/types_of_all_files.csv'):
    with open(csv_file, mode='w+', newline='') as csv_file:
        f_writer = csv.writer(csv_file, delimiter=';', quotechar='"')  # quoting=csv.QUOTE_MINIMAL)
        f_writer.writerow([" ", "Dateityp", "Anzahl", "Prozentsatz"])

        i = 1
        for key, value in types_dict.items():
            f_writer.writerow([i, str(key), str(value), round((value * 100) / numb_of_files, 4)])


def find_bpmn_files_from_xml():
    bpmn_schema = 'http://www.omg.org/spec/BPMN/20100524/MODEL'

    db_path = "data_GH_projects/databases/result.db"
    table_res = "result"
    table_bpmn = "result_bpmn"
    db_handler = DbHandler()
    db_conn = db_handler.create_connection(db_path)
    query = "SELECT login, project_name, path_bpmn_file FROM " + table_res + \
            " WHERE path_bpmn_file LIKE '%.bpmn'" + \
            " OR path_bpmn_file LIKE '%.xml'" + \
            " OR path_bpmn_file LIKE '%.bpmn2'" + \
            " OR path_bpmn_file LIKE '%.bpmn2d'" + \
            " OR path_bpmn_file LIKE '%.bpmn20';"
    all_paths = db_handler.execute_query(db_conn, query, True)

    for (login, project_name, rel_file_path) in all_paths:
        file_path = os.path.join("data_GH_projects\projects_without_git", rel_file_path)
        if os.path.exists(file_path):
            if open(file_path, encoding="utf8", errors='ignore').read().find(bpmn_schema) != -1:
                query = "INSERT INTO " + table_bpmn + " VALUES ('" + rel_file_path + "');"
                db_handler.execute_query(db_conn, query, False)
        else:
            print("Error, path doesn't exist: " + file_path)


def find_image_files():
    db_path = "data_GH_projects/databases/result.db"
    table_res = "result"
    table_images = "result_images"
    db_handler = DbHandler()
    db_conn = db_handler.create_connection(db_path)
    query = "INSERT INTO " + table_images + " SELECT path_bpmn_file FROM " + table_res + \
            " WHERE path_bpmn_file LIKE '%.png'" + \
            " OR path_bpmn_file LIKE '%.gif'" + \
            " OR path_bpmn_file LIKE '%.jpeg'" + \
            " OR path_bpmn_file LIKE '%.jpg'" + \
            " OR path_bpmn_file LIKE '%.pdf';"
    db_handler.execute_query(db_conn, query, False)
