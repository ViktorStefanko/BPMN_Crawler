import os
import subprocess
import requests
import time


def make_dir(my_dir):
    """ Make directory if it doesn't exist """
    if not os.path.isdir(my_dir):
        os.mkdir(my_dir)
    return my_dir


def remove_dir(my_dir):
    """ Remove directory if it exists """
    if os.path.isdir(my_dir):
        cmd = "rm -rf " + my_dir
        pipe = subprocess.Popen(cmd, shell=True)
        pipe.wait()


def get_limit(gh_key):
    url_limit = 'https://api.github.com/rate_limit?' + gh_key
    try:
        data = requests.get(url_limit).json()
        rate = data["rate"]
        return [int(rate["remaining"]), int(rate["reset"])]
    except:
        print("Exception in get_limit()")
        time.sleep(120)
        get_limit(gh_key)

