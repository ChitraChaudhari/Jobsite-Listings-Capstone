from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import pandas as pd


url = 'https://www.dice.com/jobs?q=entry%20level%20data%20engineering&location=Canton,%20MI%2048187,%20USA&latitude=42.3373253&longitude=-83.4963567&countryCode=US&locationPrecision=PostalCode&radius=30&radiusUnit=mi&page=1&pageSize=10&language=en'
# original url 'https://www.dice.com/jobs?q=data%20science&countryCode=US&radius=30&radiusUnit=mi&pageSize=10&language=en&page='
# https://www.dice.com/jobs?q=entry%20level%20data%20engineering&location=Canton,%20MI%2048187,%20USA&latitude=42.3373253&longitude=-83.4963567&countryCode=US&locationPrecision=PostalCode&radius=30&radiusUnit=mi&page=1&pageSize=10&language=en

# download chromedriver for your OS from https://chromedriver.storage.googleapis.com/index.html?path=92.0.4515.43/ and set the path below
driver = webdriver.Chrome('/Users/rajpa/Desktop/chromedriver')
joblist = []
for page in range(1,3):
    driver.get(f'{url}{page}')
    try:
        WebDriverWait(driver, 5).until(lambda s: s.find_elements(By.CLASS_NAME,"card"))
    except TimeoutException:
        print("TimeoutException: Element not found")
        #exit()

    soup = BeautifulSoup(driver.page_source, "lxml")
    jobs = soup.select("div .search-card")
    for job in jobs:
        title = ''
        company = ''
        location = ''
        description = ''
        try:
            if(job.select('.card-title-link')[0]):
                title = job.select('.card-title-link')[0].text
            if(job.select('.card-company a')[0]):
                company = job.select('.card-company a')[0].text
            if(job.select('.card-company:last-child')[0]):
                location = job.select('.card-company:last-child')[0].text
            if(job.select('.card-description')[0]):
                description = job.select('.card-description')[0].text
        except:
            pass

        job = {
            'title' : title,
            'company' : company,
            'description' : description,
            'location' : location
        }
        joblist.append(job)

df = pd.DataFrame(joblist)
print(df.head(10))
#df.to_csv('../data/rj_dice.csv')
driver.close()
