#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys

def parse(PATH, driver, website):
    
    # Acquire the URL and launch it in the chosen browser.
    
    driver.get(website)
    print(driver.title)

    try:
        scroller = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "infinite-scroll-component "))
        )
        # print(scroller.text)

        bull_count = 0
        bear_count = 0 

        # Controls the page scrolling parameters==================================================================================
        
        # Control the pause time before scrolling begins to allow page loading.
        SCROLL_PAUSE_TIME = 0.5

        # Acquire the page scroll height.
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to the preset pixel length of the page.
            driver.execute_script("window.scrollTo(0, 40000)")

            # Utilize the pause value above.
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height.
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height

        # ======================================================================================================================

        for i in range(1, 50):
            try:
                stock_comments = scroller.find_element_by_xpath("/html/body/div[2]/div/div/div[3]/div/div/div/div[2]/div/div/div[2]/div[3]/div/div[%i]/div/div/article" %(i))
                print(stock_comments.text)
                
                # Extract Bearish or Bullish from the header.
                stock_outlook = scroller.find_element_by_xpath("/html/body/div[2]/div/div/div[3]/div/div/div/div[2]/div/div/div[2]/div[3]/div/div[%i]/div/div/article/div/div[2]/div[1]/span[2]/span/div/div" %(i))
                # print(stock_outlook.text)
        
                if stock_outlook.text == "Bullish":
                    bull_count += 1
                elif stock_outlook.text == "Bearish":
                    bear_count += 1
                else:
                    pass

                # print(stock_outlook.text)
            except:
                pass
        
        print("Bulls: " + str(bull_count))
        print("Bears: " + str(bear_count))
            
    finally:
        driver.quit()

def main(argv):
    # Path to Chrome driver.
    PATH = "C:\Program Files (x86)\chromedriver.exe"

    # These options ensure that the browser launches in headless mode.
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    options.add_argument('--lang=en')

    driver = webdriver.Chrome(executable_path=PATH, options=options)

    stock = input("Enter stock symbol: ")
    website = "https://www.stocktwits.com/symbol/" + stock

    parser = parse(PATH, driver, website)

if __name__ == "__main__":
    main(sys.argv)