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


FOLLOWERS_XPATH = "/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"
FOLLOING_XPATH = "/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]"
TIMEOUT = 15

def scroll_down(bot): #https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-in-dynamically-loading-webpage
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


def scroll_down_dialog(bot, what): #https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-in-dynamically-loading-webpage and https://stackoverflow.com/questions/53971506/scroll-to-the-bottom-of-a-dynamically-loading-dialog-box-in-python
    """A method for scrolling the div."""

    time.sleep(5)

    if what == "followers":
        element = f"document.evaluate(\"{FOLLOWERS_XPATH}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue"
    elif what == "following":
        element = f"document.evaluate(\"{FOLLOING_XPATH}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue"

    else:
        print("Invalid argument")
        return

    # Get scroll height.
    last_height = bot.execute_script(f"return {element}.scrollHeight")

    found = True

    while True:

        # Scroll down to the bottom.
        bot.execute_script(f"{element}.scrollTo(0, {element}.scrollHeight);")

        # Wait to load the page.
        time.sleep(0.5) #FIXME doesn't work with slow connections

        # Calculate new scroll height and compare with last scroll height.
        new_height = bot.execute_script(f"return {element}.scrollHeight")


        # print(f"new height: {new_height} last height: {last_height}")

        found = not (bot.find_elements(By.XPATH, "//*[name() = \"svg\" and @aria-label=\"Loading...\"]") == [])


        if new_height == last_height:
            if not found:
                break

        last_height = new_height
    


def save_credentials(username, password):
    with open('credentials.txt', 'w') as file:
        file.write(f"{username}\n{password}")


def load_credentials():
    # print(str(os.getcwd()))
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
    bot.get('https://business.instagram.com/')

    # Check if cookies need to be accepted
    try:
        print("[Info] - Accepting cookies...")
        element = bot.find_element(By.XPATH, '//*[@id="allow_button"]')
        element.click()
        time.sleep(3)
    except NoSuchElementException:
        print("[Info] - Instagram did not require to accept cookies this time.")
    except Exception as e:
        print(f"[Error] - {e}")


    print("[Info] - Logging in...")

    bot.get('https://www.instagram.com/accounts/login/')

    username_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    username_input.clear()
    username_input.send_keys(username)
    password_input.clear()
    password_input.send_keys(password)

    login_button = WebDriverWait(bot, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_button.click()

    time.sleep(5)
    if("https://www.instagram.com/accounts/login/two_factor" in bot.current_url):
        print("[Info] - Waiting for 2FA code...")
        while(bot.current_url != "https://www.instagram.com/"): 
            time.sleep(1) # TODO: add a way to input the 2FA code in the console so that the browser can be headless
        print("[Info] - Proceding.")

    print("[Info] - Logged in.")

    # WebDriverWait(bot, 1).until(lambda d : EC.title_is("https://www.instagram.com/#reactivated"))


def scrape_profile(bot, username, mode):
    bot.get(f'https://www.instagram.com/{username}/')
    time.sleep(2)

    match mode:
        case 1:
            subject = 'followers'
        case 2:
            subject = 'following'



    WebDriverWait(bot, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, '/{subject}')]"))).click()
    time.sleep(2)
    print(f"[Info] - Scraping {subject} for {username}...")

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
    print(f"[Info] - letting all {subject} load")
    scroll_down_dialog(bot, subject)

    print(f"[Info] - Scraping")
    elements = bot.find_elements(By.XPATH, "//a[contains(@role, 'link') and not(contains('|/|/explore/|/reels/|/direct/inbox/|', concat('|', @href, '|')))]")
    
    #remove every other entry since they all appear twice, and self (start from index 3):
    # followers = followers[3::2]
    print(f"[Info] - Loaded duplicated followers: {len(elements)} \n ") #list of {subject} (contains duplicates): {elements} \n

    for entry in elements:
        href = entry.get_attribute('href')
        if href:
            # print(f"link:{i.get_attribute('href')} of {i}")
            users.add(entry.get_attribute('href').split("/")[3])
        else:
            continue
    users = set(users)
    print(f"[Info] - Actual users: {len(users)}")
    print(f"[Info] - Saving {subject} for {username}...")
    with open(f'{username}_{subject}.txt', 'w') as file:
        file.write("\n".join(users) + "\n")


def scrape():
    credentials = load_credentials()

    if credentials is None:
        username, password = prompt_credentials()
    else:
        username, password = credentials

    user = input("Enter the Instagram username you want to scrape: ")
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

    # TODO: fix 2FA and make headless
    #options.add_argument("--headless")
    

    #mobile_emulation = {
        # "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    
    mobile_emulation = {

   "deviceMetrics": { "width": 620, "height": 1280, "pixelRatio": 1 },

   "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",

   "clientHints": {"platform": "Android", "mobile": True} }
    

    

    #options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = webdriver.Chrome(options= options)

    login(bot, username, password)

    # for user in usernames:
    user = user.strip()

    
    if not mode == 3:
        scrape_profile(bot, user, mode)
    else:
        scrape_profile(bot, user, 1)
        scrape_profile(bot, user, 2)

    bot.quit()


if __name__ == '__main__':
    scrape()