#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

def parse(PATH, driver, website):
    
    # Acquire the URL and launch it in the chosen browser.
    
    driver.get(website)
    print(driver.title)

    # search = driver.find_element_by_class_name("infinite-scroll-component ")
    # print(driver.page_source)

    try:
        scroller = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "infinite-scroll-component "))
        )
        print(scroller.text)
    except:
        driver.quit()

    # scroller = driver.find_element_by_class_name("infinite-scroll-component ")
    # print(scroller.text)
    # time.sleep(5)

    driver.quit()

def main(argv):
    # Path to the driver. In this case, Chrome.
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    stock = input("Enter stock symbol: ")
    website = "https://www.stocktwits.com/symbol/" + stock

    parser = parse(PATH, driver, website)

if __name__ == "__main__":
    main(sys.argv)