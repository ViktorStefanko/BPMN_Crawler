from bpmn_crawler.crawler import Crawler
import MySQLdb
import os
import requests
import json
"""
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
if not os.path.isfile(store_txt_file):
    f = open(store_txt_file, "w+")
    f.close()

target_file = [".bpmn", ".xml"]
if __name__ == '__main__':
    Crawler.traverse_all_repositories(repo_list, store_dir, store_txt_file, db_cursor, target_file)

db.commit()
db.close()

um = "https://raw.githubusercontent.com/ViktorStefanko/BPMN_Crawler/master/bpmn_crawler/api_rep_crawler.py"
um2 = "https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/lib/directories.zsh"

r = requests.get(um2)
    #print(r.json())
    print(r.content)
"""

um2 = "https://api.github.com/users/whatever?client_id=ecde69e021a6a9361e5d&client_secret=0a07515f3d78268c89dea9d25baad5c195216945"
data = requests.get(um2).json()
print(data)
try:
    repo = ("ViktorStefanko", "BPMN_Crawler")
    directory = "store/" + repo[0]
    if not os.path.isdir(directory):
        os.mkdir(directory)
    f = directory + "/" + repo[1] + ".json"
    with open(f, 'w+', encoding='utf-8') as outfile:
        json.dump(data, outfile)

    #r = requests.get(um2)
    #print(r.json())
    #print(r.content)
except IOError:
    print("IOERROR: " + um2)
"""
#user_rep = [["p-otto", "Armadillo"], ["ryukinkou", "BPMN2TranslateProgram"], ["LulzAreGiven", "IGT_BPMN"]]

#store_json_file = "res.json"
#target_str = "http://www.omg.org/spec/BPMN/20100524/MODEL"
#ApiCodeCrawler.traverse_user_rep(repo_list, store_dir, store_json_file, db_cursor, target_str)
"""

