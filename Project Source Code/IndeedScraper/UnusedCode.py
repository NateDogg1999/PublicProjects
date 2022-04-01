
reString = "https://www.google.com/search?q=indeed+job+search+canada"
indeed_req = driver.get(reString)

#Tries to click on ca.indeed.com, and if it fails, tries a different xpath
try:
	driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="main"]/div[4]/div/div[1]/a'))
except:
	driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div/div/div[1]/a'))

if "hCaptcha" in BeautifulSoup(driver.page_source, "html.parser").find("title").text:
	input("Press something once captcha is solved: ")

#Writes 'programmer' and 'Victoria, BC' into the search
driver.find_element_by_id('text-input-what').send_keys('programmer')
driver.find_element_by_id('text-input-where').send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, 'Victoria, BC', Keys.ENTER)
