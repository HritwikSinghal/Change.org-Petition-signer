# Sign change.org petitions automatically and using proxies.
Uses Selenium.It will automatically ask for url and whether to use
proxies or not. If you chose to sign using proxies, it will auto fetch proxies and sign
using them. A new firefox window will be opened every time to sign. (selenium)


To run: 
- download and Install python 3 (https://www.python.org/downloads/) and firefox (https://www.mozilla.org/en-US/firefox/new/)
- download or clone this repo https://github.com/HritwikSinghal/petition
- extract it and open terminal in that folder & run below commends

```
$ pip3 install -r requirements.txt
$ python3 petition.py
```
Currently only tested on windows. If on linux or macOS, the only problem would be of firefox driver.
