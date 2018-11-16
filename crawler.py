import subprocess
import os
import shutil


# Run over entire GH users and search for some files in their repositories
def traverse_all_users(github, store_f, target_f):
    for user in github.all_users():
        for rep in github.repositories_by(user):
            rep = str(rep)
            folder = clone_repository(rep)
            if folder is not None:
                find_files(folder, store_f, target_f)
                shutil.rmtree(folder, ignore_errors=True)


# Clone a GH repository
def clone_repository(repository):
    cmd = "git clone https://github.com/" + repository
    pipe = subprocess.Popen(cmd, shell=True)
    pipe.wait()
    folder = os.path.basename(repository)
    if os.path.exists(folder):
        return folder
    return None


# Find files and store their paths to the text file
def find_files(root_dir, store_f, target_f):
    f = open(store_f, "a+")
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(target_f):
                f.write(str(os.path.join(root, file)) + "\n")
    f.close()

