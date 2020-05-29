import requests
import re
from bs4 import BeautifulSoup as beautifulsoup


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
    def get_names(url, file_name):
        # url = 'https://www.change.org/p/realme-mobiles-release-the-flashtool-for-realme-devices'

        user_agent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
        }

        res = requests.get(url, headers=user_agent)
        soup = beautifulsoup(res.text, "html5lib")
        content = soup.prettify()


def start():
    sign()


start()
