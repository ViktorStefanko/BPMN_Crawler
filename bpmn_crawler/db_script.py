from src.db_handler import DbHandler

# Path to the database
db_dir = "database"
db_name = "sqliteBPMN.db"
db_path = db_dir + "\\" + db_name

# Create (if not exists) database and tables: log_repos and projects_bpmn
db_handler = DbHandler()
db_handler.create_db(db_dir, db_name)
conn = db_handler.create_connection(db_path)
create_log_repos = """CREATE TABLE IF NOT EXISTS log_repos(
                                        id INTEGER NOT NULL PRIMARY KEY,     
                                        login TEXT NOT NULL, 
                                        name TEXT NOT NULL
                                        );"""
create_projects_bpmn = """CREATE TABLE IF NOT EXISTS projects_bpmn(
                                        login TEXT NOT NULL,
                                        project_name TEXT NOT NULL,
                                        link_bpmn_file TEXT PRIMARY KEY
                                        );"""
db_handler.execute_query(conn, create_log_repos, False)
db_handler.execute_query(conn, create_projects_bpmn, False)

# Import csv to log_repos table
csv_file = "temp/login_repos_csv.csv"
db_handler.import_scv(csv_file, conn, "log_repos")

query = "SELECT * FROM log_repos;"
print(db_handler.execute_query(conn, query, True))
