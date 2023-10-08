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




def read_profile(name):
    # empty list to read list from a file
    names = []
    # open file and read the content in a list
    with open(f'instagramuser/{name}/profile.txt', 'r') as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]
            # add current item to the list
            names.append(x)

    return names

def count_jpg_files(name):
    directory = f'instagramuser/{name}/images'

    if not os.path.exists(directory):
        os.makedirs(directory)

    count = 0
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            count += 1
    return count

def write_alluser_toFile(lst):
    path = f"instagramuser/ALLinstagramUSERS.txt"
    # Create directory if it does not exist
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Write list to file
    with open(path, 'w') as f:
        for item in lst:
            f.write(f'{item}\n')

def write_follower_toFile(lst, name):
    path = f"instagramuser/{name}/follower.txt"
    # Create directory if it does not exist
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Write list to file
    with open(path, 'w') as f:
        for item in lst:
            f.write(f'{item}\n')

def write_following_toFile(lst, name):
    path = f"instagramuser/{name}/following.txt"
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
    with open(f'instagramuser/{name}/follower.txt', 'r') as fp:
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
    with open(f'instagramuser/{name}/following.txt', 'r') as fp:
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
    with open(f'instagramuser/ALLinstagramUSERS.txt', 'r') as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            names.append(x)

    return names

def download_images(driver, name, imagenumber):
    time.sleep(random.randint(2,4))
    # find the images
    images = driver.find_elements(By.TAG_NAME, 'img')
    path = f"instagramuser/{name}/images"
    # create the directory if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)

    hrefs = []
    for img in images[3:]:
        if img.get_attribute("class") == "x6umtig x1b1mbwd xaqea5y xav7gou" \
                                         " xk390pu x5yr21d xdj266r x11i5rnm " \
                                         "xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 " \
                                         "xkhd6sd x11njtxf xh8yej3":
            continue

        if img.get_attribute('class') == "xpdipgo x6umtig x1b1mbwd xaqea5y " \
                                         "xav7gou xk390pu x5yr21d xdj266r" \
                                         " x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 " \
                                         "x18d9i69 xkhd6sd x11njtxf xh8yej3":
            continue
        hrefs.append(img.get_attribute('src'))

    number = 0


    for img_src in hrefs:
        if number > imagenumber:
            break
        driver.get(img_src)
        time.sleep(2)
        filename = path + f'/image-{number}.jpg'
        number += 1
        with open(filename, 'wb') as fp:
            fp.write(driver.find_element(By.TAG_NAME, "img").screenshot_as_png)



def find_profile_detail(driver, name):
    images = driver.find_elements(By.TAG_NAME, 'img')
    pathprof = f"instagramuser/{name}/images"
    # create the directory if it doesn't exist
    if not os.path.exists(pathprof):
        os.makedirs(pathprof)

    profsrc = images[3].get_attribute('src')

    driver.get(profsrc)
    time.sleep(2)
    filename = pathprof + '/image-0.jpg'
    with open(filename, 'wb') as fp:
        fp.write(driver.find_element(By.TAG_NAME, "img").screenshot_as_png)
    driver.back()
    time.sleep(2)
    path = f"instagramuser/{name}/profile.txt"
    # Create directory if it does not exist
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    allspan = driver.find_elements(By.TAG_NAME, 'span')
    lst = []
    for sp in allspan:
        if sp.get_attribute('class') == '_ac2a':
            string = sp.get_attribute('innerHTML')
            print(string)
            match = re.search(r'<span>(.+?)</span>', string)
            if match:
                result = match.group(1)
                lst.append(result)
            else:
                print("No match found")

    # Write list to file
    with open(path, 'w') as f:
        for item in lst:
            f.write(f'{item}\n')

    return lst


def scrape_followers(driver, username, user_input):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/followers')]"))).click()
    time.sleep(random.randint(2, 3))
    fBody = driver.find_element(By.XPATH, "//div[@class='_aano']")
    scroll = 0
    timetoscroll = (user_input + 10) // 6
    while scroll < timetoscroll:  # scroll 5 times
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        time.sleep(random.randint(2, 3))
        scroll += 1

    users = set()

    ff = driver.find_elements(By.TAG_NAME, "span")
    for i in ff:
        if i.get_attribute('class') == "_aacl _aaco _aacw _aacx _aad7 _aade":
            users.add(i.get_attribute('innerHTML'))
        else:
            continue

    return list(users)


