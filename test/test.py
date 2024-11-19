import unittest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from compare import *
from timecompare import *


class TestWriteLoad(unittest.TestCase):
    def test_write_load(self):
        test_users = {'rat', 'cat', 'bat', 'mat'}
        write('rat', '2021-08-01', 'rat_followers.txt', test_users)
        self.assertEqual(load('rat', '2021-08-01', 'rat_followers.txt'), test_users)

class TestTimeCompare(unittest.TestCase):
    def test_time_compare(self):
        write('rat', '2021-08-01', 'rat_followers.txt', {'a', 'b', 'c', 'd', 'lost'})
        write('rat', '2021-08-01', 'rat_following.txt', {'a', 'b', 'c', 'd', 'stopped'})
        write('rat', '2021-08-02', 'rat_followers.txt', {'a', 'b', 'gained', 'c', 'd'})
        write('rat', '2021-08-02', 'rat_following.txt', {'a', 'b', 'started', 'c', 'd'})

        timeCompare('rat', '2021-08-01', '2021-08-02')

        self.assertEqual(load('rat', '2021-08-02', '2021-08-01_lost_followers.txt'), {'lost'})
        self.assertEqual(load('rat', '2021-08-02', '2021-08-01_gained_followers.txt'), {'gained'})
        self.assertEqual(load('rat', '2021-08-02', '2021-08-01_stopped_following.txt'), {'stopped'})
        self.assertEqual(load('rat', '2021-08-02', '2021-08-01_started_following.txt'), {'started'})

if __name__ == '__main__':
    unittest.main()