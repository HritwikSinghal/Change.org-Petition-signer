import re

import requests
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
    url = 'https://www.change.org/p/realme-mobiles-release-the-flashtool-for-realme-devices'

    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
    }
    proxies = getProxyList.fate_proxy()
    # print_list(proxies)

    for proxy in proxies:
        try:
            res = requests.get(url, proxies={"http": proxy, "https": proxy}, headers=user_agent)
            if 'internal error' in res.text:
                continue
            break
        except Exception as e:
            print("Skipped this proxy")

    soup = beautifulsoup(res.text, "html5lib")
    content = soup.prettify()
    print(content)

    with open('a.txt', 'w+', encoding='utf-8') as data:
        data.write(content)


def start():
    sign()


start()
