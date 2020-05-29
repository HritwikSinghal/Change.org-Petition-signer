import re

import requests
import random
import mechanize  # sudo pip install python-mechanize
from bs4 import BeautifulSoup as beautifulsoup

import getProxyList


def print_list(my_list):
    print('---------------------')
    for x in my_list:
        print(x)
    print('---------------------')


def retrieveNames(url, file_name):
    # url = 'https://www.change.org/p/realme-mobiles-release-the-flashtool-for-realme-devices'

    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
    }

    res = requests.get(url, headers=user_agent)
    soup = beautifulsoup(res.text, "html5lib")

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


def sign():
    first_names = open('first_name', 'r').readlines()
    last_names = open('last_name', 'r').readlines()
    fname = random.choice(first_names).strip()
    lname = random.choice(last_names).strip()
    email = fname + lname + '@gmail.com'

    url = 'https://www.change.org/p/realme-mobiles-release-the-flashtool-for-realme-devices'
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
    }
    proxies = getProxyList.fate_proxy()

    br = mechanize.Browser()
    br.set_handle_robots(False)  # ignore robots

    for proxy in proxies:
        try:
            # res = requests.post(url, data=data, headers=user_agent, proxies={"http": proxy, "https": proxy})
            br.set_proxies({"http": proxy, "https": proxy})
            br.open(url)
            br.select_form(name="sign-form")
            br["firstName"] = fname
            br["lastName"] = lname
            br["email"] = email
            res = br.submit()

            if 'internal error' in str(res.read()):
                print("Internal Error")
                continue

            print("Done using ", fname, lname)
            break
        except Exception as e:
            print("Skipped this proxy")

    content = beautifulsoup(res.read(), 'html5lib').prettify()
    with open("ab.txt", 'w+', encoding='utf-8') as f:
        f.write(content)


def start():
    # for x in range(200):
    #     sign()
    sign()
    # proxies = getProxyList.fate_proxy()
    # print_list(proxies)


start()
