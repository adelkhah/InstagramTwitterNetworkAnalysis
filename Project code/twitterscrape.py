import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time, urllib.request
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import re
import os
import json
import relation_to_json






def write_alluser_toFile(lst):
    path = f"twitteruser/ALLtwitterUSERS.txt"
    # Create directory if it does not exist
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Write list to file
    with open(path, 'w') as f:
        for item in lst:
            f.write(f'{item}\n')

def write_follower_toFile(lst, name):
    path = f"twitteruser/{name}/follower.txt"
    # Create directory if it does not exist
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Write list to file
    with open(path, 'w') as f:
        for item in lst:
            f.write(f'{item}\n')

def write_following_toFile(lst, name):
    path = f"twitteruser/{name}/following.txt"
    # Create directory if it does not exist
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Write list to file
    with open(path, 'w') as f:
        for item in lst:
            f.write(f'{item}\n')

def read_follower_fromFile(name):
    # empty list to read list from a file
    names = []
    # open file and read the content in a list
    with open(f'twitteruser/{name}/follower.txt', 'r') as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            names.append(x)

    return names

def read_following_fromFile(name):
    # empty list to read list from a file
    names = []
    # open file and read the content in a list
    with open(f'twitteruser/{name}/following.txt', 'r') as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            names.append(x)

    return names

def read_alluser_fromFile():
    # empty list to read list from a file
    names = []
    # open file and read the content in a list
    with open(f'twitteruser/ALLtwitterUSERS.txt', 'r') as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            names.append(x)

    return names



def scrape_followers(driver, username, user_input):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/verified_followers')]"))).click()

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/followers')]"))).click()


    time.sleep(random.randint(2, 3))
    users = set()
    numbertoscroll = (user_input + 20) // 8
    for i in range(numbertoscroll):
        ff = driver.find_elements(By.TAG_NAME, "span")
        for j in ff:
            if j.get_attribute('class') == "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0":
                nn = j.get_attribute('innerHTML')
                if nn[0] == '@':
                    users.add(nn)

        old = i * 1000
        now = (i + 1) * 1000
        driver.execute_script(f"window.scrollTo({old}, {now})")
        time.sleep(3)

    return list(users)


def scrape_followings(driver, username, user_input):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/following')]"))).click()
    time.sleep(random.randint(2, 3))
    users = set()
    numbertoscroll = (user_input + 20) // 8
    for i in range(numbertoscroll):
        ff = driver.find_elements(By.TAG_NAME, "span")
        for j in ff:
            if j.get_attribute('class') == "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0":
                nn = j.get_attribute('innerHTML')
                if nn[0] == '@':
                    users.add(nn)

        old = i * 1000
        now = (i + 1) * 1000
        driver.execute_script(f"window.scrollTo({old}, {now})")
        time.sleep(3)

    return list(users)




