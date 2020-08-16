# Imports
import string
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import sys
import json
from selenium.common.exceptions import NoSuchElementException

# Read from json file
# open json via sys arg?
# settingsFile = sys.argv[2]
with open("seed-file.json", "r") as f:
    site_data = json.load(f)
print("site_data", site_data)
print("f", f)

# Establish web driver
driver = webdriver.Chrome()

# Initialize log file
output_file = open('backlog.txt', 'a')

try:
    assert len(site_data)
    print("JSON data present")
except AssertionError:
    print("Error with JSON data")


def siteLoop():
    for calList in site_data["caliber"]:
        print(calList.get('url'))
        urlKeyword = calList.get('url')
        nameKeyword = calList.get('name')
        # print('nameKeyword', nameKeyword)
        webFunc(urlKeyword, nameKeyword)


def webFunc(urlHalf, itemName):  # Handle site and validation for correct page

    # Browser instance, navigation and check for correct page Title
    testUrl = (site_data["site"] + urlHalf)
    print(testUrl)

    driver.get(testUrl)

    pageTitle = driver.title
    print(pageTitle)

    # Verify correct page has loaded.
    try:
        assert site_data["title"] in driver.title
        print('Correct Page!')
    except AssertionError:
        print("Page Error!")

    # Wait to give modal time to display
    time.sleep(6)

    # Handle popup and target "in stock" only
    # Check for modal, close if present.
    try:
        modal = driver.find_element_by_class_name(site_data["targetClass"])
        modal.click()
        print("Closed That Damn Modal")
    except:
        print("No Signup Modal")

    # Sort by "in stock"
    driver.find_element_by_id(site_data["targetID"]).click()

    # Handle displayed stock
    stockRead(itemName)


def stockRead(itemName):  # Handle results - Log "out of stock" dates
    # timeStamp = datetime.now()
    dfa = driver.find_element_by_class_name("product-list")
    try:
        driver.find_element_by_xpath(
            '//ul[@class="product-list"]/li')
        print("Found stock")
    except NoSuchElementException:
        print('No stock!')
        # listBody = site_data["productList"]
        # listBodyXPath = driver.find_elements_by_xpath(listBody)
        # print("listBody", listBodyXPath)
        # targetPath = listBodyXPath.find_elements_by_xpath("//*[li()]")
        # print('targetPath', targetPath)
        # print('Reading product information.......')
        # print('On item: % s \n' %
        #       (itemName))
        # try resultItems = driver.find_element_by_id():
        #     print('In stock!!')
        # else:
        #     print('No Items Available')
        # output_file.write('Item % s is out of stock as of % s \n' %
        #                   (itemName, timeStamp))


siteLoop()

# print("Running Main Function...")
# webFunc()
# mainFunc()

# with open("test-data2.json", "r") as f:
#     settings_dict = json.load(f)
# print(settings_dict)
# webFunc()
# contentFilter()
# mainFunc()
# print("Second Test Completed!")