def scrape_followings(driver, username, user_input):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/following')]"))).click()
    time.sleep(random.randint(2, 3))
    print(f"[Info] - scrolling down followings for {username}...")
    fBody = driver.find_element(By.XPATH, "//div[@class='_aano']")
    scroll = 0
    timetoscroll = (user_input + 10) // 6
    while scroll < timetoscroll:  # scroll 5 times
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        time.sleep(random.randint(2, 3))
        scroll += 1
        print(f"[Info] - Scraping followings for {username}...{(scroll * 100) // timetoscroll}%")

    users = set()

    ff = driver.find_elements(By.TAG_NAME, "span")
    for i in ff:
        if i.get_attribute('class') == "_aacl _aaco _aacw _aacx _aad7 _aade":
            users.add(i.get_attribute('innerHTML'))
            print(i.get_attribute('innerHTML'))
        else:
            continue

    return list(users)


def scrape_instagram(driver, username, imageinput, ferinput, finginput, ):

    if len(username) < 2:
        return

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




    driver.get(f'https://www.instagram.com/{username}/')
    time.sleep(2)

    try:
        proflist = find_profile_detail(driver, username)
    except:
        list_of_followers = ['not foung']
        list_of_followings = ['not found']
        write_follower_toFile(list_of_followers, username)
        write_following_toFile(list_of_followings, username)
        return


    ff = driver.find_elements(By.TAG_NAME, "h2")
    for i in ff:
        try:
            if i.get_attribute('class') == "_aa_u" and i.get_attribute('innerHTML') == "This Account is Private":
                print(i.get_attribute('innerHTML'))
                list_of_followers = ['private']
                list_of_followings = ['private']
                write_follower_toFile(list_of_followers, username)
                write_following_toFile(list_of_followings, username)
                return
        except:
            break



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

    if imageinput > count_jpg_files(username):
        download_images(driver, username, imageinput)



def read_tags(name):
    # empty list to read list from a file
    names = []
    # open file and read the content in a list
    with open(f'instagramuser/{name}/tags.txt', 'r', encoding="utf-8") as fp:
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
    with open(f'instagramuser/{name}/comments.txt', 'r', encoding="utf-8") as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            names.append(x)

    return names

def write_comments(lst, name):
    path = f"instagramuser/{name}/comments.txt"
    # Create directory if it does not exist
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Write list to file
    with open(path, 'w', encoding="utf-8") as f:
        for item in lst:
            f.write(f'{item}\n')

def write_tag(lst, name):
    path = f"instagramuser/{name}/tags.txt"
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

def scrape_tags(driver, username):
    driver.get(f'https://www.instagram.com/{username}/')
    time.sleep(3)
    allcomment = []
    alltags = []
    try:
        bio = driver.find_element(By.TAG_NAME, 'h1')
        alltags.append(remove_html_tags_word(bio.get_attribute('innerHTML')))
    except:
        pass

    allpost = driver.find_elements(By.CLASS_NAME, '_aagw')
    for post in allpost:
        post.click()
        time.sleep(2)
        des = driver.find_elements(By.TAG_NAME, 'h1')
        try:
            allcomment.append(remove_html_tags_word(des[1].get_attribute('innerHTML')))
        except:
            try:
                allcomment.append(remove_html_tags_word(des[1].get_attribute('innerHTML')))
            except:
                pass

        t = driver.find_elements(By.TAG_NAME, 'a')
        for tt in t:
            try:
                if tt.get_attribute('class') == "x1i10hfl xjbqb8w x6umtig x1b1mbwd" \
                                                " xaqea5y xav7gou x9f619 x1ypdohk " \
                                                "xt0psk2 xe8uvvx xdj266r x11i5rnm " \
                                                "xat24cr x1mh8g0r xexx8yu x4uap5 " \
                                                "x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg " \
                                                "xggy1nq x1a2a7pz  _aa9_ _a6hd":
                    alltags.append(tt.get_attribute('innerHTML'))
            except:
                pass

        driver.back()

    allcomment = clean_text(allcomment)
    write_tag(alltags, username)
    write_comments(allcomment, username)

    return (alltags, allcomment)



if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_argument("user-data-dir=C:/Users/salia/AppData/Local/Google/Chrome/User Data/Default")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.instagram.com/")

    scrape_instagram(driver, 'fseyedmousavi',50, 50)