import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

total_jobs = []

def extract_description(soup):
  descriptions = soup.select('.job-description')
  for i, description in enumerate(descriptions):
    joblist[i]['description'] = description.decode_contents()

for x in range(1, 2):
  joblist = []
  url = 'https://www.flexjobs.com/search?location=&search=data+science&page='
  r = requests.get(url + str(x))
  soup = BeautifulSoup(r.content,'html.parser')
  content = soup.find_all('div', class_ = 'col-md-12 col-12')
  #return r.status_code  #testing url,header

  #return len(divs) #testing divs 
  for item in content:
    title = item.find('a').text.strip()

    #jobage = item.find('div', class_ = 'job-age').text.strip() #ignoring it to match other csv

    salary = ''

    jobtype = item.find('span', class_ = 'job-tag d-inline-block mr-2 mb-1').text.strip()

    location = item.find('div', class_ = 'col pr-0 job-locations text-truncate').text.strip()
    #print(joblocation) #testing joblocation 

    job = {
        'title' : title,
        #'jobage' : jobage,
        'salary': salary,        
        'jobtype' : jobtype,
        'location' : location
    } 
    joblist.append(job)

  extract_description(soup)
  total_jobs.extend(joblist)
  print('jobs found in this iteration:', len(joblist))  

  time.sleep(2)
print(joblist)


df = pd.DataFrame(total_jobs)

print(df.head())

df.to_csv('../data/flexjobs.csv')
