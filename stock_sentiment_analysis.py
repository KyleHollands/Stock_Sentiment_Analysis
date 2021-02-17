#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# The main function of the script=================================================================================================

def parse(driver, website, bullish_pattern, bearish_pattern, positive_count, negative_count, positive_list, negative_list):
    
    # Acquire time to scroll to from the user. (11:00 AM). Only considers hour and AM/PM.

    date_time = 000000
    commentNum = 0
    date_time_pattern = ""
    
    print("\nWould you like to search until time or day? (ex. Yes/No")
    ans = input()
    print("----------------")

    if ans == "Yes":
        print("\nEnter the date (ex. 10/3/20) or time (ex. 03:00 PM  | minutes excluded from search.)")
        date_time = input()
    else:
        print("\nEnter the number of comments to search to.")
        commentNum = int(input())
    
    # Utilizing the driver parameters set before, get the website that was indicated prior.
    
    driver.get(website)

    print("\n" + driver.title) # Prints the title of the web page.

    if ans == "Yes":
        date_time = date_time.lower()

        if "am" in date_time or "pm" in date_time:
            date_time_pattern = r''+date_time[0:2]+':\d\d\s'+date_time[6:8]+''
        else:
            date_time_pattern = r''+date_time+''

    # Using a try, except block, ensure the content is loaded before continuing by waiting.
    # try:
    scroller = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "infinite-scroll-component "))
    )
    # print(scroller.text) 

    # Sets the bull and bear counters to 0.
    bull_count = 0
    bear_count = 0 
    count = 0
    
    # Controls the page scrolling parameters==================================================================================
    
    # Control the pause time before scrolling begins to allow page loading.
    SCROLL_PAUSE_TIME = 0.5

    # Acquire the page scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the preset pixel length of the page.
        driver.execute_script("window.scrollTo(0, 50000)") # Set to a high value.

        # Utilize the pause value above.
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    # The main loop to acquire header and comment information================================================================
    for stock_comment in scroller.find_elements_by_css_selector('.st_24ON8Bp.st_1x3QBA7.st_1SZeGna.st_3-tdfjd'):
        stock_comment_text = stock_comment.text.lower()
        stock_comment_text = (stock_comment_text.translate({ord(i): None for i in "'\''-?!"}))
        count += 1 # Count the number of comments scrolled through.

        # try:
        print(stock_comment_text) # For debugging.
        print("-----------------------------------------------------------------")
        print("-----------------------------------------------------------------")

        if ans == "Yes":
            if re.search(date_time_pattern, stock_comment_text):
                break
            elif count == 100: # If no matches exist, this will prevent the script from running indefinitely.
                break
            else:
                pass

        if ans != "Yes":
            if count == commentNum:
                break

        # Create a counter of how many times Bullish or Bearish appear and whether positive or negative comments are found.
        if re.search(bullish_pattern, stock_comment_text):
            bull_count += 1
        elif re.search(bearish_pattern, stock_comment_text):
            bear_count += 1
        else:
            if any(x in stock_comment_text for x in positive_list):
                # print("Found Positive")
                positive_count += 1
            elif any(x in stock_comment_text for x in negative_list):
                # print("Found Negative")
                negative_count += 1
            else:
                pass
        # except:
        #     pass
        
    # Print out bearish/bullish results as well as a calculated percentage reflecting overall sentiment========================

    # Print out the results while explicitly converting the variables to strings.
    # print("\nBulls: " + str(bull_count))
    # print("Bears: " + str(bear_count))
    
    # print("\nPositive comments: " + str(positive_count))
    # print("Negative comments: " + str(negative_count))
    
    positive_total = (positive_count + bull_count)
    negative_total = (negative_count + bear_count)

    print("\nBulls + positive comments: " + str(positive_total))
    print("Bears + negative comments: " + str(negative_total))
    
    # Determine positive outlook percentage.
    if positive_total > negative_total:
        percentage = 100 - ((negative_total / positive_total) * 100)
        print("\nStock Sentiment: " + "{:.2f}".format(percentage) + "%")
    elif negative_total > positive_total:
        percentage = ((positive_total / negative_total) * 100)
        print("\nStock Sentiment: " + "{:.2f}".format(percentage) + "%")
    elif negative_total == 0 and positive_total == 0:
        print("\nNo positive or negative data found.")
    elif negative_total == positive_total:
        percentage = ((positive_total / negative_total) * 50)
        print("\nStock Sentiment: " + "{:.2f}".format(percentage) + "%")
    else:
        pass

    print(count)

    # Wait for user input to prevent window from closing.
    input('\nPress ENTER to exit')

    # ==========================================================================================================================

    # finally:
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
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--ignore-urlfetcher-cert-requests')
    options.add_argument('--allow-insecure-localhost')
    options.add_argument('--ignore-certificate-errors-spki-list')

    # Sets the driver to the Chrome webdriver utilizing the options set above.
    driver = webdriver.Chrome(executable_path=PATH, options=options)

    # Asks the user to enter a ticker (stock) symbol.
    stock = input("\nEnter stock symbol (ex. PTON): ")
    website = "https://www.stocktwits.com/symbol/" + stock

    
    
    bullish_pattern = r'bullish'
    bearish_pattern = r'bearish'

    positive_count = 0
    negative_count = 0
    
    positive_list = ["buy", "up", "increase", "better", "great", "healthy", "consolidation", "undervalued", "the squeeze", "outperform", "outperforms", "thats a bullish close", "recover", "squeeze", "short it again"]
    negative_list = ["sell", "overvalued", "shrinking", "down", "underperform", "underperforms", "thats a bearish close", "cut my losses", "get out", "bye bye", "beware", "will fall", "pos"]

    # Calls the main function above and passes the variables set previously.
    parser = parse(driver, website, bullish_pattern, bearish_pattern, positive_count, negative_count, positive_list, negative_list)

if __name__ == "__main__":
    main(sys.argv)