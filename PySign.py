
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
with open("seed-file.json", "r") as f:
    site_data = json.load(f)

# Initialize log file
output_file = open('signup.txt', 'a')

# Establish web driver
driver = webdriver.Chrome()

# Defining timestamp var
timeStamp = datetime.now()

# Remind the user they waited too long
print("Looking at the goodies you didn't stock up on, idiot...")

# Loop through json
def siteLoop():
    for targets in site_data["cal"]:
        urlSub = targets.get('url')
        itemName = targets.get('name')
        print(urlSub)
        print(itemName)
        webFunc(urlSub, itemName)
        

# Run main function
def webFunc(urlSub, itemName):
    # Read the next url and print
    url = driver.get(site_data["site"] + urlSub)
    print('Reading product information.......')
    print('On item: % s via % s ' %
          (itemName, url))

    # Ensure page loaded
    try:
        assert site_data["title"] in driver.title
        print("Correct page loaded")
    except AssertionError:
        print("Page error")

    # Wait to give modal time to display
    print("Waiting for that damn modal")
    time.sleep(8)

    # Check for modal, close if present.
    try:
        modal = driver.find_element_by_class_name(site_data["targetClass"])
        modal.click()
        print("Closed That damn modal")
    except:
        print("No signup modal...")

    # Sort by "in stock"
    print("Sorting by 'in stock'...")
    driver.find_element_by_id(site_data["targetID"]).click()
    time.sleep(3)
    # Handle displayed stock
    try:  # Search for list items on the product-list element
        items = driver.find_element_by_xpath(
            '//ul[@class="product-list"]/li').is_displayed()
        print("items: % s" % items)
        print('% s is IN stock!' % itemName)
        output_file.write(
            "% s is IN STOCK DUDE, you probably missed it though... \n" % itemName)
        scrapeFunc()
    # If no items are displayed, add the timestamp and item to the backlog.
    except NoSuchElementException:
        print("% s is OUT of stock! \n" % itemName)
        output_file.write('ALL % s is out of stock as of % s \n' %
                        (itemName, timeStamp))

def scrapeFunc():
    returnList = []
    # stockedItems = driver.find_elements_by_xpath(
    #     '//ul[@class="product-list"]/li/a/h2')
    # stockedItemsTile = driver.find_elements_by_xpath(
    #     '//ul[@class="product-list"]/u')
    # stockedItemList = driver.find_element_by_class_name("product-list")
    stockedItemsTile = driver.find_elements_by_xpath('//*[@id="Results"]/ul/li')
    print("stockedItems length: % s" % len(stockedItemsTile))

    # print("stockedItems: % s " % stockedItems)
    # print("stockedItemsTile: % s " % stockedItemsTile)
    
    # Scrape info of stocked
    for elem in stockedItemsTile:
        print("elem: % s" % elem)
        text =  elem.find_element_by_xpath('.//a/h2').text
        price = elem.find_element_by_xpath('.//a/div[@class="product-listing-price"]').text
        pricePer = elem.find_element_by_xpath('.//a/div[@class="product-listing-price"]/span').text
        print("Text: % s" % text)
        print("price: % s" % price)
        print("per: % s" % pricePer)
        returnList.append({'\n Name': text, "\n Price per round": pricePer, "\n Price": price})
        # print
    # resultTitle = stockedItems.get_attribute("innerHTML")
    # returnList.append(elem)
    # print("text % s" % text)
    print("returnList: % s" % returnList)

     # TODO: Add items to email
    # emailFunc(items)


def emailFunc(items): 
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

    print(items)

# # Go back to "out of stock"
# print("Showing 'out of stock'...")
# driver.find_element_by_id(site_data["targetID"]).click()
# time.sleep(3)

# Start handling the list items
items = driver.find_elements_by_xpath(
    '//*[@id="Results"]/ul/li')

# '//ul[@class="product-list"]/li/a/button')

# try:
#     assert items.is_displayed()
#     print("Found items list")
# except NoSuchElementException:
#     print("Error finding items list")

siteLoop()
print("All done")
output_file.write('Done searching on % s \n' % (datetime.now()))

# def subLoop(itemList):
#     print("")

# # for itemList in items:
# for i in (items):
#     print("items: % s" % items)
#     print("i: % s" % i)
#     # test = i.find_element_by_class_name("stockNotify")
#     # print(test)
#     time.sleep(10)
#     subLoop(i)


