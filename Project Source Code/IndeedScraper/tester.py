import config
import FileWriter
import DriverFunctions

import re
import requests
import json
import os
import timeit
import time
import sqlite3
import os
import sys

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
config.startTime = timeit.default_timer()

from win32com.client import Dispatch

def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version


paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
version = list(filter(None, [get_version_via_com(p) for p in paths]))[0]

#Creates a random fake 'useragent' to reduce the amount of Captchas
ua = UserAgent()
userAgent = ua.random

#Makes the chromedriver use Canary instead of normal chrome to reduce the amount of Captchas
#Headless is disabled because I love watching it work
chrome_options = Options()
#chrome_options.add_argument("--headless")
username = os.getlogin( )
chrome_options.add_argument(f'user-agent={userAgent}')



try:
    chrome_options.binary_location = "C:\\Users\\" + username + r"\AppData\Local\Google\Chrome SxS\Application\chrome.exe"
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriverCanary"), chrome_options=chrome_options)
    driver.delete_all_cookies()
    driver2 = webdriver.Chrome(executable_path=os.path.abspath("chromedriverCanary"), chrome_options=chrome_options)
    driver2.delete_all_cookies()
except:
    chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if version[1] == '0':
        driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver10"), chrome_options=chrome_options)
        driver.delete_all_cookies()
        driver2 = webdriver.Chrome(executable_path=os.path.abspath("chromedriver10"), chrome_options=chrome_options)
        driver2.delete_all_cookies()
    elif version[1] == '9':
        driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver9"), chrome_options=chrome_options)
        driver.delete_all_cookies()
        driver2 = webdriver.Chrome(executable_path=os.path.abspath("chromedriver9"), chrome_options=chrome_options)
        driver2.delete_all_cookies()
    elif version[1] == '8':
        driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver8"), chrome_options=chrome_options)
        driver.delete_all_cookies()
        driver2 = webdriver.Chrome(executable_path=os.path.abspath("chromedriver8"), chrome_options=chrome_options)
        driver2.delete_all_cookies()
    else:
        input("Make sure you have version 98 or higher of Google Chrome installed. Press enter to exit the program.")
        sys.exit()
