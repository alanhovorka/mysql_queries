from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pyquery import PyQuery as pq

driver = webdriver.Firefox()
# open page to released inmates incarcarated for sex crimes
# driver.get("http://offender.fdle.state.fl.us/offender/offenderSearchNav.do?link=advanced")

names = [
	("Aristide", "Smith"), # Smith is first name
	("Murray", "Jonathan"),
	("Breitberg", "Bleiweiss")
	]

def checkName(nametuple):
	#firstname = driver.find_element_by_name("firstName")
	# open page to released inmates incarcarated for sex crimes
	driver.get("http://offender.fdle.state.fl.us/offender/offenderSearchNav.do?link=advanced")
	sleep(2)
	lastname, firstname = nametuple
	print("Attempting to find " + firstname + " " + lastname)
	driver.find_element_by_name("firstName").send_keys(firstname)
	driver.find_element_by_name("lastName").send_keys(lastname)
	driver.find_element_by_xpath("/html/body/div/div/div/div/div/form/table/tbody/tr[7]/td[2]/a").click()
	sleep(2)
	html = driver.page_source
	# print(html)
	for personrow in pq(html)("tr.ResultRow"):
		print(pq(pq(personrow)("td")[2])("p")[0].text)
	return
	  
for name in names:
	checkName(name)
	
