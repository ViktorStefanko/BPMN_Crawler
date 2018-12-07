import requests
import json


class ApiRepCrawler:

    @staticmethod
    def get_json(log_repo, store_dir):
        github_api = "https://api.github.com/repos/"
        url_append = "?client_id=ecde69e021a6a9361e5d&client_secret=0a07515f3d78268c89dea9d25baad5c195216945"
        url = github_api + log_repo[0] + "/" + log_repo[1] + url_append

        try:
            r = requests.get(url)
            data = r.json()
            print(data)
            try:
                store_file = store_dir + "\\" + log_repo[0] + "_" + log_repo[1] + ".json"
                with open(store_file, 'a+', encoding='utf-8') as outfile:
                    json.dump(data, outfile)
            except:
                print("ERROR: With json")

        except:
            print("ERROR: " + url)
