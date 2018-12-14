import MySQLdb


class DbHandler:

    def connect_db_run_query(self, query, select=True, host="localhost", user="root", password="vo37puh", db="ghtorrent"):
        db = MySQLdb.connect(host, user, password, db)
        cursor = db.cursor()
        result = None
        try:
            try:
                cursor.execute(query)
                if select:
                    result = cursor.fetchall()
                else:
                    db.commit()
            except (MySQLdb.Error, MySQLdb.Warning) as e:
                print(e)
                return None
            except:
                print("Exception in DB!")
                return None
        finally:
            db.close()
            return result



