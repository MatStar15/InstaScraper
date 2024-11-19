import os
from compare import load, write;

IGNORE = ['__pycache__','.git', '.vscode' ]

def getDates(username): #FIXME: for some reason does not recognizes direcotries anymore
    path =  "./" + username
    # print("listdir: " ,os.listdir(path))
            
    dates = ([name for name in os.listdir(f"./{username}") if (os.path.isdir(f"./{name}") or not name.endswith(".txt"))])
    print("avaliable dates: (as day month year)\n", dates)
    return dates

def getUsers():
    users = ([name for name in os.listdir(".") if( os.path.isdir(name) and name not in IGNORE)])
    print("avaliable users:\n", users)
    return users


def getInput():
    users = getUsers()
    while True:
        username = input("\nEnter the Instagram username you want to compare: ")
        if username not in users:
            print("Invalid username, choose another user")
            continue
        dates = getDates(username)
        if len(dates) < 2:
            print("Not enough dates to compare, choose another user")
            continue
        else:
            break
    while True:
        print("\n **NOTE**: Second date should be later than the first date!!! \n")
        date1 = input("Enter the first date to compare: ")
        date2 = input("Enter the second date to compare: ")
        if date1 not in dates or date2 not in dates:
            print("Invalid date, choose another date")
            continue
        if date1 == date2:
            print("Dates are the same, choose another date")
            continue
        else:
            break
    return username, date1, date2
            
def timeCompare(username, date1, date2):
    following1 = load(username, date1, f'{username}_following.txt')
    followers1 = load(username, date1, f'{username}_followers.txt')
    following2 = load(username, date2, f'{username}_following.txt')
    followers2 = load(username, date2, f'{username}_followers.txt')

    if followers1 and following1 and followers2 and following2:
        gained_followers = followers2.difference(followers1)
        lost_followers = followers1.difference(followers2)
        started_following = following2.difference(following1)
        stopped_following = following1.difference(following2)

        write(username, date2, f'{date1}_gained_followers.txt', gained_followers)
        write(username, date2, f'{date1}_lost_followers.txt', lost_followers)
        write(username, date2, f'{date1}_started_following.txt', started_following)
        write(username, date2, f'{date1}_stopped_following.txt', stopped_following)
    else:
        print("Error loading files")


def main():
    timeCompare(*getInput()) # username, date1, date2 unpacked arguments from the list returned by getInput()


if __name__ == '__main__':
    main()