def scrape_twitter(driver, username, ferinput, finginput, ):


    alluser = read_alluser_fromFile()
    list_of_followers = []
    list_of_followings = []

    if username in alluser:
        list_of_followers = read_follower_fromFile(username)
        list_of_followings = read_following_fromFile(username)
    else:
        write_following_toFile([],username)
        write_follower_toFile([],username)
        alluser.append(username)
        write_alluser_toFile(alluser)


    if len(list_of_followers) == 1 and list_of_followers[0] == 'private':
        print("this account is private")
        return


    driver.get(f'https://www.twitter.com/{username}/')
    time.sleep(2)

    spans = driver.find_elements(By.TAG_NAME, 'span')

    for sp in spans:
        if sp.get_attribute('class') == "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0":
            if "These Tweets are protected" in sp.get_attribute('innerHTML'):
                list_of_followers = ['private']
                list_of_followings = ['private']
                write_follower_toFile(list_of_followers, username)
                write_following_toFile(list_of_followings, username)
                return

            elif "This account doesn’t exist" in sp.get_attribute('innerHTML'):
                list_of_followers = ['notExist']
                list_of_followings = ['notExist']
                write_follower_toFile(list_of_followers, username)
                write_following_toFile(list_of_followings, username)
                return

            elif "Caution: This " in sp.get_attribute('innerHTML'):
                list_of_followers = ['Caution']
                list_of_followings = ['Caution']
                write_follower_toFile(list_of_followers, username)
                write_following_toFile(list_of_followings, username)
                return

        if sp.get_attribute('class') == "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0":
            if "suspended" in sp.get_attribute('innerHTML'):
                list_of_followers = ['suspended']
                list_of_followings = ['suspended']
                write_follower_toFile(list_of_followers, username)
                write_following_toFile(list_of_followings, username)
                return

    if ferinput > len(list_of_followers):
        list_of_followers = scrape_followers(driver, username, ferinput)
        write_follower_toFile(list_of_followers, username)
        driver.back()
        time.sleep(2)


    if finginput > len(list_of_followings):
        list_of_followings = scrape_followings(driver, username, finginput)
        write_following_toFile(list_of_followings, username)
        driver.back()
        time.sleep(2)

    scrape_tags(driver, username)


def read_tags(name):
    # empty list to read list from a file
    names = []
    # open file and read the content in a list
    with open(f'twitteruser/{name}/tags.txt', 'r', encoding="utf-8") as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            names.append(x)

    return names

def read_comments(name):
    # empty list to read list from a file
    names = []
    # open file and read the content in a list
    with open(f'twitteruser/{name}/comments.txt', 'r', encoding="utf-8") as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            names.append(x)

    return names

def write_comments(lst, name):
    path = f"twitteruser/{name}/comments.txt"
    # Create directory if it does not exist
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Write list to file
    with open(path, 'w', encoding="utf-8") as f:
        for item in lst:
            f.write(f'{item}\n')

def write_tag(lst, name):
    path = f"twitteruser/{name}/tags.txt"
    # Create directory if it does not exist
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Write list to file
    with open(path, 'w', encoding="utf-8") as f:
        for item in lst:
            f.write(f'{item}\n')


def clean_text(text_list):
    cleaned_text = []
    for text in text_list:
        # Remove all non-alphanumeric characters
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 0:
            cleaned_text.append(text)
    return cleaned_text



def remove_html_tags_word(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def remove_newlines(text):
    return re.sub('\n', ' ', text)

def remove_hashtag(text):
    return re.sub('#', '', text)

def scrape_tags(driver, username):
    old = 0
    new = 500
    alltweets = set()
    alltags = set()
    for _ in range(4):
        driver.execute_script(f"window.scrollTo({old}, {new})")
        old += 500
        new += 500
        time.sleep(2)
        articles = driver.find_elements(By.TAG_NAME, 'div')

        for art in articles:
            if art.get_attribute('data-testid') == 'tweetText':

                allspan = art.find_elements(By.TAG_NAME, 'span')
                tweettext = ""

                pp = art.find_elements(By.XPATH, "//a[contains(@href, '/hashtag')]")
                for p in pp:
                    alltags.add(p.get_attribute('innerHTML'))

                for span in allspan:
                    tweettext += remove_html_tags_word(span.text)

                alltweets.add(remove_newlines(tweettext))

    write_tag(list(alltags), username)
    write_comments(list(alltweets), username)



def find_hashtags(text):
    hashtags = re.findall(r'\B#\w*', text)
    return hashtags

def find_ID(text):
    hashtags = re.findall(r'\B@\w*', text)
    return hashtags


def find_ID_list(l):
    ans = []
    for p in l:
        ans += find_ID(p)

    return ans



def find_hashtags_list(l):
    ans = []
    for p in l:
        ans += find_hashtags(p)

    return ans



if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_argument("user-data-dir=C:/Users/salia/AppData/Local/Google/Chrome/User Data/Default")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.twitter.com/")


    scrape_twitter(driver, 'TavFanavar',80, 80)