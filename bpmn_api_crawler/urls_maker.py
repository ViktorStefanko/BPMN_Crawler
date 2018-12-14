import json
import os.path

START = "https://raw.githubusercontent.com/"


class UrlsMaker:

    def hits_to_urls(self, hits_file, urls_file, default_dir):
        with open(hits_file, 'r') as file:
            line_list = file.readlines()

        for line in line_list:
            if "KeyError" in line:
                continue
            try:
                path, blob = line[:-1].split(" https://api.github.com/")
            except ValueError:
                continue
            blob_list = blob.split('/')
            username = blob_list[1]
            repo = blob_list[2]
            branch = self.obtain_branch(username, repo, default_dir)
            if not branch:
                continue
            total = START + username + "/" + repo + "/" + branch + "/" + path
            with open(urls_file, 'a+', encoding='utf-8') as outfile:
                outfile.write(total + "\n")
            print(total)

    def obtain_branch(self, username, repo, default_dir):
        file_path = default_dir + "/" + username + "/" + username + "__" + repo + ".json"
        if os.path.isfile(file_path):
            with open(file_path) as data_file:
                data = json.load(data_file)
                try:
                    return data["default_branch"]
                except KeyError:
                    print("ERROR:", file_path)
                    return 0

        return "master"
