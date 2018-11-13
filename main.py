from github3 import login
import stuff

# Setting user's name and password from GH increases amount of GH requests up to 5000/h
name = ""
psw = ""
gh = login(username=name, password=psw)

store_f = "result.txt"
target_f = ".png"
stuff.traverse_all_users(gh, store_f, target_f)

