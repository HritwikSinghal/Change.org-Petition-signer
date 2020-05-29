import ast
import base64
import json
import os
import re
import traceback
from Base import tools

import requests
import urllib3.exceptions
from bs4 import BeautifulSoup
from pyDes import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
}


# -------------------------------------------#
# todo: inspect below func's

def fate_proxy():
    resp = requests.get('https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list')
    a = resp.text.split('\n')
    p_list = []
    for i in a:
        try:
            p_list.append(json.loads(i))
        except Exception as e:
            continue
    np_list = []
    for i in p_list:
        if i['country'] == 'IN':
            np_list.append(i)
    proxy = []
    fast_proxy = sorted(np_list, key=lambda k: k['response_time'])
    for p in fast_proxy:
        proxy.append(str(p['host']) + ':' + str(p['port']))
    return proxy


def setProxy():
    base_url = 'http://h.saavncdn.com'
    proxy_ip = ''
    if 'http_proxy' in os.environ:
        proxy_ip = os.environ['http_proxy']
    proxies = {
        'http': proxy_ip,
        'https': proxy_ip,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
    }
    return proxies, headers


# -------------------------------------------#

def decrypt_url(url):
    des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    base_url = 'http://h.saavncdn.com'

    enc_url = base64.b64decode(url.strip())
    dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
    dec_url = base_url + dec_url[10:] + '_320.mp3'
    r = requests.get(dec_url)
    if str(r.status_code) != '200':
        dec_url = dec_url.replace('_320.mp3', '.mp3')
    return dec_url


def get_lyrics(url):
    try:
        if '/song/' in url:
            # url = url.replace("/song/", '/lyrics/')
            source = requests.get(url).text
            soup = BeautifulSoup(source, 'html5lib')
            res = soup.find('p', class_='lyrics')
            lyrics = str(res).replace("<br/>", "\n")
            lyrics = lyrics.replace('<p class="lyrics"> ', '')
            lyrics = lyrics.replace("</p>", '')
            return (lyrics)
    except Exception:
        traceback.print_exc()
        return


def start(url, log_file, test=0):
    # returns list of songs from search url.
    # each element of list is a dict in json format with song data

    proxies = fate_proxy()

    try:
        res = requests.get(url, headers=user_agent, data=[('bitrate', '320')])

        soup = BeautifulSoup(res.text, "html5lib")
        all_songs_info = soup.find_all('div', attrs={"class": "hide song-json"})

        song_list = []

        for info in all_songs_info:
            try:
                json_data = json.loads(str(info.text))

                #######################
                # print("IN TRY")
                #######################

            except:
                # the error is caused by quotation marks in songs title as shown below
                # (foo bar "XXX")
                # so just remove the whole thing inside parenthesis

                #######################
                # print("IN EXCEPT")
                # print(info.text)
                # x = input()
                #######################

                try:
                    x = re.compile(r'''
                        (
                        [(\]]
                        .*          # 'featured in' or 'from' or any other shit in quotes
                        "(.*)"      # album name
                        [)\]]
                        )
                        ","album.*"
                        ''', re.VERBOSE)

                    rem_str = x.findall(info.text)

                    # old method, dont know why this wont work
                    # json_data = re.sub(rem_str[0][0], '', str(info.text))

                    json_data = info.text.replace(rem_str[0][0], '')

                    #######################
                    # print("IN EXCEPT2")
                    # print(rem_str[0][0])
                    # print(json_data)
                    # a = input()
                    #######################

                    # actually that thing in () is the correct album name, so save it.
                    # since saavn uses song names as album names, this will be useful

                    if len(rem_str[0]) > 1:
                        actual_album = rem_str[0][1]
                    else:
                        actual_album = ''

                except:
                    # old method, if above wont work, this will work 9/10 times.

                    json_data = re.sub(r'.\(\b.*?"\)', "", str(info.text))
                    json_data = re.sub(r'.\[\b.*?"\]', "", json_data)
                    actual_album = ''

                try:
                    json_data = json.loads(str(json_data))
                except:
                    continue

                if actual_album != '':
                    json_data['actual_album'] = actual_album

            fix(json_data)
            json_data = json.dumps(json_data, indent=2)

            song_list.append(json_data)

        return song_list
    except Exception:
        print("invalid url...")
        tools.writeAndPrintLog(log_file, '\nSaavnAPI error, url={}\n'.format(url), test=test)
        return []


def fix(json_data):
    json_data['album'] = tools.removeGibberish(json_data['album']).strip()

    oldArtist = json_data['singers']
    newArtist = tools.removeGibberish(oldArtist)
    newArtist = tools.divideBySColon(newArtist)
    newArtist = tools.removeTrailingExtras(newArtist)
    json_data['singers'] = tools.removeDup(newArtist)

    old_composer = json_data['music']
    new_composer = tools.removeGibberish(old_composer)
    new_composer = tools.divideBySColon(new_composer)
    new_composer = tools.removeTrailingExtras(new_composer)
    json_data['music'] = tools.removeDup(new_composer)

    json_data['title'] = tools.removeGibberish(json_data['title'])
