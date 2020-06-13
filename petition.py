import os
import platform
import random
import time
import traceback

from faker import Faker
from selenium import webdriver

# def retrieveNames(url, file_name):
#     user_agent = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
#     }
#
#     res = requests.get(url, headers=user_agent)
#     soup = beautifulsoup(res.content, 'html5lib')
#
#     with open(file_name, 'w+', encoding='utf-8') as x:
#         for line in list(soup.find_all('h3')):
#             line = str(line).strip('<h3>')
#             line = str(line).strip('</h3>')
#
#             line = re.sub('\d+. ', '', line)
#             line = line.strip(':')
#             line = line.strip(". ")
#             x.writelines(str(line) + '\n')

# def getNames():
#     last_name_url = 'https://www.momjunction.com/articles/popular-indian-last-names-for-your-baby_00334734/'
#     first_name_url = 'https://www.momjunction.com/articles/indian-baby-boy-names-with-meanings_00349318/'
#     retrieveNames(last_name_url, 'last_name')
#     retrieveNames(first_name_url, 'first_name')

wait_time = 3


def sign(browser):
    global wait_time

    fname = Faker().first_name()
    lname = Faker().last_name()
    randemail = fname + lname + str(random.randint(0, 50000)) + '@gmail.com'

    print("Using: ", fname, lname, randemail)

    fnamebox = browser.find_element_by_name('firstName')
    lnamebox = browser.find_element_by_name("lastName")
    emailbox = browser.find_element_by_name("email")
    publiccheck = browser.find_element_by_name("public")

    # This will not work
    # fnamebox.send_keys(fname)
    # time.sleep(1)
    # lnamebox.send_keys(lname)
    # time.sleep(1)
    # emailbox.send_keys(randemail)
    # time.sleep(1)
    # publiccheck.click()
    # time.sleep(1)
    # emailbox.submit()
    # time.sleep(1)

    # this will work
    for k in fname:
        fnamebox.send_keys(k)
        # time.sleep(.1)

    for k in lname:
        lnamebox.send_keys(k)
        # time.sleep(.1)

    for k in randemail:
        emailbox.send_keys(k)
        # time.sleep(.1)

    publiccheck.click()
    emailbox.submit()
    time.sleep(wait_time)

    if 'Share petition' not in browser.title:
        # print(browser.title)
        browser.delete_all_cookies()
        wait_time += 1
        print("New Wait time:", wait_time)

        time.sleep(10)

    browser.delete_all_cookies()


def start(test=0):
    print("""
      ____  _             ____        _
     / ___|(_) __ _ _ __ | __ )  ___ | |_
     \___ \| |/ _` | '_ \|  _ \ / _ \| __|
      ___) | | (_| | | | | |_) | (_) | |_
     |____/|_|\__, |_| |_|____/ \___/ \__|
              |___/
    """)
    print("Starting...")

    if not test:
        url = input("Enter url: ")
    else:
        url = 'https://www.change.org/p/realme-mobiles-release-the-flashtool-for-realme-devices'

    os_name = platform.system()
    os_arch, t = platform.architecture()

    if os_name == 'Linux':
        if os_arch == "64bit":
            loc = './geckodriver_L64'
        else:
            loc = './geckodriver_L32'
    elif os_name == "Windows":
        if os_arch == "64bit":
            loc = './geckodriver_W64'
        else:
            loc = './geckodriver_W32'
    else:
        print("OS Not Supported...")
        exit(0)

    # these are the workarounds for not getting flagged as bot
    # UA = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0"
    # profile = webdriver.FirefoxProfile('/home/hritwik/.mozilla/firefox/zufq32k3.New')
    profile = webdriver.FirefoxProfile()
    # profile.set_preference("general.useragent.override", UA)
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)  # this is must
    profile.set_preference('devtools.jsonview.enabled', False)
    profile.update_preferences()

    browser = webdriver.Firefox(profile, executable_path=loc)

    for _ in range(1, 200):
        try:
            browser.get(url)
            sign(browser)
        except:
            if test:
                traceback.print_exc()

            browser.delete_all_cookies()
            print("Error filling form. Refreshing...")


try:
    if os.path.isfile('./test_bit'):
        test = 1
    else:
        test = 0
except:
    test = 0

try:
    start(test=test)
except:
    if test:
        traceback.print_exc()
    print("Exiting...")
    exit(0)
