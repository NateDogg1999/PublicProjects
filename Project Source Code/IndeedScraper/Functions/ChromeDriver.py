from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from win32com.client import Dispatch

import os
import sys

#Gets the version of chrome installed
def get_version_via_com(filename):
	parser = Dispatch("Scripting.FileSystemObject")
	try:
		version = parser.GetFileVersion(filename)
	except Exception:
		return "11"
	return version

def launchDriver():
	paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
		  r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
	version = list(filter(None, [get_version_via_com(p) for p in paths]))[0]
	
	#Creates a random fake 'useragent' to reduce the amount of Captchas
	ua = UserAgent()
	userAgent = ua.random
	
	
	#Headless is disabled because I love watching it work
	chrome_options = Options()
	#chrome_options.add_argument("--headless")
	username = os.getlogin( )
	chrome_options.add_argument(f'user-agent={userAgent}')
	
	
	try:
		#Makes the chromedriver use Canary instead of normal chrome to reduce the amount of Captchas
		chrome_options.binary_location = "C:\\Users\\" + username + r"\AppData\Local\Google\Chrome SxS\Application\chrome.exe"
		driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriverCanary"), chrome_options=chrome_options)

	#If canary fails, use normal chrome instead
	except:
		if version[1] != '8' and version[1] != '9' and version[1] != '0':
			input("Make sure you have version 98 or higher of Google Chrome installed. Press enter to exit the program.")
			sys.exit()
		try:
			chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
			driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver" + version[1]), chrome_options=chrome_options)
		except:
			try:
				chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
				driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver" + version[1]), chrome_options=chrome_options)
			except:
				input("Google chrome does not seem to be installed in the default directory. Press enter to exit the program.")
				sys.exit()


	driver.delete_all_cookies()
	return driver




