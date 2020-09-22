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

def parse(PATH, driver, website, time_pattern, bullish_pattern, bearish_pattern, positive_list, negative_list):
    
    # Utilizing the driver parameters set before, get the website that was indicated prior.
    
    driver.get(website)

    print("\n" + driver.title) # Prints the title of the web page.

    # Using a try, except block, ensure the content is loaded before continuing by waiting.
    try:
        scroller = WebDriverWait(driver, 5).until(
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
            driver.execute_script("window.scrollTo(0, 100000)") # Set to a high value.

            # Utilize the pause value above.
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height.
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height

        # The main loop to acquire header and comment information================================================================
        for stock_comment in scroller.find_elements_by_css_selector('.st_24ON8Bp.st_1x3QBA7.st_1SZeGna.st_3MXcQ5h.st_3-tdfjd'):
            try:
                # print(stock_comment.text) # For debugging.

                # Once the time stamp reaches the time entered, break the loop.
                if re.search(time_pattern, stock_comment.text):
                    break
                else:
                    pass

                # Create a counter of how many times Bullish or Bearish appear.
                if re.search(bullish_pattern, stock_comment.text):
                    bull_count += 1
                elif re.search(bearish_pattern, stock_comment.text):
                    bear_count += 1
                else:
                    pass

                if any(x in stock_comment.text.lower() for x in positive_list):
                    print("Found")

                # result = [ele for ele in positive_list if (ele in stock_comment.text.lower())]
                # print(bool(result))

            except:
                pass
            
        # Print out bearish/bullish results as well as a calculated percentage reflecting overall sentiment========================

        # Print out the results while explicitly converting the variables to strings.
        print("Bulls: " + str(bull_count))
        print("Bears: " + str(bear_count))

        # Determine positive outlook percentage.
        if bear_count < bull_count:
            percentage = 100 - ((bear_count / bull_count) * 100)
            print("Stock Sentiment: " + "{:.2f}".format(percentage) + "%")
        else:
            percentage = 100 - ((bull_count / bear_count) * 100)
            print("Stock Sentiment: " + "{:.2f}".format(percentage) + "%")

        # Wait for user input to prevent window from closing.
        input('\nPress ENTER to exit')

        # ==========================================================================================================================

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

    # Sets the driver to the Chrome webdriver utilizing the options set above.
    driver = webdriver.Chrome(executable_path=PATH, options=options)

    # Asks the user to enter a ticker (stock) symbol.
    stock = input("\nEnter stock symbol (ex. PTON): ")
    website = "https://www.stocktwits.com/symbol/" + stock

    # Acquire time to scroll to from the user. (11:00 AM). Only considers hour and AM/PM.
    time = input("\nEnter the time to search until (ex. 03:00 PM): ")
    
    # Time search regex pattern.
    time_pattern = r''+time[0:2]+':\d\d\s'+time[6:8]+''
    bullish_pattern = r'Bullish'
    bearish_pattern = r'Bearish'

    positive_list = ["always", "free"]
    negative_list = ["sell"]

    # Calls the main functioon above and passes the variables set previously.
    parser = parse(PATH, driver, website, time_pattern, bullish_pattern, bearish_pattern, positive_list, negative_list)

if __name__ == "__main__":
    main(sys.argv)