import os
from datetime import datetime


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

# def write(users, file_name):
#     date_folder = datetime.now().strftime("%Y-%m-%d")
#     user_folder = os.path.join(date_folder, file_name.split('_')[0])
#     if not os.path.exists(user_folder):
#         os.makedirs(user_folder)
#     file_path = os.path.join(user_folder, file_name)
#     with open(file_path, 'w') as file:
#         file.write("\n".join(users) + "\n")
#         print(f"[Info] - saving {file_path}")

def write(user, date, file_name, userlist):
    date_folder = os.path.join(user, date)
    if not os.path.exists(date_folder):
        os.makedirs(date_folder)
    file_path = os.path.join(user, date, file_name)
    with open(file_path, 'w') as file:
        file.write("\n".join(userlist))
        print(f"[Info] - saving {file_path}")


def compare():
    username = input("Enter the Instagram username you want to compare: ")

    
    following = load(username, f'{username}_following.txt')
    followers = load(username, f'{username}_followers.txt')

    if followers and following:
        followers_not_following = followers.difference(following)
        following_not_followers = following.difference(followers)

        # print(f"List of followers than you don't follow back: \n{followers_not_following}")
        write(followers_not_following, f'{username}_followers_not_following.txt')
        # print(f"List of people you follow but don't follow you back: \n{following_not_followers}")
        write(following_not_followers, f'{username}_following_not_followers.txt')


if __name__ == '__main__':
    compare()
