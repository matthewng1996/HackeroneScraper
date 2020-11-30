import sys
import requests
import time
import threading
import termplotlib as tpl
from collections import defaultdict
from collections import OrderedDict
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

## ---------------- Funtions ---------------- ##
def loading():
    loading_thread = threading.currentThread()
    while getattr(loading_thread, "loading_loop", True):
        print ("Loading   ",end='\r')
        time.sleep(1) #do some work here...
        print ("Loading.  ",end='\r')
        time.sleep(1) #do some more work here...
        print ("Loading.. ",end='\r')
        time.sleep(1) #do even more work...
        print ("Loading...",end='\r')
        time.sleep(1)
    print ("[ * ] Hactivity page scrolling complete.")

def scroll_down():
    """Scrolling the page for pages with infinite scrolling"""
    loading_thread = threading.Thread(target=loading)
    loading_thread.start()
    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page.
        time.sleep(5)
        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    loading_thread.loading_loop = False
    loading_thread.join()


## ---------------- Main code ---------------- ##\
n = len(sys.argv)
search_param = ""

if (n == 1):
    print("[ * ] Need an argument for hacktivity search!")
else:
    for i in range(1, n):
        search_param += sys.argv[i] + "%20"

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--enable-javascript")
    webdriver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    url = "https://hackerone.com/hacktivity?querystring=" + search_param

    with webdriver as driver:
            # Set timeout time 
            wait = WebDriverWait(driver, 1)

            # retrive url in headless browser
            driver.get(url)
            print("[ * ] Scrolling the page due to infinite scrolling")
            scroll_down()
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            driver.close()

            ## Find the total number of reports
            results = soup.find(class_='vertical-spacing vertical-spacing--large vertical-spacing--top')
            job_elems = results.find_all('div',class_='grid__column grid__column--four-fifths')
            
            num_results_text = "" #Tracks the total number of reports for the specific Hacktivity query 
            
            for job in job_elems:
                lookingfor = job.find('h3', class_='daisy-h3 no-margin')
                num_results_text = lookingfor.text 

            #Number of results - int
            num_reports = int("".join(filter(str.isdigit, num_results_text))) #Extracts only the digit and nothing else
     
            ## Initialise dictionary that stores all reports links for each bug bounty program
            report_directory_dictionary = defaultdict(list)

            fades = soup.find_all(class_='fade fade--show')
            for fade in fades:
                report_title_cards = fade.find(class_='sc-gsTCUz fZiDzA spec-hacktivity-content')
                # Retrieving report links and directory and adding them into a dictionary

                ## ---------------- Retrieving directory ---------------- ##
                report_directory_str = fade.find(class_='daisy-link routerlink daisy-link daisy-link--major').text

                ## ---------------- Retrieving links ---------------- ##    
                if (report_title_cards.find('a', {'class': 'daisy-link ahref daisy-link hacktivity-item__publicly-disclosed spec-hacktivity-item-title'}) != None):
                    report_link = report_title_cards.find('a', {'class': 'daisy-link ahref daisy-link hacktivity-item__publicly-disclosed spec-hacktivity-item-title'}).attrs['href']
                elif (report_title_cards.find('a', {'class': 'daisy-link ahref daisy-link hacktivity-item__hacker-published spec-hacktivity-item-title'}) != None):
                    report_link = report_title_cards.find('a', {'class': 'daisy-link ahref daisy-link hacktivity-item__hacker-published spec-hacktivity-item-title'}).attrs['href']
                ## ---------------- Add info to dictionary ---------------- ##
                ## Dictionary Key ==> Bug Bounty Program (BBP)
                ## Dictionary Value ==> Report Links for each (BBP)
                report_directory_dictionary[report_directory_str].append(report_link)
           
            bar_graph_label = [] #All the keys resides here
            num_reports_list = [] #Number of values for each key resides here

            for k in report_directory_dictionary:
                num_reports_list.append(len(report_directory_dictionary[k]))
                bar_graph_label.append(k)

            print("There are a total of " + str(len(report_directory_dictionary)) + " different directories.")
            print("There are a total of " + str(num_reports) + " different reports.")

            ## ---------------- Plot Graph ---------------- ##
            fig = tpl.figure()
            fig.barh(
                num_reports_list, # Amount per label
                bar_graph_label, # Label
                force_ascii = True
                )
            fig.show()