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


#We need 51 separate URLS for this one. Queries need to be constructed like this: q=%22New+York%22&page=0
#Note, the search function is very loose and when you type Washington, it also returns people with the last name Washington. It doesn't actually pay attention to location
#However, you can clean the data later and drop duplicates if this query/download method doesn't just update an existing file down the road

# Note: when viewing the search result pages, the HTML only displays 20 pages for results. You can go past page 20 by manually changing the page number in the URL, making it difficult to actually know how many pages there are in the scrape. We'll default to 1000 to make sure we get everything

# Note: when combing through the pages, the http GET structure starts with page=0 (think how Python handles indices)
baseurl = ['http://names.lawmemorial.org/search.html#q=']

#Similar to script used on the Officer Down Memorial Page, collecting same data, basically
#list of states
states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado', 'Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho', 'Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana', 'Maine' 'Maryland','Massachusetts','Michigan','Minnesota', 'Mississippi', 'Missouri','Montana','Nebraska','Nevada', 'New Hampshire','New Jersey','New Mexico','New York', 'North Carolina','North Dakota','Ohio', 'Oklahoma','Oregon','Pennsylvania','Rhode Island', 'South Carolina','South Dakota','Tennessee','Texas','Utah', 'Vermont','Virginia','Washington','West Virginia', 'Wisconsin','Wyoming', 'Washington D.C.', 'Puerto Rico', 'Guam']
#empty state list that will be appended to add %22 to beginning and ending of each state because that's the boolean notation in the url to match exact phrase
states2 = []
# Append each state to the baseurl and add to a list
stateurl = []
# URLs to scrape
urls = []
# Search URL: http://names.lawmemorial.org/search.html#q=
# FULL SEARCH URL: http://names.lawmemorial.org/search.html#q=%22New+York%22&page=0

# We'll want to use sleep(INTEGER) so we don't DDOS the the website

#The site's search function doesn't work properly via blanket GET request.
#Need to use Selenium to load the HTML and then save it. Get request links later for data
driver = webdriver.Firefox()

#function that runs a For loop to generate the URLs to scrape. Save this to a JSON file for easier scraping later
def statelist():

	for x in states: 
		update = '"' + x +  '"'
		# replace = x.replace(' ', '+')
		# update = '&22' + replace + '%22'
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

# function to download html of search pages to local directory, also sets the naming
#Requests won't work on this page, will need to do selenium && request
def run(state):
	print('opening page')
	driver.get("http://names.lawmemorial.org/search.html?q=")
	sleep(2)
	driver.find_element_by_name("query").send_keys(state)
	driver.find_element_by_class_name("query-submit").click()
	print('query submitted')
	sleep(3)
	html = driver.page_source
	with open('nleo_mem_fund_search/' + html, 'w', encoding='utf8') as file:
		file.write(r.text)
		print('wrote file: ')
	# print(html)


	# r = requests.get(url)
	# # Declare naming convention. In this case, it will be named using the url contents after the '?'
	
	#name=  'query'
	# class_name= 'query-submit'

	# name = url.split('/')[-1].split('#')[-1] + '.html'
	# with open('nleo_mem_fund_search/' + name, 'w', encoding='utf8') as file:
	# 	# If you don't include the encoding parameter, you'll run into an error eventually
	# 	file.write(r.text)
	# 	print('wrote file: ' + str(name))



#Create list of URLs to scrape
statelist()
#Check to see query construction worked
# pp(states2)
# pp(stateurl)

# call url list construction function
urllist()
# pp(urls)
# pp(len(urls))


#Run the function that saves the urls to a local json file
# urls_to_json(stateurl, 'lawmemorial_links')
# urls_to_json(urls, 'all_law_mem_links')

#Call 'run' function, use sleep so we don't get blocked
# for state in states[0]:
# 	run(state)
# 	print('Saved page')
# 	sleep(4)

run(states2[0])
#Call 'run' function for specific URL index range, useful if an error is thrown during your scraping. 
# for url in urls[462:]:
# 	run(url)
# 	print('Saved page')
# 	sleep(4)

# If your code throws an error during the scraping, search for the last file written (it'll probably be incomplete)
# Grab the name of that incomplete file, add the full URL, run this print command to get the index position of where you left off. This one will return 462
# With index in hand, call the 'run' function again and start from url position 462, give the function a range
# print(urls.index('https://www.odmp.org/search?from=1951&to=2000&o=100'))



# String url = webdriver.getCurrentUrl();
# Then, all you have to do is replace old guid with a new guid.

# int numOfChars = 36;
# int posOfQuestionMark = url.indexOf("?");
# String newGuid = "..."; // put new/wrong guid value here
# String newUrl = url.substring(0, posOfQuestionMark-numOfChars)+newGuid+url.substring(posOfQuestionMark);
# --Edit--

# Now, load this new url in the browser.

# webdriver.get(newUrl);