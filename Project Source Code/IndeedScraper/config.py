import re

class company:
	name = None
	overallRating = None
	numberOfRating = None
	compensationRating = None
	cultureRating = None
	securityAdvancementRating = None
	managementRating = None
	workLifeBalanceRating = None



class job:
	jobTitle = None
	salary = None
	company_name = None
	permanent = -1
	fullTime = -1
	remote = -1
	jobLink = None
	yearPosted = None
	monthPosted = None
	dayPosted = None
	description = None

	def AddSalary(self, pageSource):
		salary_match = re.search('"salaryText":"\$([0-9]+.?[0-9]*) - \$([0-9]+.?[0-9]*) .*? (hour|year)', pageSource)
		if(salary_match):
	
			salary1 = float(salary_match.group(1).replace(',', ''))
			salary2 = float(salary_match.group(2).replace(',', ''))
			salary = (salary1 + salary2)/2
	
			if('year' in salary_match.group(3)):
				salary = salary/1920
	
			self.salary = salary
			return
	
		if(re.search('"salaryText":"\$([0-9]+.?[0-9]*) .*? (hour|year)', pageSource)):
	
			salary = float(re.search('"salaryText":"\$([0-9]+.?[0-9]*) .*? (hour|year)', pageSource).group(1).replace(',', ''))
	
			if('year' in re.search('"salaryText":"\$([0-9]+.?[0-9]*) .*? (hour|year)', pageSource).group(2)):
				salary = salary/1920
	
			self.salary = salary


companies_dict = {}
jobDict = {}
idList = []
number_of_jobs = 0
number_of_companies = 0
xpath = 7
actually_done_countdown = 0
fully_done = False
startTime = None
i = 0
j = 0
x = 0
