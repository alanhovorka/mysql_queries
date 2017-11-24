from bs4 import BeautifulSoup
import os
from glob import glob
#grab all of the files in a directory and put them in a list
from time import sleep
from pprint import pprint as pp
#prints pretty
import csv
import requests
import json

#Similar to script used on the Officer Down Memorial Page, collecting same data, basically

states = []
stateurl = []
# URLs to scrape
urls = []
# Search URL: http://names.lawmemorial.org/search.html#q=
# FULL SEARCH URL: http://names.lawmemorial.org/search.html#q=%22New+York%22&page=0

#We need 51 separate URLS for this one. Queries need to be constructed like this: q=%22New+York%22&page=0
#Note, this http GET is very loose and when you type Washington, it also returns people with the last name Washington. It doesn't actually pay attention to location
#However, you can clean the data later and drop duplicates if this query/download method doesn't just update an existing file down the road

# Note: when viewing the search result pages, the HTML only displays 20 pages for results. You can go past page 20 by manually changing the page number in the URL, making it difficult to actually know how many pages there are in the scrape. We'll default to 1000 to make sure we get everything

# Note: when combing through the pages, the http GET structure starts with page=0 (think how Python handles indices)
baseurl = ['http://names.lawmemorial.org/search.html#q=']

# We'll want to use sleep(INTEGER) so we don't DDOS the the website

#function that runs a For loop to generate the URLs to scrape. Save this to a JSON file for easier scraping later
def statelist():
	for url in baseurl:
		for state in states:
			newurl = url + state
			stateurl.append(newurl)

def urllist():
	for urlstate in stateurl:
		for x in range(0, 2000, 1):
			newurl = urlstate + '&page=' + str(x)
			urls.append(newurl)

# function to write the urls list variable to a local json file for scraping. Run this to save the data locally for posterity. 
def urls_to_json(url_list):
	with open('data.json', 'w') as outfile:
		json.dump(url_list, outfile)

# function to download html of search pages to local directory, also sets the naming

def run(url):
	r = requests.get(url)
	# Declare naming convention. In this case, it will be named using the url contents after the '?'
	name = url.split('/')[-1].split('?')[-1] + '.html'
	with open('search_results/' + name, 'w', encoding='utf8') as file:
		# If you don't include the encoding parameter, you'll run into an error eventually
		file.write(r.text)
		print('wrote file: ' + str(name))



#Create list of URLs to scrape
statelist()
urllist()

# pp(urls)
# pp(len(urls))
#This should return a list of the urls to scrape. Their should be 935 urls to scrape. Each url will have about 25 data entries to scrape, with about four or five possible columns of data.
#This comes out to about 23,000 police deaths, may include K9 units.
# When accounting for columns, the final scrape should produce about one million cells (23000 rows * 4 OR 23000 * 5)
# pp() = pretty printing library to make print statements readable for large amounts of data


#Run the function that saves the urls to a local json file
# urls_to_json(urls)

#Call 'run' function, use sleep so we don't get blocked
# for url in urls:
# 	run(url)
# 	print('Saved page')
# 	sleep(4)

#Call 'run' function for specific URL index range, useful if an error is thrown during your scraping. 
for url in urls[462:]:
	run(url)
	print('Saved page')
	sleep(4)

# If your code throws an error during the scraping, search for the last file written (it'll probably be incomplete)
# Grab the name of that incomplete file, add the full URL, run this print command to get the index position of where you left off. This one will return 462
# With index in hand, call the 'run' function again and start from url position 462, give the function a range
# print(urls.index('https://www.odmp.org/search?from=1951&to=2000&o=100'))
