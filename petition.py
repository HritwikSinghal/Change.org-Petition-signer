import json
import random
import re
import traceback

import requests
from bs4 import BeautifulSoup as beautifulsoup

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType


def print_list(my_list):
    print('---------------------')
    for x in my_list:
        print(x)
        # print('"' + x + '"' + ',')
    print('---------------------')


def retrieveNames(url, file_name):
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
    }

    res = requests.get(url, headers=user_agent)
    soup = beautifulsoup(res.content, 'html5lib')

    with open(file_name, 'w+', encoding='utf-8') as x:
        for line in list(soup.find_all('h3')):
            line = str(line).strip('<h3>')
            line = str(line).strip('</h3>')

            line = re.sub('\d+. ', '', line)
            line = line.strip(':')
            line = line.strip(". ")
            x.writelines(str(line) + '\n')


def fate_proxy():
    resp = requests.get('https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list')
    a = ((resp.text).split('\n'))
    p_list = []
    for i in a:
        try:
            p_list.append(json.loads(i))
        except Exception as e:
            continue
    np_list = []

    countries = ["AE",
                 "AR",
                 "AU",
                 "AZ",
                 "BD",
                 "BG",
                 "BO",
                 "BR",
                 "CA",
                 "CL",
                 "CN",
                 "CO",
                 "CR",
                 "CZ",
                 "DE",
                 "EC",
                 "FR",
                 "GB",
                 "GE",
                 "GH",
                 "GN",
                 "HK",
                 "ID",
                 "IL",
                 "IN",
                 "IQ",
                 "JP"
                 ]
    for i in p_list:
        if i['country'] in countries:
            # print(i['country'])
            np_list.append(i)
        # np_list.append(i)
    proxy = []
    fast_proxy = sorted(np_list, key=lambda k: k['response_time'])
    for p in fast_proxy:
        proxy.append(str(p['host']) + ':' + str(p['port']))
    return proxy


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
    # url = 'https://www.change.org/p/free-nazanin-ratcliffe?source_location=discover_feed'

    proxies = fate_proxy()
    # random.shuffle(proxies)

    for proxy in proxies:

        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True

        firefox_capabilities['proxy'] = {
            "proxyType": "MANUAL",
            "httpProxy": proxy,
            "ftpProxy": proxy,
            "sslProxy": proxy
        }
        browser = webdriver.Firefox(capabilities=firefox_capabilities)

        try:
            # proxy = '45.236.88.42:8880'
            print('Using Proxy: ', proxy)
            browser.set_page_load_timeout(30)

            browser.get(url)
            for key in data:
                a = browser.find_element_by_name(key)
                a.send_keys(data[key])

            try:
                b = browser.find_element_by_name('marketingCommsConsent.consentGiven')
                b.click()
                b.submit()
            except:
                a.submit()

            print("filled by: ", fname, lname)
            print()
            x = input()
            browser.quit()

        except:
            browser.quit()
            # traceback.print_exc()
            print('skipping this proxy')
            continue


def start():
    first_names = open('first_name', 'r').readlines()
    last_names = open('last_name', 'r').readlines()

    for x in range(200):
        try:
            sign(first_names, last_names)
        except:
            print("timeout")
            continue


start()
