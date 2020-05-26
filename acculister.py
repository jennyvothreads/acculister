from config import keys
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException

import os, psutil, time, pyperclip, getpass


for process in (process for process in psutil.process_iter() if process.name()=="chrome.exe"):
    process.kill()
time.sleep(5)
##
driver_path = r'C:/Windows/chromedriver.exe'
##
chrome_options = ChromeOptions()
chrome_options.add_argument("--window-size=1080,608")
chrome_options.add_argument("--user-data-dir=C:\\Users\\" + getpass.getuser() + "\\AppData\\Local\\Google\\Chrome\\User Data")
chrome_options.add_argument("start-maximized")

def order(driver, keys):
    driver.get(keys['product_url']) ## go to the product url
    driver.switch_to.frame('findprod_iframe') ## switch to the frame where input is
    driver.find_element_by_xpath('//*[@id="w0-find-product-search-bar-search-field"]').send_keys(keys['product_title']) ## find the input field and enter product title
    driver.find_element_by_xpath('//*[@id="w0-find-product-search-bar-search-button"]').click() ## click on the search button
    ##driver.switch_to.default_content()

    try:
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="w0-find-product-2"]/div[2]/button'))).click() ## click on the "Couldn't find Item in Listings"
    except(NoAlertPresentException, TimeoutException) as py_ex:
        print("Timed out while waiting for Continue button to show")
        print(py_ex)
        print(py_ex.args)

    time.sleep(5)

    try:
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//select[@name="itemCondition"]'))).send_keys(keys['item_condition']) ## select item condition.
        ## New (N), Open Box (O), Manufacturer Refurbished (M), Seller Refurbished (S), Used (U), For parts, or not working, (
        driver.find_element_by_xpath('//*[@id="itemCondition"]').send_keys(Keys.TAB)
    except(NoAlertPresentException, TimeoutException) as py_ex:
        print("Page didn't load on time!")
        print(py_ex)
        print(py_ex.args)

    item_brand = driver.find_element_by_xpath('//*[@id="Listing.Item.ItemSpecific[Brand]"]') ## find the 'Brand' input field
    pyperclip.copy(keys['brand']) ## copy the contents of the brand key
    item_brand.send_keys(Keys.CONTROL, 'a') ## select everything there
    item_brand.send_keys(Keys.CONTROL, 'v') ## and paste in the text in brand

    try:
        item_color = keys['color']
        WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, '//*[@name="_st_Color" and @value=' + item_color + ']'))).click()
        time.sleep(3)
        WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, '//*[@name="_st_Color"]'))).send.keys(item_color)
    except(NoAlertPresentException, TimeoutException) as py_ex:
        print("Checkbox for " + item_color + " color not present after 5 seconds... \n Option select for " + item_color + " proceeding")
        print(py_ex)
        print(py_ex.args)

    driver.find_element_by_xpath('//*[@id="binPrice"]').send_keys(keys['binPrice']) ## send keys to starting price input field
    driver.find_element_by_xpath('//*[@id="pkgLength"]').send_keys(keys['pkgLength']) ## send dimensions for Length
    driver.find_element_by_xpath('//*[@id="pkgWidth"]').send_keys(keys['pkgWidth']) ## send dimensions for Width
    driver.find_element_by_xpath('//*[@id="pkgHeight"]').send_keys(keys['pkgHeight']) ## send dimensions for Height

    mjuw = driver.find_element_by_xpath('//*[@id="majorUnitWeight"]')
    pyperclip.copy(keys['majorUnitWeight'])
    mjuw.send_keys(Keys.CONTROL, 'a')
    mjuw.send_keys(Keys.CONTROL, 'v') ## send value for major unit of weight

    mnuw = driver.find_element_by_xpath('//*[@id="minorUnitWeight"]')
    pyperclip.copy(keys['minorUnitWeight'])
    mnuw.send_keys(Keys.CONTROL, 'a')
    mnuw.send_keys(Keys.CONTROL, 'v') ## send value for minor unit of weight

    description_area = driver.find_element_by_xpath('//iframe[contains(@id, "txtEdit_st")]')
    driver.switch_to.frame(description_area) ## switch to the frame for description
    pyperclip.copy(keys['description'])
    description_textarea = driver.find_element_by_xpath('/html/body')
    description_textarea.send_keys(Keys.CONTROL, 'v')
    time.sleep(2)
    ## driver.find_element_by_xpath('/html/body').send_keys(keys['description']) ## and enter the description

    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="format"]').send_keys(keys['format']) ## select item condition.
    driver.find_element_by_xpath('//*[@id="format"]').send_keys(Keys.TAB)


if __name__ == '__main__':
    driver = Chrome(executable_path=driver_path, options=chrome_options)
    order(driver, keys)

