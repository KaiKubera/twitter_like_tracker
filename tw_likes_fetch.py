import pickle
import time
import os
from pathlib import Path
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


load_dotenv(override=True)

def get_likes():
    # Check if prior list of Twitter links exists as a .pickle file:
    link_list_path = Path('link_list.pickle')
    if link_list_path.is_file():
        with open('link_list.pickle', 'rb') as file:
            link_list = pickle.load(file)

    class TwitterBot:
        def __init__(self, username, password):
            '''
            This method asign the username and the password parameters inputs in the driver that will be used in the following methods
            '''
            self.username = username
            self.password = password
            self.bot = webdriver.Chrome()  # Copy YOUR chromedriver path

            # Clears and then fills in login/password fields on Twitter login
            # ONLY WORKS WHEREVER TWITTER IS WORKING (use VPN while in Russia for the time being)
            bot = self.bot
            # bot.get('https://twitter.com/login')
            bot.get('https://x.com/i/flow/login')
            time.sleep(15)

            email = bot.find_element("xpath", '//input[@autocomplete="username"]')
            email.clear()
            email.send_keys(self.username)
            email.send_keys(Keys.RETURN)
            time.sleep(7)

            password = bot.find_element("xpath", '//input[@name="password"]')
            password.send_keys(self.password)
            time.sleep(3)
            password.send_keys(Keys.RETURN)
            time.sleep(3)

        def liked_tweets(self):
            bot = self.bot
            likes_url = 'https://twitter.com/' + self.username + '/likes'
            bot.get(likes_url)

            max_scrolls = 10
            scroll_count = 0
            scroll_distance = 2000
            tweet_links_urls = []

            while scroll_count < max_scrolls:
                bot.execute_script(f"window.scrollBy(0, {scroll_distance});")
                time.sleep(2)
                print(f'Scroll count {scroll_count} -> {scroll_count + 1}')
                scroll_count += 1
                tweets_before_scroll = bot.find_elements(By.XPATH,
                                                         "//a[contains(@href, '/status/') and not(contains(@href, '/photo/')) and not(contains(@href, '/analytics'))]")
                tweet_links_urls.extend([link.get_attribute('href') for link in tweets_before_scroll])
                # Check if prior Twitter link list exists, again:
                if link_list_path.is_file():
                    # print(f'Checking if {set(tweet_links_urls)} contains something from {set(link_list)}')
                    common_elements = set(tweet_links_urls) & set(link_list)

                    if common_elements:
                        print('Scrolled to old posts!')
                        print('Found common elements:')
                        for i in common_elements:
                            print(i)
                        print()
                        tweet_links_urls = [element for element in tweet_links_urls if element not in list(common_elements)]
                        break

            time.sleep(5)
            for link in set(tweet_links_urls):
                print(link)

            return set(tweet_links_urls)

    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    link_list = TwitterBot(username=username,
                           password=password).liked_tweets()
    print("New link list made!")

    if not link_list:
        print('HALT! Link list is empty. This is most likely due to having run the '
              'script before already, without having liked any new post. Like a Tweet and try again.')
        exit()

    else:
        with open('link_list.pickle', 'wb') as file:
            pickle.dump(link_list, file)
