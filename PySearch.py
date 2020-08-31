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
import smtplib

# Read from json file
# open json via sys arg?
# settingsFile = sys.argv[2]
with open("seed-file.json", "r") as f:
    site_data = json.load(f)
# print("site_data", site_data)
# print("f", f)

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
    for calList in site_data["cal"]:
        # print(calList.get('url'))
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
    time.sleep(3)
    # Handle displayed stock
    stockRead(itemName)


def stockRead(itemName):  # Handle results - Log "out of stock" dates
    timeStamp = datetime.now()

    print('Reading product information.......')
    print('On item: % s' %
          (itemName))

    # See if any products are displayed
    try:  # Search for list items on the product-list element
        items = driver.find_element_by_xpath(
            '//ul[@class="product-list"]/li').is_displayed()
        print('% s is IN stock! \n' %
              (itemName))

        # Scrape information of IN STOCK items (func?)
        stockScrape(itemName, items)

    # If no items are displayed, add the timestamp and item to the backlog.
    except NoSuchElementException:
        print('% s is OUT of stock! \n' %
              (itemName))
        output_file.write('Item % s is out of stock as of % s \n' %
                          (itemName, timeStamp))


def stockScrape(itemName, items):
    print("Gathering item info!")
    # Send email function
    stockEmail()

# stockEmail params? itemName, totalPrice, indPrice


def stockEmail():  # Email functionality
    print("Sending email with in-stock product information....")

    # Get login information
    emailName = site_data["emailCreds"][0]["username"]
    emailPass = site_data["emailCreds"][0]["password"]
    print('emailName', emailName)
    print('emailPass', emailPass)

    # Email recipient
    toEmail = site_data["emailRec"]

    # Create session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(emailName, emailPass)

    # Build email
    emailBody = "This is a test"
    emailSubject = ("Stock Results on % s" % datetime.now())

    headers = "\r\n".join(
        ["from: " + emailName, "subject: " + emailSubject, "to: " + toEmail, "mine-version: 1.0", "content-type: text/html"])

    content = headers + "\r\n\r\n" + emailBody

    # Sent email
    s.sendmail(emailName, toEmail, content)
    s.quit()

    print("Email sent successfully")


siteLoop()
print("Done looking for ammo!!")

output_file.write('Done searching on % s \n' % (datetime.now()))

# Sleep timer for 4 hours

# Repeat functions
