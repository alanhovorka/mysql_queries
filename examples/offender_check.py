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

names = [PUT NAMES OF PERSONS HERE]

def checkName(nametuple):
    text_file = open("A-Matches.txt", "w")
    #firstname = driver.find_element_by_name("firstName")
    # open page to released inmates incarcarated for sex crimes
    driver.get("http://offender.fdle.state.fl.us/offender/offenderSearchNav.do?link=advanced")
    sleep(4)
    lastname, firstname = nametuple
    text_file.write("Attempting to find " + firstname + " " + lastname)
    driver.find_element_by_name("firstName").send_keys(firstname)
    driver.find_element_by_name("lastName").send_keys(lastname)
    driver.find_element_by_xpath("/html/body/div/div/div/div/div/form/table/tbody/tr[7]/td[2]/a").click()
    sleep(4)
    #present = driver.find_element_by_class_name("ResultsPhoto")
    try:
        notpresent = driver.find_element_by_class_name("error-text")
        if notpresent:
            text_file.write("Not Present")
    except:
        text_file.write("Present")
    html = driver.page_source
    # print(html)
    for personrow in pq(html)("tr.ResultRow"):
        print(pq(pq(personrow)("td")[2])("p")[0].text)
    return

    text_file.close()
      
for name in names:
    checkName(name)