from pydriller import RepositoryMining
import MySQLdb

store_f = "result.txt"
target_f = ".png"

db = MySQLdb.connect(host="localhost", user="root", passwd="vo37puh", db="ghtorrent_restore")
cursor = db.cursor()
query = "SELECT * FROM login_and_proj_name;"
cursor.execute(query)

# repo_list is a list of (username, repository_name) tuples

repo_list = cursor.fetchall()
db.close()

urls = []
for i in repo_list[0:2]:
    urls.append("git clone https://github.com/" + str(i[0]) + "/" + str(i[1]) + ".git")

for commit in RepositoryMining(path_to_repo=urls).traverse_commits():
    print("Project {}, commit {}, date {}".format(commit.project_path, commit.hash, commit.author_date))
