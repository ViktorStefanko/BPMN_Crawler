from src.db_handler import DbHandler

# Paths to the databases
# Paths to the databases
db_dir = "database"
db_source = "source.db"
db_source_path = db_dir + "/" + db_source
db_result = "result.db"
db_result_path = db_dir + "/" + db_result

# Create (if not exists) database and tables: log_repos and projects_bpmn
db_handler = DbHandler()
db_handler.create_db(db_dir, db_source)
db_handler.create_db(db_dir, db_result)
conn_source = db_handler.create_connection(db_source_path)
create_log_repos = """CREATE TABLE IF NOT EXISTS log_repos(
                                        id INTEGER NOT NULL PRIMARY KEY,     
                                        login TEXT NOT NULL, 
                                        name TEXT NOT NULL
                                        );"""
db_handler.execute_query(conn_source, create_log_repos, False)

conn_result = db_handler.create_connection(db_result_path)
create_projects_bpmn = """CREATE TABLE IF NOT EXISTS projects_bpmn(
                                        login TEXT NOT NULL,
                                        project_name TEXT NOT NULL,
                                        link_bpmn_file TEXT PRIMARY KEY
                                        );"""

db_handler.execute_query(conn_result, create_projects_bpmn, False)

# Import csv to log_repos table
csv_file = "login_repos_csv.csv"
db_handler.import_scv(csv_file, conn_source, "log_repos")

query = "SELECT * FROM log_repos;"
print(db_handler.execute_query(conn_source, query, True))
