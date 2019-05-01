import os
import subprocess
import requests
import time


class UsefulFunctions:

    @staticmethod
    def make_dir(my_dir):
        """ Make directory if it doesn't exist """
        if not os.path.isdir(my_dir):
            os.mkdir(my_dir)
        return my_dir

    @staticmethod
    def remove_dir(my_dir):
        """ Remove directory if it exists """
        if os.path.isdir(my_dir):
            cmd = "rm -rf " + my_dir
            pipe = subprocess.Popen(cmd, shell=True)
            pipe.wait()

    @staticmethod
    def get_limit(gh_key):
        url_limit = 'https://api.github.com/rate_limit?' + gh_key
        try:
            data = requests.get(url_limit).json()
            rate = data["rate"]
            return [int(rate["remaining"]), int(rate["reset"])]
        except:
            print("Exception in get_limit()")
            time.sleep(120)
            UsefulFunctions.get_limit(gh_key)

    # Clone a GH repository
    @staticmethod
    def clone_repository(user_name, rep_name, store_dir):
        cmd = "git clone https://github.com/" + user_name + "/" + rep_name
        pipe = subprocess.Popen(cmd, cwd=store_dir, shell=True)
        pipe.wait()
        rep_path = store_dir + "/" + rep_name
        if os.path.isdir(rep_path):
            return True
        else:
            print("Error in clone_repository")
            print(cmd)
            return False

