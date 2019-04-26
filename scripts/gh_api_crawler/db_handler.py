import os
import sqlite3


class DbHandler:

    def create_db(self, db_dir, db_name):
        """ Create a SQLite database """
        if not os.path.isdir(db_dir):
            os.mkdir(db_dir)
        return self.create_connection(db_dir + "/" + db_name)

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
                    print(e)
                    result = False
            except:
                print("Exception in DB: " + query)
                result = False
        finally:
            return result
