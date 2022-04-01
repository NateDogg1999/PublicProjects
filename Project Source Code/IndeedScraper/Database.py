import config
import sqlite3
import re
import keywordFinder
from datetime import datetime


config.i = 0
conn = sqlite3.connect('jobdb.sqlite')

cur = conn.cursor()


cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Jobs' ''')


if(cur.fetchone()[0] == 0):
	cur.execute(''' CREATE TABLE Jobs (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, jobTitle TEXT, salary REAL, permanent INTEGER, 
	fullTime INTEGER, remote INTEGER, jobLink TEXT UNIQUE, yearPosted INTEGER, monthPosted INTEGER, dayPosted INTEGER, companies_id INTEGER, 
	date TEXT, stillActive INTEGER, description TEXT) ''')

	

cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Companies' ''')

if(cur.fetchone()[0] == 0):
	cur.execute(''' CREATE TABLE Companies (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT, overallRating REAL, numberOfRating INTEGER, 
	compensationRating REAL, cultureRating REAL, securityAdvancementRating REAL, managementRating REAL, workLifeBalanceRating REAL) ''')

	

cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Metadata' ''')

if(cur.fetchone()[0] == 0):
	cur.execute(''' CREATE TABLE Metadata (date TEXT, numberOfJobs INTEGER, meanSalary REAL, numberOfCompanies INTEGER, 
	proportionPermanent REAL, proportionFullTime REAL, proportionRemote REAL, meanRating REAL, meanCompensationRating REAL, proportionCompanyJob REAL, numberStillActive INTEGER) ''')


companyDataHandle = open("indeedCompanies.txt", "r")
for line in companyDataHandle:
	config.i += 1
	re_str = '[0-9]+: name: "(.*)" overallRating: (None|[0-9.]+) numberOfRating: (None|[0-9]+) compensationRating: (None|[0-9.]+) cultureRating: (None|[0-9.]+) securityAdvancementRating: (None|[0-9.]+) managementRating: (None|[0-9.]+) workLifeBalanceRating: (None|[0-9.]+)'
	cM = re.search(re_str, line)

	cur.execute(''' SELECT name FROM Companies WHERE name=? ''', (cM.group(1),))
	if not cur.fetchone():
		cur.execute(''' INSERT INTO Companies (name, overallRating, numberOfRating, 
		compensationRating, cultureRating, securityAdvancementRating, managementRating, workLifeBalanceRating) 
		VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (cM.group(1), cM.group(2), cM.group(3), cM.group(4), cM.group(5), cM.group(6), cM.group(7), cM.group(8)))

	if not config.i%10:
		conn.commit()

conn.commit()
companyDataHandle.close()
config.i = 0


jobDataHandle = open("indeedJobs.txt", "r", encoding="utf-8")
re_str = r'''jobTitle: "(.*)" salary: (None|[0-9.]+) company_name: (.*) permanent: (-1|1) fullTime: (-1|[0-9]) remote: (-1|[0-9]) jobLink: (.*) yearPosted: (None|[0-9]+) monthPosted: (None|[0-9]+) dayPosted: (None|[0-9]+) description: ([\s\S]*?)[0-9]+: '''
jMs = re.findall(re_str, jobDataHandle.read())

for jM in jMs:
	config.i += 1

	cur.execute(''' SELECT id FROM Companies WHERE name=? ''', (jM[2],))
	try:
		companies_id = cur.fetchone()[0]
	except:
		companies_id = None

	cur.execute(''' INSERT OR IGNORE INTO Jobs (jobTitle, salary, permanent, fullTime, 
			remote, jobLink, yearPosted, monthPosted, dayPosted, companies_id, date, stillActive, description) 
			VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date('now', 'localtime'), 1, ?)''', (jM[0], jM[1], jM[3], jM[4], jM[5], jM[6], jM[7], jM[8], jM[9], companies_id, jM[10]))

	if not config.i%10:
		conn.commit()

jobDataHandle.close()
config.i = 0
conn.commit()

keywordFinder.FindKeywords()



#Find metadata
tableValues = cur.execute(''' SELECT salary, permanent, fullTime, remote FROM Jobs ''').fetchall()
conn.commit()

sum = 0
meanCount = 0
permanentCount = 0
fullTimeCount = 0
remoteCount = 0

for tableValue in tableValues:
	if tableValue[0] != 'None':
		sum += tableValue[0]
		meanCount += 1

	if tableValue[1] == 1:
		permanentCount += 1

	if tableValue[2] == 1:
		fullTimeCount += 1

	if tableValue[3] == 1 or tableValue[3] == 2:
		remoteCount += 1


tableValues = cur.execute(''' SELECT overallRating, compensationRating FROM Companies ''').fetchall()
conn.commit()

sumOverall = 0
meanOverallCount = 0
sumComp = 0
meanComp = 0

for tableValue in tableValues:
	if tableValue[0] != 'None':
		sumOverall += tableValue[0]
		meanOverallCount += 1

	if tableValue[1] != 'None':
		sumComp += tableValue[1]
		meanComp += 1



numberOfJobs = cur.execute(''' SELECT COUNT(*) FROM Jobs ''').fetchone()[0]
numberOfCompanies = cur.execute(''' SELECT COUNT(*) FROM Companies ''').fetchone()[0]
meanSalary = sum/meanCount
proportionPermanent = permanentCount/numberOfJobs
proportionFullTime = fullTimeCount/numberOfJobs
proportionRemote = remoteCount/numberOfJobs
proportionCompanyJob = numberOfCompanies/numberOfJobs
meanRating = sumOverall/meanOverallCount
meanCompensationRating = sumComp/meanComp
numberStillActive = cur.execute(''' SELECT COUNT() FROM Jobs WHERE stillActive = 1''').fetchone()[0]


if cur.execute(''' SELECT date FROM Metadata WHERE date = date('now', 'localtime') ''').fetchone():
	cur.execute(''' UPDATE Metadata SET numberOfJobs = ?, meanSalary = ?, numberOfCompanies = ?, 
	proportionPermanent = ?, proportionFullTime = ?, proportionRemote = ?, meanRating = ?, meanCompensationRating = ?, 
	proportionCompanyJob = ?, numberStillActive = ? WHERE date = date('now', 'localtime')''', (numberOfJobs, meanSalary, numberOfCompanies, proportionPermanent, proportionFullTime, proportionRemote, meanRating, meanCompensationRating, proportionCompanyJob, numberStillActive))
else:
	cur.execute(''' INSERT INTO Metadata (date, numberOfJobs, meanSalary, numberOfCompanies, 
	proportionPermanent, proportionFullTime, proportionRemote, meanRating, meanCompensationRating, 
	proportionCompanyJob, numberStillActive) VALUES (date('now', 'localtime'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	''', (numberOfJobs, meanSalary, numberOfCompanies, proportionPermanent, proportionFullTime, proportionRemote, meanRating, meanCompensationRating, proportionCompanyJob, numberStillActive))

conn.commit()

keywordFinder.CountKeywords()


