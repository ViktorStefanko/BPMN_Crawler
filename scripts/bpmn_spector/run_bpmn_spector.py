from scripts.gh_api_crawler.db_handler import DbHandler
import subprocess
import xmltodict
import os


class ConstraintsChecker:

    def __init__(self):
        self.db_path = "databases/ghbpmn.db"
        self.bpmn_spector_path = "scripts/bpmn_spector/BPMNspector-fat-1.1.0.jar"
        self.all_files_unfixed = "data_GH_projects/all_files_fixed"
        self.all_files_fixed = "data_GH_projects/all_files"
        self.reports_path_unfixed = "reports_unfixed"
        self.reports_path_fixed = "reports_fixed"
        self.table_res_xml = "result_xml_original"
        self.db_handler = DbHandler()
        self.db_conn = self.db_handler.create_connection(self.db_path)

    def create_reports_unfixed(self):
        query = "SELECT path_copy_file FROM " + self.table_res_xml + \
                 " WHERE valid is null;"
        names_list = self.db_handler.execute_query(self.db_conn, query, True)

        for bpmn_file in names_list:
            bpmn_file_path = self.all_files_unfixed + "/" + bpmn_file[0]
            if os.path.exists(bpmn_file_path):
                cmd = "java --add-modules java.xml.bind -jar " + self.bpmn_spector_path + " " + \
                      bpmn_file_path + " -r XML"
                pipe = subprocess.Popen(cmd, shell=True)
                pipe.wait()
            else:
                print("Path doesn't exist: " + str(bpmn_file_path))

    def create_reports_fixed(self):
        query = "SELECT path_copy_file FROM " + self.table_res_xml + \
                 " WHERE valid=0 and valid_after_repairing is null;"
        names_list = self.db_handler.execute_query(self.db_conn, query, True)

        for bpmn_file in names_list:
            if ".xml" in bpmn_file[0]:
                f_new = bpmn_file[0].split(".xml")[0] + ".bpmn"
                bpmn_file_path = self.all_files_fixed + "/fixed_" + f_new
            else:
                bpmn_file_path = self.all_files_fixed + "/fixed_" + bpmn_file[0]

            if os.path.exists(bpmn_file_path):
                cmd = "java --add-modules java.xml.bind -jar " + self.bpmn_spector_path + " " + \
                      bpmn_file_path + " -r XML"
                pipe = subprocess.Popen(cmd, shell=True)
                pipe.wait()
            else:
                print("Path doesn't exist: " + str(bpmn_file_path))

    def add_constraints_unfixed(self):
        reports_list = os.listdir(self.reports_path_unfixed)
        query = "SELECT path_copy_file FROM " + self.table_res_xml + " WHERE valid IS NULL);"
        names_list = self.db_handler.execute_query(self.db_conn, query, True)

        for file_xmll in names_list:
            file_xml = file_xmll[0] + "_validation_result.xml"
            if file_xml in reports_list:
                full_path = self.reports_path_unfixed + "/" + file_xml
                if os.path.isfile(full_path):
                    query1 = "SELECT path_file FROM " + self.table_res_xml +\
                             " WHERE path_copy_file='" + file_xml.split("_validation_result.xml")[0] + "';"
                    bpmn_path_in_db = self.db_handler.execute_query(self.db_conn, query1, True)[0][0]

                    with open(full_path, 'r') as myfile:
                        file_dict = xmltodict.parse(myfile.read())
                        try:
                            is_valid = 0 if file_dict['validationResult']['valid'] == 'false' else 1
                            if is_valid:
                                query3 = 'UPDATE ' + self.table_res_xml +\
                                         ' SET valid=' + str(is_valid) + \
                                         ' WHERE path_file="' + bpmn_path_in_db + '";'
                                self.db_handler.execute_query(self.db_conn, query3, False)
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

                                query3 = 'UPDATE ' + self.table_res_xml +\
                                         ' SET valid=' + str(is_valid) + ', constraints_list="' + \
                                         str(constraint_dict) + '" WHERE path_file="' + bpmn_path_in_db + '";'
                                self.db_handler.execute_query(self.db_conn, query3, False)
                        except:
                            print("Exception: " + str(full_path))

    def add_constraints_fixed(self):
        reports_list = os.listdir(self.reports_path_fixed)
        query = "SELECT path_copy_file FROM " + self.table_res_xml + ";"
        names_list = self.db_handler.execute_query(self.db_conn, query, True)

        for file_xmll in names_list:
            file_xml = "fixed_" + file_xmll[0] + "_validation_result.xml"
            full_path = self.reports_path_unfixed + "/" + file_xml
            if not os.path.exists(full_path):
                file_xml = "fixed_" + str(file_xmll[0]).split(".xml")[0] + ".bpmn" + "_validation_result.xml"
                full_path = self.reports_path_unfixed + "/" + file_xml
                if not os.path.exists(full_path):
                    continue

            if file_xml in reports_list:
                if os.path.isfile(full_path):
                    query2 = "SELECT path_file FROM " + self.table_res_xml + \
                             " WHERE path_copy_file='" + file_xmll[0] + "';"
                    bpmn_path_in_db = self.db_handler.execute_query(self.db_conn, query2, True)[0][0]

                    with open(full_path, 'r') as myfile:
                        file_dict = xmltodict.parse(myfile.read())
                        try:
                            is_valid = 0 if file_dict['validationResult']['valid'] == 'false' else 1
                            if is_valid:
                                query3 = 'UPDATE result_xml SET valid_after_repairing=' + str(is_valid) + \
                                         ' WHERE path_file="' + bpmn_path_in_db + '";'
                                self.db_handler.execute_query(self.db_conn, query3, False)
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

                                query3 = 'UPDATE ' + self.table_res_xml +\
                                         ' SET valid_after_repairing=' + str(is_valid) +\
                                         ', constraints_list_after_repairing="' + str(constraint_dict) + \
                                         '" WHERE path_file="' + bpmn_path_in_db + '";'
                                self.db_handler.execute_query(self.db_conn, query3, False)
                        except:
                            print("Exception: " + str(full_path))
