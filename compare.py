import os

def load(username, file_name):
    if not os.path.exists(file_name):
        print(f"[Error] - {file_name} does not exists")
        return None

    users = set()

    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            users.add(line.strip(' \n'))
        return users

    return None


def write(users, file_name):
    with open(file_name, 'a') as file:
        file.write("\n".join(users) + "\n")
        print(f"[Info] - saving {file_name}")


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