import os
from datetime import datetime
from utils import *


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


def compare():
    getUsers()
    username = input("Enter the Instagram username you want to compare: ")

    getDates(username)
    date = input("Enter the date you want to compare: ")
    
    following = load(username,date, f'{username}_following.txt')
    followers = load(username,date, f'{username}_followers.txt')

    if followers and following:
        followers_not_following = followers.difference(following)
        following_not_followers = following.difference(followers)

        # print(f"List of followers than you don't follow back: \n{followers_not_following}")
        write(username, date, 'followers_not_following.txt',followers_not_following)
        # print(f"List of people you follow but don't follow you back: \n{following_not_followers}")
        write(username, date, 'following_not_followers.txt', following_not_followers)


if __name__ == '__main__':
    compare()
