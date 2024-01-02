import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.common.exceptions import NoSuchElementException


def scroll_down(bot):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = bot.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(1.5)

        # Calculate new scroll height and compare with last scroll height.
        new_height = bot.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height



def save_credentials(username, password):
    with open('credentials.txt', 'w') as file:
        file.write(f"{username}\n{password}")


def load_credentials():
    print(str(os.getcwd()))
    if not os.path.exists('credentials.txt'):
        return None

    with open('credentials.txt', 'r') as file:
        lines = file.readlines()
        if len(lines) >= 2:
            return lines[0].strip(), lines[1].strip()

    return None


def prompt_credentials():
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    save_credentials(username, password)
    return username, password


def login(bot, username, password):
    bot.get('https://www.instagram.com/accounts/login/')
    time.sleep(2)

    # Check if cookies need to be accepted
    try:
        element = bot.find_element(By.XPATH, '//*[contains(text(), "Allow all cookies")]')
        element.click()
        time.sleep(2)
    except NoSuchElementException:
        print("[Info] - Instagram did not require to accept cookies this time.")
    print("[Info] - Logging in...")
    username_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    username_input.clear()
    username_input.send_keys(username)
    password_input.clear()
    password_input.send_keys(password)

    login_button = WebDriverWait(bot, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_button.click()
    time.sleep(10)


def scrape_followers(bot, username):
    bot.get(f'https://www.instagram.com/{username}/')
    time.sleep(3.5)
    WebDriverWait(bot, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/followers')]"))).click()
    time.sleep(2)
    print(f"[Info] - Scraping followers for {username}...")

    users = set()

    # prev_lenght = 0
    # repeated = False

    try:
        element = bot.find_element(By.XPATH, '//*[contains(text(), "See All Followers")]')
        element.click()
        time.sleep(2)
    except NoSuchElementException:
            print("[Info] - Instagram did not require to show all followers this time.")

    # for i in range(scrolls):
    #     ActionChains(bot).send_keys(Keys.END).perform()
    #     time.sleep(1)

    scroll_down(bot)
    followers = bot.find_elements(By.XPATH, "//a[contains(@role, 'link') and not(contains('|/|/explore/|/reels/|/direct/inbox/|', concat('|', @href, '|')))]")
    
    #remove every other entry since they all appear twice, and self (start from index 3):
    # followers = followers[3::2]
    print(f"loaded followers: {len(followers)} \n list of followers (contains duplicates): {followers} \n")

    for i in followers:
        href = i.get_attribute('href')
        if href:
            # print(f"link:{i.get_attribute('href')} of {i}")
            users.add(i.get_attribute('href').split("/")[3])
        else:
            continue
    print(f"[Info] - loaded users: {len(users)}")
    print(f"[Info] - Saving followers for {username}...")
    with open(f'{username}_followers.txt', 'a') as file:
        file.write("\n".join(users) + "\n")


def scrape():
    credentials = load_credentials()

    if credentials is None:
        username, password = prompt_credentials()
    else:
        username, password = credentials

    user = input("Enter the Instagram usernames you want to scrape (separated by commas): ").split(",")
    mode = 0
    while mode not in (1, 2, 3):
        try :
            mode = int(input("Enter what you want to scrape: \n (1) for followers \n (2) for following \n (3) for both \n"))
        except:
            mode = 0

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    #mobile_emulation = {
        # "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    
    mobile_emulation = {

   "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },

   "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",

   "clientHints": {"platform": "Android", "mobile": True} }

    options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = webdriver.Chrome(options= options)

    login(bot, username, password)

    # for user in usernames:
    user = user.strip()
    scrape_followers(bot, user, mode)

    bot.quit()


if __name__ == '__main__':
    TIMEOUT = 15
    scrape()