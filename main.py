from compare import *
from timecompare import *
from scrape import *

def main():
    print("Welcome to InstaScraper!")
    print("Choose an option:")
    print("0. Scrap Instagram data")
    print("1. Compare followers and following")
    print("2. Compare followers and following over time")
    option = input("Enter the number of the option you want to choose: ")
    if option == '0':
        scrape()
    if option == '1':
        compare()
    elif option == '2':
        username, date1, date2 = getInput()
        timeCompare(username, date1, date2)
    else:
        print("Invalid option")
        return

if __name__ == '__main__':
    main()