import sqlite3
import datetime
import time


class DbHandler:

    def create_database(self, db_name):
        """ Create a SQLite database """
        if self.create_connection(db_name):
            return True
        else:
            return False

    def create_connection(self, db_path):
        """ Create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(db_path)
            return conn
        except sqlite3.Error as e:
            print(e)
            return None

    def execute_query(self, conn, query, is_select):
        """
        Query the table_result_projects
        :param conn: the Connection object
        :return: result
        """

        cursor = conn.cursor()
        result = True
        try:
            try:
                print(query)
                cursor.execute(query)
                if is_select:
                    result = cursor.fetchall()
                else:
                    conn.commit()
            except sqlite3.Error as e:
                if "UNIQUE" in e.args[0]:
                    print(e)
                else:
                    if e.__str__() == "database is locked":
                        print("Database is locked. Sleep 0.3 sec. and try again")
                        time.sleep(0.3)
                        self.execute_query(conn, query, is_select)
                    else:
                        print(e)
                        result = False
            except:
                print("Exception in DB: " + query)
                result = False
        finally:
            return result
