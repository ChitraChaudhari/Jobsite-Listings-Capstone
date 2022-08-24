from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import pandas as pd


url = 'https://www.dice.com/jobs?q=data%20science&countryCode=US&radius=30&radiusUnit=mi&pageSize=10&language=en&page='

# download chromedriver for your OS from https://chromedriver.storage.googleapis.com/index.html?path=92.0.4515.43/ and set the path below
driver = webdriver.Chrome('/Users/rajpa/Desktop/chromedriver')
joblist = []
for page in range(1,2):
    driver.get(f'{url}{page}')
    try:
        WebDriverWait(driver, 5).until(lambda s: s.find_element_by_class_name("card").is_displayed())
    except TimeoutException:
        print("TimeoutException: Element not found")
        exit()

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
#df.to_csv('../data/dice.csv')
driver.close()
