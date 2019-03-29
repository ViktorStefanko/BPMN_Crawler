from src_bpmn_crawler.db_handler import DbHandler
import csv

db_path = "data_GH_projects/databases/result.db"
db_handler = DbHandler()
db_conn_source = db_handler.create_connection(db_path)


def count_bpmn_repos():
    bpmn_paths_table = "result_bpmn"
    result_table = "result"

    query = "SELECT COUNT(*) FROM (SELECT DISTINCT login, project_name FROM " + result_table + \
             " WHERE path_bpmn_file IN (" + "SELECT path_bpmn_file FROM " + bpmn_paths_table + "));"
    number_bpmn_repos = db_handler.execute_query(db_conn_source, query, True)
    return number_bpmn_repos[0][0]


def count_all_repos():
    projects_table = "projects"
    query = "SELECT COUNT(*) FROM " + projects_table + ";"
    number_repos = db_handler.execute_query(db_conn_source, query, True)
    return number_repos[0][0]


def make_csv_bpmn_repos(number_bpmn_repos, number_all_repos, csv_file_name):

    with open(csv_file_name, mode='w+', newline='') as csv_file:
        f_writer = csv.writer(csv_file, delimiter=';', quotechar='"')
        f_writer.writerow([' ', 'Anzahl bpmn-Projekte nach Schema', 'Anzahl alle bpmn-Projekte'])
        f_writer.writerow(['1', str(number_bpmn_repos), number_all_repos])
