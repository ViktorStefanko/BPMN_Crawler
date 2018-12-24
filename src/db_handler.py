import os
import sqlite3
from sqlite3 import Error


class DbHandler:

    def create_db(self, db_dir, db_name):
        if not os.path.isdir(db_dir):
            os.mkdir(db_dir)
        return self.create_connection(db_dir + "/" + db_name)

    def create_connection(self, db_path):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(db_path)
            return conn
        except Error as e:
            print(e)
            return None

    def execute_query(self, conn, query, is_select):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """

        cursor = conn.cursor()
        result = None
        try:
            try:
                cursor.execute(query)
                if is_select:
                    result = cursor.fetchall()
                else:
                    conn.commit()
            except:
                print("Exception in DB!")
                return None
        finally:
            return result
