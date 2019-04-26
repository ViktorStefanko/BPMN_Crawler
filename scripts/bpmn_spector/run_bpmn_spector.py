from scripts.gh_api_crawler.db_handler import DbHandler
import subprocess
import xmltodict
import os
import re

bpmn_spector_path = "scripts/bpmn_spector/BPMNspector-fat-1.1.0.jar"
all_files_path = "data_GH_projects/all_files"
db_path = "data_GH_projects/databases/result.db"
table_res_bpmn = "result_bpmn"
db_handler = DbHandler()
db_conn = db_handler.create_connection(db_path)


def create_reports():
    query1 = "SELECT path_copy_bpmn_file FROM files_copy WHERE path_bpmn_file IN (SELECT path_bpmn_file FROM " +\
             table_res_bpmn + " WHERE valid IS NULL AND path_bpmn_file NOT LIKE 'themarkler/bpmrepo%');"
    bpmn_names_list = db_handler.execute_query(db_conn, query1, True)

    my_list = ["8605.xml", "9790.xml", "3330.bpmn2", "3336.bpmn2", "3343.bpmn2", "3346.bpmn2", "3347.bpmn2",
               "3354.bpmn2", "3358.bpmn2", "3360.bpmn2", "3361.bpmn2", "5810.bpmn2", "6525.bpmn", "6526.bpmn",
               "5961.bpmn", "6528.bpmn", "6529.bpmn", "6530.bpmn", "6532.bpmn", "6546.bpmn", "6547.bpmn", "6629.bpmn",
               "6631.bpmn2", "6632.bpmn", "6633.bpmn", "6634.bpmn", "6635.bpmn", "6636.bpmn", "6637.bpmn",
               "6638.bpmn", "6639.bpmn", "6642.bpmn2", "6643.bpmn", "6645.bpmn", "6647.bpmn", "6648.bpmn", "6650.bpmn",
               "6653.bpmn", "6654.bpmn", "6655.bpmn", "6656.bpmn", "6657.bpmn", "6658.bpmn", "6659.bpmn", "6661.bpmn",
               "6924.bpmn2", "7199.bpmn2"]

    for bpmn_file in bpmn_names_list:
        if bpmn_file[0] not in my_list:
            bpmn_file_path = all_files_path + "/" + bpmn_file[0]
            cmd = "java --add-modules java.xml.bind -jar " + bpmn_spector_path + " " + \
                  bpmn_file_path + " -r XML"
            pipe = subprocess.Popen(cmd, shell=True)
            pipe.wait()


def reports_to_json():
    reports_path = "reports"
    reposrts_list = os.listdir(reports_path)
    query1 = "SELECT path_copy_bpmn_file FROM files_copy WHERE path_bpmn_file IN (SELECT path_bpmn_file FROM " + \
             table_res_bpmn + " WHERE valid IS NULL);"
    bpmn_names_list = db_handler.execute_query(db_conn, query1, True)

    for file_xmll in bpmn_names_list:
        file_xml = file_xmll[0] + "_validation_result.xml"
        if file_xml in reposrts_list:
            full_path = reports_path + "/" + file_xml
            if os.path.isfile(full_path):
                query2 = "SELECT path_bpmn_file FROM files_copy WHERE path_copy_bpmn_file='" + \
                         file_xml.split("_validation_result.xml")[0] + "';"
                bpmn_path_in_db = db_handler.execute_query(db_conn, query2, True)[0][0]

                with open(full_path, 'r') as myfile:
                    file_dict = xmltodict.parse(myfile.read())
                    try:
                        is_valid = 0 if file_dict['validationResult']['valid'] == 'false' else 1
                        if is_valid:
                            query3 = 'UPDATE result_bpmn SET valid=' + str(is_valid) + \
                                     ' WHERE path_bpmn_file="' + bpmn_path_in_db + '";'
                            db_handler.execute_query(db_conn, query3, False)
                        else:
                            constraint_dict = dict()
                            if isinstance(file_dict['validationResult']['violations']['violation'], list):
                                for constraint in file_dict['validationResult']['violations']['violation']:
                                    if constraint['@constraint'] in constraint_dict:
                                        constraint_dict[constraint['@constraint']] += 1
                                    else:
                                        constraint_dict[constraint['@constraint']] = 1
                            else:
                                constraint_dict[
                                    file_dict['validationResult']['violations']['violation']['@constraint']] = 1

                            query3 = 'UPDATE result_bpmn SET valid=' + str(is_valid) + ', constraints_list="' + \
                                     str(constraint_dict) + '" WHERE path_bpmn_file="' + bpmn_path_in_db + '";'
                            db_handler.execute_query(db_conn, query3, False)
                    except:
                        print("Exception: " + str(full_path))


def check_bpmn_contains_cpecial_characters():
    query = "SELECT path_copy_bpmn_file FROM files_copy WHERE path_bpmn_file IN " \
            "(SELECT path_bpmn_file FROM result_bpmn);"
    copy_files_list = db_handler.execute_query(db_conn, query, True)

    for f in copy_files_list:
        query1 = "SELECT path_bpmn_file FROM files_copy WHERE path_copy_bpmn_file='" + \
                 f[0] + "';"
        bpmn_path_in_db = db_handler.execute_query(db_conn, query1, True)[0][0]
        file_path = "data_GH_projects/all_files/" + f[0]
        i = 0
        try:
            with open(file_path, 'r', encoding='utf-8') as my_file:
                words_list = re.findall(u'[\u4e00-\u9fff]+', my_file.read())
                if words_list:
                    i = 1
        except:
            i = 2
        query3 = 'UPDATE result_bpmn SET contains_special_character=' + str(i) + \
                 ' WHERE path_bpmn_file="' + bpmn_path_in_db + '";'
        db_handler.execute_query(db_conn, query3, False)
