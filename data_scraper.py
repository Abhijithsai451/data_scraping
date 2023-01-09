import datetime

import requests
import os
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://severeweather.wmo.int/v2/list.html")

try:
    elem = WebDriverWait(driver,30).until(
        EC.presence_of_element_located((By.CLASS_NAME,"dataTables_scrollBody")))
finally:
    print('loaded')

soup = BeautifulSoup(driver.page_source,'html.parser')
# Exracting the data from the html page
all = soup.findAll('tbody')[2]
rows = all.findAll('tr')

# Saving the data into a CSV file
data = []
for i in rows:
    infos_row = i.findAll('td')
    for index,j in enumerate(infos_row):
        info = None
        if index == 0:
            info = j.find('span')
            event = info.text
        if index == 4:
            info = j.find('span')
            areas = info.text
        if index == 1:
            issued_time = j.text
        if index == 3:
            country = j.text
        if index == 5:
            regions = j.text
        if index == 2:
            continue
    data.append([event,issued_time,country,areas,regions])

# Saving the data as a Pandas data frame and then to convert it as a CSV
df = pd.DataFrame(data, columns=['Event_type','Issued_time','Country','Areas','Regions'])
df.to_csv("scrapped_weather.csv",mode='a',index = False, header = False)

