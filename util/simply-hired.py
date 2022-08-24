import requests
import bs4
from bs4 import BeautifulSoup

import pandas as pd
import time
joblist = []

for x in range(1,300):
  url = 'https://www.simplyhired.com/search?q=data+engineer&l=&job=4YxTnrhZo9AmsJWm4ZxptL9gCLGKuzOhlEuINh_WljZGypfj43oSNA'
  r = requests.get(url + str(x))
  soup = BeautifulSoup(r.content,'html.parser')
  content = soup.find_all('div', class_ = 'SerpJob-jobCard card')
  #return r.status_code  #testing url,header

  #return len(divs) #testing divs 
  for item in content:
    title = item.find('a').text.strip()
    company = item.find('span', class_ = 'JobPosting-labelWithIcon jobposting-company').text.strip()

    description = getattr(item.find('div', class_ = 'SerpJob-snippetContainer'), 'text', None) #unable to get description text, need to check----1
    #print(description) #testing jobdescription

    location = item.find('span', class_ = 'jobposting-location').text.strip()
    #print(joblocation) #testing joblocation 
    #jobage = item.find('div', class_ = 'job-age').text.strip() #ignoring it to match other csv
    try:
      salary = item.find('div', class_ = 'jobposting-salary SerpJob-salary').text.strip()
    except:
      salary = ''
    job = {
        'title' : title,
        #'jobage' : jobage,
        'salary': salary,        
        'company' : company,
        'description' : description,
        'location' : location
    } 
    joblist.append(job)
    

  print('jobs Found :', len(joblist))  
  time.sleep(2)
#print(joblist)


df = pd.DataFrame(joblist)

print(df.head())
df.to_csv('../data/simplyhired-DE-2022.csv')

