import requests
import json
import time


# Benutzen mit git clone zusammen!!!

class ApiCodeCrawler:

    @staticmethod
    def traverse_user_rep(user_rep_list, store_dir, store_file, db_cursor, str_to_match):
        i = 0
        for user_rep in user_rep_list:
            if 10 == i:
                time.sleep(50)
                i = 0
            i += 1
            data = ApiCodeCrawler.get_json(user_rep[0], user_rep[1], str_to_match).json()
            if not data or data.get('errors'):
                try:
                    sql = "INSERT INTO projects_bpmn (login, project_name, language, stored_id) VALUES (%s, %s, %s, %s)"
                    val = (user_rep[0], user_rep[1], user_rep[2], user_rep[3])
                    db_cursor.execute(sql, val)
                except:
                    print("Error!")
                rep_path = store_dir + "\\" + store_file
                with open(rep_path, 'a+', encoding='utf-8') as outfile:
                    json.dump(data, outfile)


    @staticmethod
    def get_json(user, repository, str_to_match):
        url = "https://api.github.com/search/code?q=" + str(str_to_match) +"+in:file+user:" + str(user) + "+repo:" + str(repository) + "&client_id=ecde69e021a6a9361e5d&client_secret=0a07515f3d78268c89dea9d25baad5c195216945"
        print(url)
        try:
            r = requests.get(url)
            print(r.json())
            return(r)
        except IOError:
            print("IOERROR: " + url)
            return {}

#curl -i 'https://api.github.com/users/whatever?client_id=ecde69e021a6a9361e5d&client_secret=0a07515f3d78268c89dea9d25baad5c195216945'