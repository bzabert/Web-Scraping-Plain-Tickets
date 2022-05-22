from cProfile import label
from locale import currency
from typing import Counter
from wsgiref.headers import Headers
import click
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time
import datetime
import pandas as pd


URL = "https://www.aerolineas.com.ar/"

# Options for Navigation
option = webdriver.ChromeOptions()
option.add_argument("--start-maximized")
option.add_argument("--disable-extensions")

driver_path = "/Users/bzabert/Documents/Portfolio/Python/Web scraping/chromedriver"
driver = webdriver.Chrome(driver_path, chrome_options=option)
driver.maximize_window()


# Open google Chrome
driver.get(URL)

# Definde Date and time of scraping and data Structure

scraping_date = datetime.datetime.now()
scraping_date = scraping_date.strftime("%d/%m/%Y %H:%M:%S")
scraping_time = scraping_date[-8:-3]
scraping_date = scraping_date[:10]
header = [
    "ScrapingDate",
    "ScrapingTime",
    "OrigenCity",
    "DestinationCity",
    "Currencie",
    "Price",
    "TypeTicket",
    "TicketDate",
]

dic_month = {
    "ENERO": "01",
    "FEBRERO": "02",
    "MARZO": "03",
    "ABRIL": "04",
    "MAYO": "05",
    "JUNIO": "06",
    "JULIO": "07",
    "AGOSTO": "08",
    "SEPTIEMBRE": "09",
    "OCTUBRE": "10",
    "NOVIEMBRE": "11",
    "DICIEMBRE": "12",
}
data = []

# Select Origin and Destination City
try:
    Origin_city = driver.find_element_by_xpath('//*[@id="suggestion-input-sb-origin"]')
    Origin_city.send_keys("Buenos Aires")
    time.sleep(2)
    Origin_city = driver.find_element_by_xpath(
        '//*[@id="react-autowhatever-1--item-0"]'
    ).click()

    Destination_city = driver.find_element_by_xpath(
        '//*[@id="suggestion-input-sb-destination"]'
    )
    Destination_city.send_keys("Miami")
    time.sleep(2)
    Destination_city = driver.find_element_by_xpath(
        '//*[@id="react-autowhatever-1--item-0"]'
    ).click()
except:
    pass

# Scraping from June to December
scrape_month = [
    ("Sun May 22 2022", "Mon May 30 2022"),
    ("Thu Jun 02 2022", "Wed Jun 29 2022"),
    ("Sat Jul 02 2022", "Sat Jul 30 2022"),
    ("Tue Aug 02 2022", "Tue Aug 30 2022"),
    ("Fri Sep 02 2022", "Thu Sep 29 2022"),
    ("Sun Oct 02 2022", "Sun Oct 30 2022"),
    ("Wed Nov 02 2022", "Tue Nov 29 2022"),
    ("Fri Dec 02 2022", "Fri Dec 30 2022"),
]
count = 0
for fisrt_day, end_day in scrape_month:
    if count == 0:
        driver.find_element_by_xpath('//*[@id="button-search-flights"]').click()
        time.sleep(10)
    else:
        driver.find_element_by_xpath('//*[@id="button-edit-search"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="input-from-date"]').click()
    days = driver.find_elements_by_xpath('//*[@class="DayPicker-Day"]')
    for day in days:
        if fisrt_day in day.get_attribute("aria-label"):
            day.click()
            time.sleep(4)
            break

    days = driver.find_elements_by_xpath('//*[@class="DayPicker-Day"]')
    time.sleep(2)
    for day in days:
        if end_day in day.get_attribute("aria-label"):
            day.click()
            time.sleep(4)
            break
    driver.find_element_by_xpath('//*[@id="button-search-flights"]').click()
    time.sleep(6)
    # Scraping One-way Day
    one_way_days = driver.find_element_by_xpath('//*[@id="fdc-from-box"]')
    available_days_one_way = one_way_days.find_elements_by_xpath(
        './/*[@id="fdc-available-day"]'
    )
    for day in available_days_one_way:
        date = day.find_element_by_xpath('.//*[@id="fdc-button-day"]').text
        month = dic_month[
            one_way_days.find_element_by_xpath('.//*[@id="fdc-month"]').text
        ]
        date = date + "/" + month + "/" + "2022"
        ticekt_type = one_way_days.find_element_by_xpath('.//*[@id="header-type"]').text
        price = day.find_element_by_xpath('.//*[@id="fdc-button-price"]').text
        currency = day.find_element_by_xpath('.//*[@id="fdc-button-currency"]').text
        data.append(
            [
                scraping_date,
                scraping_time,
                "Buenos Aires, Argentina (BUE)",
                "Miami, USA (MIA)",
                currency,
                price,
                ticekt_type,
                date,
            ]
        )
    # Scraping return Day
    return_days = driver.find_element_by_xpath('//*[@id="fdc-to-box"]')
    available_days_return = return_days.find_elements_by_xpath(
        './/*[@id="fdc-available-day"]'
    )
    for day in available_days_return:
        date = day.find_element_by_xpath('.//*[@id="fdc-button-day"]').text
        month = dic_month[
            return_days.find_element_by_xpath('.//*[@id="fdc-month"]').text
        ]
        date = date + "/" + month + "/" + "2022"
        ticekt_type = return_days.find_element_by_xpath('.//*[@id="header-type"]').text
        price = day.find_element_by_xpath('.//*[@id="fdc-button-price"]').text
        currency = day.find_element_by_xpath('.//*[@id="fdc-button-currency"]').text
        data.append(
            [
                scraping_date,
                scraping_time,
                "Miami, USA (MIA)",
                "Buenos Aires, Argentina (BUE)",
                currency,
                price,
                ticekt_type,
                date,
            ]
        )
    count += 1
driver.close()

with open(
    "/Users/bzabert/Documents/Portfolio/Python/Web scraping/Aerolineas Argentinas/PlainDataset.csv",
    "w",
    newline="",
    encoding="UTF8",
) as Dataset:
    writer = csv.writer(Dataset)
    writer.writerow(header)
    for row in data:
        writer.writerow(row)

print(pd.DataFrame(data))
