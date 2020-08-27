
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
# import WebDriverWait

# Read from json file
with open("signup.json", "r") as f:
    site_data = json.load(f)

# Initialize log file
output_file = open('signup.txt', 'a')

# Establish web driver
driver = webdriver.Chrome()


targetUrl = (site_data["site"])
print(targetUrl)

driver.get(targetUrl)
timeStamp = datetime.now()

try:
    assert site_data["title"] in driver.title
    print("Correct page loaded")
except AssertionError:
    print("Page error")

# Wait to give modal time to display
print("Waiting for that damn modal")
time.sleep(8)

# Handle popup and target "in stock" only
# Check for modal, close if present.
try:
    modal = driver.find_element_by_class_name(site_data["targetClass"])
    print(modal)
    modal.click()
    print("Closed That damn modal")
except:
    print("No signup modal...")


# # Sort by "in stock"
# print("Sorting by 'in stock'...")
# driver.find_element_by_id(site_data["targetID"]).click()
# time.sleep(3)
# # Handle displayed stock
# try:  # Search for list items on the product-list element
#     items = driver.find_element_by_xpath(
#         '//ul[@class="product-list"]/li').is_displayed()
#     print('Shit is IN stock!')
#     output_file.write(
#         "Shit is IN STOCK DUDE, you probably missed it though... \n")

# # If no items are displayed, add the timestamp and item to the backlog.
# except NoSuchElementException:
#     print("Everything is OUT of stock! \n")
#     output_file.write('Everything is out of stock as of % s \n' %
#                       (timeStamp))

# # Go back to "out of stock"
# print("Showing 'out of stock'...")
# driver.find_element_by_id(site_data["targetID"]).click()
# time.sleep(3)
# print("Looking at the goodies you didn't stock up on, idiot.")

# Start handling the list items
items = driver.find_elements_by_xpath(
    '//*[@id="Results"]/ul/li')

# '//ul[@class="product-list"]/li/a/button')


# try:
#     assert items.is_displayed()
#     print("Found items list")
# except NoSuchElementException:
#     print("Error finding items list")


def subLoop(itemList):
    time.sleep(5)
    driver.switch_to.default_content()

    itemList.click()

    time.sleep(9)

    # new WebDriverWait(driver, TimeSpan.FromSeconds(10)).Until(ExpectedConditions.ElementToBeClickable(By.CssSelector(site_data["entryEmail"]))).SendKeys(site_data["email"])
    driver.switch_to.frame("sb-player")
    # driver.find_element_by_id(site_data["entryEmail"])
    entry = driver.find_element_by_id(site_data["entryEmail"])
    # entry = item.find_element_by_xpath('//*[@id="stockpopupemail"]')
    print("Typing in email...")
    entry.send_keys(site_data["email"])
    notify = driver.find_element_by_id(site_data["notifyButton"])
    time.sleep(2)
    notify.click()
    time.sleep(3)
    driver.switch_to.default_content()
    print("Heading back to main page...")
    # driver.back()
    driver.execute_script("window.history.go(-2)")


# for itemList in items:
for i in (items):
    print("items: % s" % items)
    print("i: % s" % i)
    # test = i.find_element_by_class_name("stockNotify")
    # print(test)
    time.sleep(10)
    subLoop(i)


print("all done")
