# Sign change.org petitions automatically
![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+) 
Edit (June 2020) : So apparently Change.org added a Bot prevention script and
made this project useless. But Now i have implemented workaround and this is working fine. Also, proxy support has been removed.

For Windows & Linux Only. Not Compatible with MacOS.

Uses Selenium.It will automatically ask for url.

Installation:

Download and Install python 3 and Firefox
```
    (Windows)
    Python: https://www.python.org/downloads/ 
    Firefox: https://www.mozilla.org/en-US/firefox/new/

    (Linux)
    Python: sudo apt insatll python3
    Firofox: sudo apt install firefox

```

Clone this repository using
```sh
$ git clone https://github.com/HritwikSinghal/petition
```
Enter the directory and install all the requirements using
```sh
$ pip3 install -r requirements.txt
```
Run the app using
```sh
$ python3 petition.py
```

If the program is exiting just after entering url, try moving the folder to some other location (other drive on PC) and then re-run. This issue occurs mostly on Linux and is caused by missing permission of 'geckodriver_XXX' file. So moving to other drive usually solves the problem. Otherwise try to give proper permissions to 'geckodriver_XXX' (make sure to tick mark 'run as executable').
