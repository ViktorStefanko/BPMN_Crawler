import requests
import json
import os
import time
import datetime


class RepCrawler:
    REQUEST_LIMIT = 0
    RESET_TIME = 0
    REQUEST_COUNTER = 0
    GITHUB_API = "https://api.github.com/repos/"

    def __init__(self, gh_key):
        self.URL_LIMIT = 'https://api.github.com/rate_limit?' + gh_key

    def traverse_gh_repositories(self, repo_list, master_dir, default_dir, trees_dir, github_key):
        self.REQUEST_COUNTER = 0
        self.set_limit()
        already_list = os.listdir(master_dir)
        for repo in repo_list:
            if repo[0] in already_list:
                repo_l = os.listdir(master_dir + "/" + repo[0])
                if repo[0] + "__" + repo[1] + ".json" in repo_l:
                    continue
            if not self.get_json(repo, master_dir, github_key, "/branches/master"):
                continue
            sha_hash = self.read_json(repo, master_dir, ["commit", "commit", "tree", "sha"])

            if not sha_hash:
                print("Master branch not found: " + repo[0] + " " + repo[1])
                if not self.get_json(repo, default_dir, github_key):
                    continue
                default = self.read_json(repo, default_dir, ["default_branch"])

                if not default:
                    print("No default branch found: " + repo[0] + " " + repo[1])
                    continue
                if not self.get_json(repo, master_dir, github_key, "/branches/" + str(default)):
                    continue
                sha_hash = self.read_json(repo, master_dir, ["commit", "commit", "tree", "sha"])

                if not sha_hash:
                    print("Default branch not found: " + repo[0] + " " + repo[1])
                    continue
            if not self.get_json(repo, trees_dir, github_key, "/git/trees/" + str(sha_hash) + "?recursive=1"):
                continue

    def set_limit(self):
        data = requests.get(self.URL_LIMIT).json()
        to_wait = 2
        try:
            rate = data["rate"]
            self.REQUEST_LIMIT = int(rate["remaining"])
            self.RESET_TIME = int(rate["reset"])
            print("REQUEST_LIMIT: " + str(self.REQUEST_LIMIT))
            print("RESET_TIME: " + datetime.datetime.fromtimestamp(self.RESET_TIME).strftime('%Y-%m-%d %H:%M:%S'))
        except:
            print("Exception in set_limit()")
            time.sleep(to_wait + 60)
            self.set_limit()

    def get_json(self, repo, directory, github_key, url_append=""):
        if self.REQUEST_COUNTER % 100 == 0:
            print("REQUEST_COUNTER: " + str(self.REQUEST_COUNTER))
            self.set_limit()
            self.REQUEST_COUNTER = 0

        while self.REQUEST_COUNTER > self.REQUEST_LIMIT - 10:
            time_diff = self.RESET_TIME - int(time.time())
            if time_diff > 0:
                print("\nCome to close to the request limit!!!\n")
                print("REQUEST_LIMIT: " + str(self.REQUEST_LIMIT))
                print("REQUEST_COUNTER: " + str(self.REQUEST_COUNTER))
                print("RESET_TIME: " + datetime.datetime.fromtimestamp(self.RESET_TIME).strftime('%Y-%m-%d %H:%M:%S'))
                print("Need to sleep: " + str((time_diff + 60) / 60) + " min")
                time.sleep(time_diff + 60)
            self.set_limit()
            self.REQUEST_COUNTER = 0

        """
        Given the repo tuple (username, repository_name)
        and the directory to store the json
        it performs a query to the repos GitHub v3 API

        url_append offers the possibility to append something to the call
        """
        url = self.GITHUB_API + repo[0] + "/" + repo[1] + url_append
        if "?" in url_append:
            url = url + "&" + github_key
        else:
            url = url + "?" + github_key

        try:
            self.REQUEST_COUNTER = self.REQUEST_COUNTER + 1
            data = requests.get(url).json()
            user_dir = directory + "/" + repo[0]
            if not os.path.isdir(user_dir):
                os.mkdir(user_dir)
            f = user_dir + "/" + repo[0] + "__" + repo[1] + ".json"
            with open(f, 'w+', encoding='utf-8') as outfile:
                json.dump(data, outfile)
        except IOError:
            print("IOERROR: " + str(url))
            return 0
        return 1

    def read_json(self, repo, directory, lookup_list):
        """
        Given the repo tuple (username, repository_name)
        the directory where the json has been stored
        it looks up for a given value in the JSON (given as a list)
        and returns its value
        """
        with open(directory + "/" + repo[0] + "/" + repo[0] + "__" + repo[1] + ".json") as data_file:
            data = json.load(data_file)

        try:
            return self.lookup(data, *lookup_list)
        except KeyError:
            return 0

    def lookup(self, dic, key, *keys):
        """
        Given the dictionary dic, it provides the value with the given key(s)
        From StackOverflow: http://stackoverflow.com/a/11701539

        For instance, to obtain data["commit"]["commit"]["tree",]["sha"]
        you should call:
        lookup(data, ["commit", "commit", "tree", "sha"])
        """
        if keys:
            return self.lookup(dic.get(key, {}), *keys)
        return dic.get(key)
