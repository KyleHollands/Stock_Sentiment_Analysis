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

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        scroller = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "infinite-scroll-component "))
        )
        # print(scroller.text)

        bull_count = 0
        bear_count = 0     

        for i in range(1, 30):
            try:
                # stock_comments = scroller.find_element_by_xpath("/html/body/div[2]/div/div/div[3]/div/div/div/div[2]/div/div/div[2]/div[3]/div/div[%i]/div/div/article" %(i))
                stock_outlook = scroller.find_element_by_xpath("/html/body/div[2]/div/div/div[3]/div/div/div/div[2]/div/div/div[2]/div[3]/div/div[%i]/div/div/article/div/div[2]/div[1]/span[2]/span/div/div" %(i))
                # print(stock_comments.text)
        
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

        # for article in articles:
        #     # header = article.find_element_by_class_name("st_11GoBZI")
        #     header = article.find_element_by_class_name("st_11GoBZI")

            # print(header.text)
            
    finally:
        driver.quit()

    # scroller = driver.find_element_by_class_name("infinite-scroll-component ")
    # print(scroller.text)
    # time.sleep(5)

    # driver.quit()

def main(argv):
    # Path to the driver. In this case, Chrome.
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    stock = input("Enter stock symbol: ")
    website = "https://www.stocktwits.com/symbol/" + stock

    parser = parse(PATH, driver, website)

if __name__ == "__main__":
    main(sys.argv)