from bpmn_api_crawler.db_handler import DbHandler
from bpmn_api_crawler.api_rep_crawler import RepCrawler
from bpmn_api_crawler.api_tree_crawler import TreeCrawler


BPMN_KEY_WORDS = ["http://www.omg.org/spec/BPMN/20100524/MODEL", "bpmn"]
GH_KEY = "client_id=ecde69e021a6a9361e5d&client_secret=0a07515f3d78268c89dea9d25baad5c195216945"
db_handler = DbHandler()

print("Make tree: \n")
query = "SELECT login_and_project_name.login, login_and_project_name.name FROM login_and_project_name where login_and_project_name.id BETWEEN 1400 AND 2400;"
#query = "SELECT login, name FROM example_projects"
rep_crawler = RepCrawler()
# repo_list is a list of (username, repository_name) tuples
repo_list = db_handler.connect_db_run_query(query)
master_dir = rep_crawler.make_dir("master")
default_dir = rep_crawler.make_dir("default")
trees_dir = rep_crawler.make_dir("trees")
rep_crawler.traverse_gh_repositories(repo_list, master_dir, default_dir, trees_dir, GH_KEY)

print("Fill hits_file: \n")
tree_crawler = TreeCrawler()
trees_repo_list = tree_crawler.get_repo_list(trees_dir)
tree_crawler.search_files(trees_repo_list, trees_dir, default_dir)
