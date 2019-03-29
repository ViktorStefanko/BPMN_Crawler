from src_bpmn_crawler.db_handler import DbHandler
import requests
import geotext

db_path = "data_GH_projects/databases/result.db"
table = "projects"
GH_KEY = "client_id=ecde69e021a6a9361e5d&client_secret=0a07515f3d78268c89dea9d25baad5c195216945"
db_handler = DbHandler()
db_conn_source = db_handler.create_connection(db_path)


def get_repo_location():
    query1 = "SELECT login, project_name FROM " + table + ";"
    repo_list = db_handler.execute_query(db_conn_source, query1, True)

    for repo in repo_list[1100:]:
        print(repo)
        url1 = "https://api.github.com/repos/" + repo[0] + "/" + repo[1] + "/contributors?" + GH_KEY
        try:
            contributors_list = requests.get(url1).json()
            locations_list = []
            for contributor in contributors_list:
                url2 = "https://api.github.com/users/" + contributor['login'] + "?" + GH_KEY
                user_info = requests.get(url2).json()
                if user_info['location']:
                    if user_info['location'] not in locations_list:
                        locations_list.append(user_info['location'])
            if locations_list:
                locations = ""
                for location in locations_list:
                    if locations:
                        locations = locations + "_,_" + location
                    else:
                        locations = location
                query2 = "UPDATE " + table + " SET location='" + locations + \
                         "' WHERE login='" + repo[0] + \
                         "' AND project_name='" + repo[1] + "';"
                db_handler.execute_query(db_conn_source, query2, False)
                locations_list = []
        except:
            print("ERROR: " + str(url1))


def get_repo_location2():
    query = "SELECT login, project_name, location FROM projects WHERE location IS NOT NULL;"
    repo_list = db_handler.execute_query(db_conn_source, query, True)

    for repo in repo_list:
        countries = geotext.GeoText(repo[2]).countries
        if countries:
            countries_dict = dict()
            for country in countries:
                if country in countries_dict:
                    countries_dict[country] = countries_dict[country] + 1
                else:
                    countries_dict[country] = 1
            if len(countries_dict) == 1:
                query2 = "UPDATE " + table + " SET location_country='" + list(countries_dict.keys())[0] + \
                         "' WHERE login='" + repo[0] + \
                         "' AND project_name='" + repo[1] + "';"
                db_handler.execute_query(db_conn_source, query2, False)
            else:
                print("To many countries: " + str(countries_dict))

