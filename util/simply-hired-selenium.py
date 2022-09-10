# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 11:51:05 2022

@author: chitra
"""

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from IPython.display import display, HTML
from selenium.webdriver.common.by import By

import time

# get the chromedriver
driver = webdriver.Chrome('/Users/chitr/Desktop/chromedriver')
driver.maximize_window()
print(" Chrome Open")

#open given url via chromediver
url = 'https://www.simplyhired.com/search?q=data+engineer&pn='
driver.get(url)
print("url open")

#scrape the data from website
joblist = []

pages = 100

for page in range(1, pages+1):
    driver.get(f'{url}{page}')
    time.sleep(2)
    
    for i in range(1,19):
        post=''
        cmpny=''
        loc=''
        sal=''
        jobtype=''
        qualifications=''
        benefits=''
        description=''
        try:
            ele = driver.find_elements(By.CSS_SELECTOR, f'#job-list > li:nth-child({i}) > article > div > div.jobposting-title-container > h3')
            if ele:
                post = ele[0].text 
            #print(post)
            driver.implicitly_wait(2)
            
            ele = driver.find_elements(By.CSS_SELECTOR, f'#job-list > li:nth-child({i}) > article > div > div.jobposting-subtitle > span.JobPosting-labelWithIcon.jobposting-company')
            if ele:
                cmpny = ele[0].text 
            #print(cmpny)
            driver.implicitly_wait(2)                         
            
            ele = driver.find_elements(By.CSS_SELECTOR,f'#job-list > li:nth-child({i}) > article > div > div.jobposting-subtitle > span.JobPosting-labelWithIcon.jobposting-location')
            if ele:
                loc = ele[0].text
            #print(loc)
            driver.implicitly_wait(2)
            
            ele = driver.find_elements(By.CSS_SELECTOR, f'#job-list > li:nth-child({i}) > article > div > div.SerpJob-metaInfo > div.SerpJob-metaInfoLeft')
            if ele:
                sal = ele[0].text
            #print(sal)
            driver.implicitly_wait(2)
            
            ele = driver.find_element(By.CSS_SELECTOR, f'#job-list > li:nth-child({i}) > article > div > div.SerpJob-snippetContainer > p')
            if ele:
                description = ele.text
            #print("description: ", description)
            driver.implicitly_wait(10)
                
            element = driver.find_element(By.CSS_SELECTOR,f'#job-list > li:nth-child({i}) > article > div > div.jobposting-title-container > h3 > a')
            webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
            time.sleep(4)
            driver.implicitly_wait(10)
            
            try:
                
                ele = driver.find_element(By.CSS_SELECTOR,'#content > div.wrap > div > div > div.TwoPane-paneHolder.TwoPane-paneHolder--right.hidden-sm-down > div > div > aside > div > div:nth-child(2) > div.viewjob-jobDetails > span > span')
                if element:
                    jobtype = ele.text
                #print("jobtype: ", jobtype)
                driver.implicitly_wait(10)
                                
                ele = driver.find_element(By.CSS_SELECTOR, '#content > div.wrap > div > div > div.TwoPane-paneHolder.TwoPane-paneHolder--right.hidden-sm-down > div > div > aside > div > div.viewjob-section.viewjob-qualifications.viewjob-entities > ul')
                if ele:
                    qualifications = ele.text
                #print("qualifications: ", qualifications)
                driver.implicitly_wait(10)
                
                ele = driver.find_element(By.CSS_SELECTOR, '#content > div.wrap > div > div > div.TwoPane-paneHolder.TwoPane-paneHolder--right.hidden-sm-down > div > div > aside > div > div.viewjob-section.viewjob-benefits.viewjob-entities > ul')
                if ele:
                    benefits = ele.text
                #print("benefits: ", benefits)
                driver.implicitly_wait(10)
                
            except:
                pass    
            
            job = {'title' : post,
                   'company' : cmpny,
                   'salary' : sal,
                   'location' : loc,
                   'jobtype' : jobtype,
                   'qualifications' : qualifications,
                   'benefits' : benefits,
                   'description' : description,
                    }
            joblist.append(job)
            
        except NoSuchElementException as e:
            continue
            
        except TimeoutException as e:
            continue
            
print("Data scraping Done")

#save the data to file
df = pd.DataFrame(joblist)
df.head(30)

df.to_csv('simplyhired-DataEngineer-2022.csv')