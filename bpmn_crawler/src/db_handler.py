import os
import sqlite3
from sqlite3 import Error
import csv


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

    def execute_query(self, conn, query, select):
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
                if select:
                    result = cursor.fetchall()
                else:
                    conn.commit()
            except:
                print("Exception in DB!")
                return None
        finally:
            return result

    def import_scv(self, filename, conn, table):
        filename.encode('utf-8')
        with open(filename) as f:
            reader = csv.reader(f)
            for field in reader:
                query = "INSERT INTO " + table + "(id, login, name) VALUES (" + field[0] + ", '" + field[1] + "', '" + field[2] + "');"
                self.execute_query(conn, query, False)
