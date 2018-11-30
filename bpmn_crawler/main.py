from bpmn_crawler.crawler import Crawler
from bpmn_crawler import validator
import MySQLdb
import os


db = MySQLdb.connect(host="localhost", user="root", passwd="vo37puh", db="ghtorrent")
cursor = db.cursor()
query = "SELECT java_projects.login, java_projects.name FROM java_projects;"
cursor.execute(query)
# repo_list is a list of (username, repository_name) tuples
repo_list = cursor.fetchall()
db.close()

store_dir = os.getcwd() + "\\store"
if not os.path.exists(store_dir):
    os.makedirs(store_dir)

store_file = os.getcwd() + "\\result.txt"
if not os.path.exists(store_file):
    f = open(store_file, "w+")
    f.close()

target_file = [".bpmn", ".xml"]
Crawler.traverse_all_repositories(repo_list, store_dir, store_file, target_file)


#print(check())
#validator.validate("hello.bpmn", "BPMN20.xsd")
