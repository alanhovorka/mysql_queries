import os
from glob import glob
#grab all of the files in a directory and put them in a list
from pprint import pprint as pp
#prints pretty
import csv
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pyquery import PyQuery as pq

#We're searching the National Law Enforcement Officer Memorial Fund for details about police deaths
#We will run a Selenium script that will iterate through each year from 1791 to 2016 for death details

#We need 51 separate URLS for this one. Queries need to be constructed like this: q=%22New+York%22&page=0
#Note, the search function is very loose and when you type Washington, it also returns people with the last name Washington. It doesn't actually pay attention to location
#However, you can clean the data later and drop duplicates if this query/download method doesn't just update an existing file down the road

# Note: when viewing the search result pages, the HTML only displays 20 pages for results. You can go past page 20 by manually changing the page number in the URL, making it difficult to actually know how many pages there are in the scrape. We'll default to 1000 to make sure we get everything

# Note: when combing through the pages, the http GET structure starts with page=0 (think how Python handles indices)

# We'll want to use sleep(INTEGER) so we don't DDOS the the website

baseurl = ['http://names.lawmemorial.org/search.html#q=']
#list of states
states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado', 'Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho', 'Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana', 'Maine' 'Maryland','Massachusetts','Michigan','Minnesota', 'Mississippi', 'Missouri','Montana','Nebraska','Nevada', 'New Hampshire','New Jersey','New Mexico','New York', 'North Carolina','North Dakota','Ohio', 'Oklahoma','Oregon','Pennsylvania','Rhode Island', 'South Carolina','South Dakota','Tennessee','Texas','Utah', 'Vermont','Virginia','Washington','West Virginia', 'Wisconsin','Wyoming', 'Washington D.C.', 'Puerto Rico', 'Guam']
states2 = []
stateurl = []
years = []
pages = []
#urls to scrape
urls = []
# Search URL: http://names.lawmemorial.org/search.html#q=
# FULL SEARCH URL: http://names.lawmemorial.org/search.html#q=%22New+York%22&page=0
driver  = webdriver.Firefox()

# We can search for officer details in a couple of ways, years appears to be the most veriable because of the organization's total deaths by year pdf. We can cross reference the scrape with this.
# Will need to return the 'results' number in the HTML

# Functions to do stuff

def statelist():
	for x in states: 
		update = '"' + x +  '"'
		states2.append(update)
	for url in baseurl:
		for string in states2:
			newurl = url + string
			stateurl.append(newurl)

def urllist():
	for urlstate in stateurl:
		for x in range(0, 351, 1):
			newurl = urlstate + '&page=' + str(x)
			urls.append(newurl)

# function to write the urls list variable to a local json file for scraping. Run this to save the data locally for posterity. 
def urls_to_json(url_list, name):
	with open(name + '.json', 'w') as outfile:
		json.dump(url_list, outfile)

def yearlist():
	for x in range(1791, 2018, 1):
		year = x
		years.append(year)

def pagelist():
	for x in range(0, 300, 1):
		page = x
		pages.append(page)

def run(year):
	driver.get('http://names.lawmemorial.org/search.html#q=')
	sleep(2)
	driver.find_element_by_name("query").send_keys(year)
	driver.find_element_by_class_name("query-submit").click()
	print('query submitted')
	sleep(3)
	html = driver.page_source
	# for deaths in pq(html)('table.results-list'):
	# 	print(pq(pq(deaths)('td.result-body')('a.src')).text)
	# 	print(pq(pq(deaths)('td.result-body')('a')).text)
	# 	print(pq(pq(deaths)('td.result-body')('p')).text)
	name = driver.find_element_by_class_name('result-link-section')
	result = driver.find_element_by_xpath('//*[@id="search-result-section"]/table/tbody/tr[1]/td[2]/div[1]')
	desc = driver.find_element_by_class_name('result-description')
	print(name)
	print(result)
	print(desc)
	driver.quit()
	# We can edit this to click through each of these death links and pull more data. driver.find_element_by_xpath("/html/body/div/div/div/div/div/form/table/tbody/tr[7]/td[2]/a").click()


yearlist()
pagelist()

run(years[0])

#for year in years:
	# run(year)
	# print('saved page')
	# sleep(4)
