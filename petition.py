import random
import re

import requests
from bs4 import BeautifulSoup as beautifulsoup
from selenium import webdriver


def print_list(my_list):
    print('---------------------')
    for x in my_list:
        print(x)
    print('---------------------')


def retrieveNames(url, file_name):
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
    }

    res = requests.get(url, headers=user_agent)
    soup = beautifulsoup(res.content, 'html5lib')
    names = soup.find_all('div', attrs={"class": "baby-name M14_pink"})

    with open(file_name, 'w+', encoding='utf-8') as x:
        for line in list(soup.find_all('h3')):
            line = str(line).strip('<h3>')
            line = str(line).strip('</h3>')

            line = re.sub('\d+. ', '', line)
            line = line.strip(':')
            line = line.strip(". ")
            x.writelines(str(line) + '\n')


def getNames():
    last_name_url = 'https://www.momjunction.com/articles/popular-indian-last-names-for-your-baby_00334734/'
    first_name_url = 'https://www.momjunction.com/articles/indian-baby-boy-names-with-meanings_00349318/'
    retrieveNames(last_name_url, 'last_name')
    retrieveNames(first_name_url, 'first_name')


def sign(first_names, last_names):
    fname = random.choice(first_names).strip()
    lname = random.choice(last_names).strip()
    email = fname + lname + str(random.randint(0, 220000)) + '@gmail.com'

    data = {
        'firstName': fname,
        'lastName': lname,
        'email': email
    }

    url = 'https://www.change.org/p/realme-mobiles-release-the-flashtool-for-realme-devices'

    browser = webdriver.Firefox()
    browser.get(url)
    for key in data:
        a = browser.find_element_by_name(key)
        a.send_keys(data[key])
    a.submit()

    print(fname, lname)
    # x = input()
    browser.quit()


def start():
    first_names = open('first_name', 'r').readlines()
    last_names = open('last_name', 'r').readlines()

    for x in range(200):
        sign(first_names, last_names)
    # sign(first_names, last_names)


start()
