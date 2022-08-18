import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

joblist = []
url = 'https://www.indeed.com/jobs?q=data+science&start='
for x in range(0,3002,10): #need to check pagination  --- check 1 #given 100 at random
  r = requests.get(url + str(x))

  soup = BeautifulSoup(r.content,'html.parser')
  jobs = soup.select("a .slider_container")
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
      if(job.select('.companyName')[0]):
        company = job.select('.companyName')[0].text
      if(job.select('.remote-bullet ~ span')):
        remote = job.select('.remote-bullet ~ span')[0].text
      if(job.select('.companyLocation')[0]):
        location = job.select('.companyLocation')[0].text
      if(job.select('.job-snippet li')):
        jobSnippets = job.select('.job-snippet li')
      for jobSnippet in jobSnippets:
        description += jobSnippet.text
      if(job.select('.salary-snippet')[0]):
        salary = job.select('.salary-snippet')[0].text
    except:
      pass

    job = {
        'title' : title,
        'company' : company,
        'salary' : salary,
        'jobtype' : jobtype,
        'description' : description,
        'location' : location
    }
    joblist.append(job)  

  print('jobs length :', len(joblist))  
  time.sleep(10)


df = pd.DataFrame(joblist)

df.to_csv('../data/indeed_jobs.csv')


