from bpmn_crawler.api_code_crawler import ApiCodeCrawler
from bpmn_crawler.crawler import Crawler
from bpmn_crawler.api_rep_crawler import ApiRepCrawler
import MySQLdb
import os

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="vo37puh",
                     db="ghtorrent")
db_cursor = db.cursor()
query = "SELECT login_and_project_name.login, login_and_project_name.name, login_and_project_name.language, login_and_project_name.ID FROM login_and_project_name where login_and_project_name.id < 31;"
db_cursor.execute(query)
# repo_list is a list of (username, repository_name, language, id) tuples
repo_list = db_cursor.fetchall()


store_dir = os.getcwd() + "\\store"
if not os.path.exists(store_dir):
    os.makedirs(store_dir)

store_txt_file = os.getcwd() + "\\result.txt"
if not os.path.exists(store_txt_file):
    f = open(store_txt_file, "w+")
    f.close()

target_file = [".bpmn", ".xml"]
if __name__ == '__main__':
    Crawler.traverse_all_repositories(repo_list, store_dir, store_txt_file, db_cursor, target_file)

db.commit()
db.close()



#user_rep = [["p-otto", "Armadillo"], ["ryukinkou", "BPMN2TranslateProgram"], ["LulzAreGiven", "IGT_BPMN"]]

#store_json_file = "res.json"
#target_str = "http://www.omg.org/spec/BPMN/20100524/MODEL"
#ApiCodeCrawler.traverse_user_rep(repo_list, store_dir, store_json_file, db_cursor, target_str)

