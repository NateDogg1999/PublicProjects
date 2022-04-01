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

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from win32com.client import Dispatch

#Wipes out current job file so I can use append later
output = open("indeedJobs.txt", "w")
output.close()

output = open("indeedCompanies.txt", "w")
output.close()


#Gets the version of chrome installed
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



reString = "https://ca.indeed.com/jobs?q=programmer&l=Victoria%2C%20BC"
indeed_req = driver.get(reString)

if "hCaptcha" in BeautifulSoup(driver.page_source, "html.parser").find("title").text:
	input("Press something once captcha is solved: ")


conn = sqlite3.connect('jobdb.sqlite')

cur = conn.cursor()


#The infinite loop allows it to keep looping until all the pages of the results have been reached
while(True):

	#Searches for all the job IDs on this page of results
	re_search = r"jobmap\[[0-9]+\]= {jk:'(.*)',efccid:"
	jobmapIds = re.findall(re_search, driver.page_source)
	

	#Gets info for each job using its jobmap ID
	for id in jobmapIds:
		
		currentJob = config.job()
		currentCompany = config.company()

		reString = 'https://ca.indeed.com/viewjob?jk=' + id
		config.idList.append(reString)

		#Checks if the current job is already in the database.
		#If it is, it updates the database to tell it that the job is currently active, then it skips the jobs
		if cur.execute(''' SELECT remote FROM Jobs WHERE jobLink=? ''', (reString,)).fetchone():
			cur.execute(''' UPDATE Jobs SET stillActive = 1 WHERE jobLink=? ''', (reString,))
			conn.commit()
			continue
		conn.commit()

		#Pulls up the indeed page for the current job
		driver2.get(reString)
		
		#Stores the job link in the current job
		currentJob.jobLink = reString

		#Stores the job description
		try:
			currentJob.description = driver2.find_element_by_class_name("jobsearch-jobDescriptionText").text
		except:
			continue

		#Checks to make sure the current job's page loaded correctly
		if BeautifulSoup(driver2.page_source, "html.parser").find("title") == None:
			driver2.quit()
			driver2 = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)
			driver2.delete_all_cookies()
			driver2.get(reString)
		
		if ("hCaptcha" in BeautifulSoup(driver2.page_source, "html.parser").find("title").text):
			input("Press something once captcha is solved: ")

		pageSource = driver2.page_source

		#Finds the job title
		reString = '"jobTitle":"(.*?)","openCompanyLinksInNewTab"'
		currentJob.jobTitle = "".join(re.findall(reString, pageSource))

		#Finds the job salary
		currentJob.AddSalary(pageSource)

		#Finds the job-type(full-time/part-time, permanent/temporary, remote/in-person)
		if "Full-time" in pageSource:
			currentJob.fullTime = 1

		if "Permanent" in pageSource:
			currentJob.permanent = 1

		if "REMOTE_COVID_TEMPORARY" in pageSource:
			currentJob.remote = 1

		elif "REMOTE_ALWAYS" in pageSource:
			currentJob.remote = 2

		#Finds the date the job was posted
		date_match = re.search('postedDate=([0-9]{4})-([0-9]{2})-([0-9]{2})', pageSource)
		if(date_match):
			currentJob.yearPosted = int(date_match.group(1))
			currentJob.monthPosted = int(date_match.group(2))
			currentJob.dayPosted = int(date_match.group(3))


		#Finds the company name
		reString = '"companyName":"([a-zA-Z]* *[a-zA-Z]*)"'

		#If a company name was found, add it to the current job, then start finding info on that company if it isn't in the database already 
		if (re.search(reString, pageSource)):
			currentJob.company_name = re.search(reString, pageSource).group(1)

			#If the company isn't already in the dictionary
			#Asks if there isn't any returns of "True" from the list comprehension
			#It returns true if the v.name (the name variable of the value from companies_dict, where each value is a Company Object) == current_job.company_name
			if not any([True for k, v in config.companies_dict.items() if v.name == currentJob.company_name]):
				currentCompany.name = currentJob.company_name

				try:
					currentCompany.overallRating = float(re.search('"rating":([0-9.]+)', pageSource).group(1))
				except:
					pass

				if currentCompany.overallRating:

					#Opens the companies page to get ratings from it
					re_str = r'"companyOverviewLink":"https:\\u002F\\u002Fca\.indeed\.com\\u002Fcmp\\u002F(.*?)\?.*?",'
					reString = 'https://ca.indeed.com/cmp/' + re.search(re_str, pageSource).group(1)
					current_id_req = requests.get(reString)

					pageSource = current_id_req.text
					current_id_req.close()

					reString = '{"totalReviews":"([0-9.]+K?)"}},"reviewCategories":{"compensationBenefits":([0-9.]+),"culture":([0-9.]+),"jobSecurityAdvancement":([0-9.]+),"management":([0-9.]+),"workLifeBalance":([0-9.]+)}}'
					rating_matches = re.search(reString, pageSource)
					if rating_matches:
						if 'K' in rating_matches.group(1):
							currentCompany.numberOfRating = int(float(rating_matches.group(1).replace('K', ''))*1000)
						else:
							currentCompany.numberOfRating = int(rating_matches.group(1))
						currentCompany.compensationRating = float(rating_matches.group(2))
						currentCompany.cultureRating = float(rating_matches.group(3))
						currentCompany.securityAdvancementRating = float(rating_matches.group(4))
						currentCompany.managementRating = float(rating_matches.group(5))
						currentCompany.workLifeBalanceRating = float(rating_matches.group(6))
					else:
						rating_matches = re.search('"reviewCount":([0-9.]+K?)', pageSource)
						if rating_matches:
							if 'K' in rating_matches.group(1):
								currentCompany.numberOfRating = int(float(rating_matches.group(1).replace('K', ''))*1000)
							else:
								currentCompany.numberOfRating = int(rating_matches.group(1))

				#Puts the current company into the list of companies
				config.companies_dict[config.number_of_companies] = currentCompany
				config.number_of_companies += 1

		config.jobDict[config.number_of_jobs] = currentJob
		config.number_of_jobs += 1

	#Updates the file with the last 15 jobs and companies
	FileWriter.writeJobsToFile()
	FileWriter.writeCompaniesToFile()

	#Gets the next page of results
	DriverFunctions.gotoNextPageResults(driver)

	#Ends infinite loop if the next page of results can't be accessed
	if config.fully_done:
		driver.quit()
		driver2.quit()
		break


#Updates which jobs are still active in the database based on which jobs were detected in the most recent run of the program
jobLinks = cur.execute(''' SELECT jobLink FROM Jobs WHERE stillActive = 1''').fetchall()
conn.commit()
for jobLink in jobLinks:
	if jobLink[0] not in config.idList:
		cur.execute(''' UPDATE Jobs SET stillActive = 0 WHERE jobLink=? ''', (jobLink[0],))

conn.commit()

