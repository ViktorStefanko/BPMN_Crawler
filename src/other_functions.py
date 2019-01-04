import os
import subprocess


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
