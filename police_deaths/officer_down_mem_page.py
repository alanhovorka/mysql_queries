from bs4 import BeautifulSoup
import os
from glob import glob
from time import sleep
from pprint import pprint as pp
import csv
import requests
import json

#Declare empty list that will store top level death details
cops = []
#Declare empty list that will store urls to death entry details
cop_details = []
# URLs to scrape
urls = []
# Search URL https://www.odmp.org/search?
# FULL SEARCH URL: https://www.odmp.org/search?name=&agency=&state=&from=1791&to=1791&cause=&filter=all
#We can just get four URLs and then just click through the list and get the listings for each dead cop
# In reality, the differnet pages aren't don't require Selenium because of how the URL works.
# A combo of request + BS4 will get us what we need. 
# https://www.odmp.org/search?from=1900&to=1951&o=100


# Here's our year range that website will accept. 
#It breaks if you select a year range with too many results
#1791 through 1900, 2050 (2066 results)
#1901 through 1950, 9350 (9363 results)
#1951 through 2000, 8975 (8903 results)
#2001 through 2017, 2950 (2748 results)
# This list contains our base urls for our scraping. We'll loop through each item like 1000 times to get a list of URLs that fill in o=''.
# o='' must be a multiple of 25, starting at 0
baseurl = ['https://www.odmp.org/search?from=1791&to=1900&o=','https://www.odmp.org/search?from=1901&to=1950&o=', 'https://www.odmp.org/search?from=1951&to=2000&o=', 'https://www.odmp.org/search?from=2001&to=2017&o=']

#The function will go to the search page and pull all of the 
#Pull the info contained in the table body
#Top level tag is <table>, then <tbody>, then <tr>
#The data is contained in <td valign =  "top" ... >
#Inside td tag with valign value "top", the data is stored as <p> tags separated by <br>

# We'll want to use sleep(INTEGER) so we don't DDOS the the website

# mulp25 = [x for x in range(0,9351,25)]

#function that runs a For loop to generate the URLs to scrape. Save this to a JSON file for easier scraping later
def urllist():
	for url in baseurl:
		if url == 'https://www.odmp.org/search?from=1791&to=1900&o=':
			for w in range(0, 2051, 25):
				newurl = url + str(w)
				urls.append(newurl)
		elif url == 'https://www.odmp.org/search?from=1901&to=1950&o=':
			for x in range(0, 9351, 25):
				newurl = url + str(x)
				urls.append(newurl)
		elif url == 'https://www.odmp.org/search?from=1951&to=2000&o=':
			for y in range(0, 8975, 25):
				newurl = url + str(y)
				urls.append(newurl)
		elif url == 'https://www.odmp.org/search?from=2001&to=2017&o=':
			for z in range(0, 2950, 25):
				newurl = url + str(z)
				urls.append(newurl)
		else:
			pass

# function to write the urls list variable to a local json file for scraping. Run this to save the data locally for posterity. 
def urls_to_json(url_list):
	with open('data.json', 'w') as outfile:
		json.dump(url_list, outfile)

# function to download html of search pages to local directory, also sets the naming

def run(url):
	r = requests.get(url)
	# Declare naming convention. In this case, it will be named using the url contents after the '?'
	name = url.split('/')[-1].split('?')[-1]
	with open('search_results/' + name, 'w') as file:
		file.write(r.text)


#Create list of URLs to scrape
urllist()

# pp(urls)
# pp(len(urls))
#This should return a list of the urls to scrape. Their should be 935 urls to scrape. Each url will have about 25 data entries to scrape, with about four or five possible columns of data.
#This comes out to about 23,000 police deaths, may include K9 units.
# When accounting for columns, the final scrape should produce about one million cells (23000 rows * 4 OR 23000 * 5)

#Run the function that saves the urls to a local json file
# urls_to_json(urls)

#Run download function, use sleep so we don't get blocked
for url in urls:
	run(url)
	print('Saved page')
	sleep(10)