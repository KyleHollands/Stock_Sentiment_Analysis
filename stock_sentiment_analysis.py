#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
import re

# The main function of the script=================================================================================================

def parse(PATH, driver, website, pattern):
    
    # Utilizing the driver parameters set before, get the website that was indicated prior.
    
    driver.get(website)
    print(driver.title) # Prints the title of the web page.

    # Using a try, except block, ensure the content is loaded before continuing by waiting.
    try:
        scroller = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "infinite-scroll-component "))
        )
        # print(scroller.text)

        # Sets the bull and bear counters to 0.
        bull_count = 0
        bear_count = 0 
        
        # Controls the page scrolling parameters==================================================================================
        
        # Control the pause time before scrolling begins to allow page loading.
        SCROLL_PAUSE_TIME = 0.5

        # Acquire the page scroll height.
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to the preset pixel length of the page.
            driver.execute_script("window.scrollTo(0, 50000)")

            # Utilize the pause value above.
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height.
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height

        # =======================================================================================================================

        for i in range(1, 200):
            try:
                # Acquires the content in each comment.
                # stock_comments = scroller.find_element_by_xpath("/html/body/div[2]/div/div/div[3]/div/div/div/div[2]/div/div/div[2]/div[3]/div/div[%i]/div/div/article" %(i))
                # print(stock_comments.text)
                
                # Acquires the content in each header.
                stock_outlook = scroller.find_element_by_xpath("/html/body/div[2]/div/div/div[3]/div/div/div/div[2]/div/div/div[2]/div[3]/div/div[%i]/div/div/article/div/div[2]/div[1]/span[2]/span/div/div" %(i))
                # print(stock_outlook.text)

                # Acquires the time in each header.
                stock_comment_time = scroller.find_element_by_xpath("/html/body/div[2]/div/div/div[3]/div/div/div/div[2]/div/div/div[2]/div[3]/div/div[%i]/div/div/article/div/div[2]/div[1]/a" %(i))
                print(stock_comment_time.text)

                if re.search(pattern, stock_comment_time.text):
                    break
                
                # Create a counter of how many times Bullish or Bearish appear.
                if stock_outlook.text == "Bullish":
                    bull_count += 1
                elif stock_outlook.text == "Bearish":
                    bear_count += 1
                else:
                    pass

            except:
                pass
        
        # Print out the results while explicitly converting the variables to strings.
        print("Bulls: " + str(bull_count))
        print("Bears: " + str(bear_count))
        percentage = (bear_count / bull_count) * 100
        print("Stock Sentiment: " + str(percentage) + "%")
            
    finally:
        driver.quit()

def main(argv):
    # Path to Chrome driver.
    PATH = "C:\Program Files (x86)\chromedriver.exe"

    # Acquire the hour (03 for 3:00pm), from the user.
    hour = input("Enter hour to scrape comments to (ex. 03 - 3:00pm): ")

    pattern = r'^('+hour+')' # Creates the regex pattern to be used from the prior input.

    # These options ensure that the browser launches in headless mode.
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    options.add_argument('--lang=en')

    # Sets the driver to the Chrome webdriver utilizing the options set above.
    driver = webdriver.Chrome(executable_path=PATH, options=options)

    # Asks the user to enter a ticker (stock) symbol.
    stock = input("Enter stock symbol: ")
    website = "https://www.stocktwits.com/symbol/" + stock

    # Calls the main functioon above and passes the variables set previously.
    parser = parse(PATH, driver, website, pattern)

if __name__ == "__main__":
    main(sys.argv)