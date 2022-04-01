import config


def writeJobsToFile():
		output = open("indeedJobs.txt", "a", encoding="utf-8")
		if config.x == 0:
			output.write(f"{config.x}: ")
			config.x += 1
		for job in range(config.i, config.number_of_jobs):
			
			output.write(f'''jobTitle: \"{config.jobDict[config.i].jobTitle}\" \
salary: {config.jobDict[config.i].salary} company_name: {config.jobDict[config.i].company_name} \
permanent: {config.jobDict[config.i].permanent} fullTime: {config.jobDict[config.i].fullTime} \
remote: {config.jobDict[config.i].remote} jobLink: {config.jobDict[config.i].jobLink} \
yearPosted: {config.jobDict[config.i].yearPosted} monthPosted: {config.jobDict[config.i].monthPosted} \
dayPosted: {config.jobDict[config.i].dayPosted} description: {config.jobDict[config.i].description}\n{config.x}: ''')
			config.x += 1
			config.i += 1
			
		output.close()


def writeCompaniesToFile():
		output = open("indeedCompanies.txt", "a")
		for company in range(config.j, config.number_of_companies):
			output.write(f'''{config.j}: name: \"{config.companies_dict[config.j].name}\" \
overallRating: {config.companies_dict[config.j].overallRating} \
numberOfRating: {config.companies_dict[config.j].numberOfRating} \
compensationRating: {config.companies_dict[config.j].compensationRating} \
cultureRating: {config.companies_dict[config.j].cultureRating} \
securityAdvancementRating: {config.companies_dict[config.j].securityAdvancementRating} \
managementRating: {config.companies_dict[config.j].managementRating} \
workLifeBalanceRating: {config.companies_dict[config.j].workLifeBalanceRating}\n''')
			config.j += 1
	
		output.close()