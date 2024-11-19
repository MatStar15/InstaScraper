import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from compare import *
from timecompare import *

def test_compare():
    write('rat', '2021-08-01', 'rat_followers.txt', ['a', 'b', 'c', 'd', 'e'])
    print(load('rat', '2021-08-01', 'rat_followers.txt'))

def test_time_compare():
    write('rat', '2021-08-01', 'rat_followers.txt', ['a', 'b', 'c', 'd', 'lost'])
    write('rat', '2021-08-01', 'rat_following.txt', ['a', 'b', 'c', 'd', 'stopped'])
    write('rat', '2021-08-02', 'rat_followers.txt', ['a', 'b','gained' ,'c', 'd'])
    write('rat', '2021-08-02', 'rat_following.txt', ['a', 'b', 'started', 'c', 'd'])

    timeCompare('rat', '2021-08-01', '2021-08-02')

    print("[INFO] - Gained Followers: ", load('rat', '2021-08-02', '2021-08-01_gained_followers.txt'))
    print("[INFO] - Lost Followers: ",load('rat', '2021-08-02', '2021-08-01_lost_followers.txt'))
    print("[INFO] - Started Following: ",load('rat', '2021-08-02', '2021-08-01_started_following.txt'))
    print("[INFO] -Stopped Following: ",load('rat', '2021-08-02', '2021-08-01_stopped_following.txt'))
    pass

if __name__ == '__main__':
    test_compare()
    test_time_compare()