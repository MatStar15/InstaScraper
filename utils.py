import os

IGNORE = ['__pycache__','.git', '.vscode', '.idea' ] #TODO: remove in release?
#TODO: Put all user data in a Users folder

def load(username, date, file_name):
    file_path = os.path.join(username, date, file_name)
    if not os.path.exists(file_path):
        print(f"[Error] - {file_path} does not exist")
        return None

    users = set()
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            users.add(line.strip(' \n'))
    return users

def write(user, date, file_name, userlist):
    date_folder = os.path.join(user, date)
    if not os.path.exists(date_folder):
        os.makedirs(date_folder)
    file_path = os.path.join(user, date, file_name)
    with open(file_path, 'w') as file:
        file.write("\n".join(userlist))
        print(f"[Info] - saving {file_path}")

def getDates(username):
    path = "./" + username
    # print("listdir: " ,os.listdir(path))

    dates = (
    [name for name in os.listdir(f"./{username}") if (os.path.isdir(f"./{name}") or not name.endswith(".txt"))])
    print("avaliable dates: (as day month year)\n", dates)
    return dates


def getUsers():
    users = ([name for name in os.listdir(".") if (os.path.isdir(name) and name not in IGNORE)])
    print("avaliable users:\n", users)
    return users
