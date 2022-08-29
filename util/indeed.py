from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import pandas as pd
import time

joblist = []
#url = 'https://www.indeed.com/jobs?q=data+science&start='
url = 'https://www.indeed.com/jobs?q=data+engineer&start='

driver = webdriver.Chrome('/Users/chitr/Desktop/chromedriver')

for x in range(1,3002,10): #need to check pagination  --- check 1 #given 100 at random
   driver.get(f'{url}{x}')
   try:
       WebDriverWait(driver, 5).until(lambda s: s.find_elements(By.CLASS_NAME,"slider_container"))
   except TimeoutException:
       print("TimeoutException: Element not found")
       
   soup = BeautifulSoup(driver.page_source,'lxml')
   jobs = soup.select("div.job_seen_beacon")
  
   for job in jobs:
    title = ''
    company = ''
    jobtype = ''
    location = ''
    description = ''
    salary = ''
    try:
      if(job.select('.jobTitle span[title]')[0]):
        title = job.select('.jobTitle span[title]')[0].text
      if(job.select('span.companyName')[0]):
        company = job.select('span.companyName')[0].text
      #commented jobtype to match other sites data  
      #if(job.select('.remote-bullet ~ span')):
        #jobtype = job.select('.remote-bullet ~ span')[0].text
      if(job.select('.companyLocation')[0]):
        location = job.select('.companyLocation')[0].text
      if(job.select('.job-snippet li')):
        jobSnippets = job.select('.job-snippet li')
      for jobSnippet in jobSnippets:
        description += jobSnippet.text
      if(job.select(' .salary-snippet-container')[0]):
        salary = job.select(' .salary-snippet-container')[0].text
    except:
      pass

    job = {
        'title' : title,
        'company' : company,
        'salary' : salary,
        #'jobtype' : jobtype,
        'description' : description,
        'location' : location
    }
    joblist.append(job)  

   print('jobs length :', len(joblist))  
   time.sleep(10)


df = pd.DataFrame(joblist)
print(df.head(10))


df.to_csv('../data/Indeed_DataEngineer_2022.csv')


