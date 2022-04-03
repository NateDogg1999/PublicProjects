import config

import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def gotoNextPageResults(driver):
	stillLooping = True
	while stillLooping:
		xpath_str = f'/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/nav/div/ul/li[{config.xpath}]/a'
	
		#Tries first with an xpath of 7, then if that fails, does it with a 6 instead
		try:
	
			if ("hCaptcha" in BeautifulSoup(driver.page_source, "html.parser").find("title").text):
				input("Press something once captcha is solved: ")
	
			#Goes to the next page of results by clicking through Javascript (arguments[0].click()) rather than a 'natural' click
			driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(xpath_str))
			config.xpath = 7
			stillLooping = False
			config.actually_done_countdown = 0
	
		#If 7 doesn't work, change the xpath to 6 and try again. If it continues to not work, it must mean there are no pages left, so end the scraper
		except:
			stillLooping = True
			config.xpath = 6
			config.actually_done_countdown += 1
	
			if(config.actually_done_countdown > 2):
				config.fully_done = True
				break