from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
from datetime import datetime

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

URL = "https://www.transavia.com/nl-BE/home/"

abs_path = os.path.dirname(__file__)
PATH = os.path.join(abs_path, "../dependencies/chromedriver")

FROM = "BRU"

DESTINATIONS = {
    "spain": "ALC,IBZ,AGP,PMI,TFS".split(","),
    "portugal": ["FAO"],
    "italy": "BDS,NAP,PMO".split(","),
    "greece": "HER,RHO,CFU".split(",")
}

TEMP_DATE = "30-05-2023"

# FROM: Brussels
# TO: x
# date: today + (4 hours, 1 day, 7 days, 14 days, 1 month, 2 months, 4 months, 6 months)
# people: 1 adult
# deselect return flight

def set_departure(driver: webdriver.Chrome, departure = "BRU"):
    hidden_departure_input = driver.find_element(By.NAME, "routeSelection.DepartureStation")
    hidden_departure_input.send_keys(departure)

def set_destination(driver: webdriver.Chrome, destination):
    hidden_destination_input = driver.find_element(By.NAME, "routeSelection.ArrivalStation")
    hidden_destination_input.send_keys(destination)
    
def set_one_way(driver: webdriver.Chrome):
    is_return_flight_input = driver.find_element(By.ID, "dateSelection.isReturnFlight")
    if is_return_flight_input.is_selected(): is_return_flight_input.click()

def set_date(driver: webdriver.Chrome, date):
    date_input = driver.find_element(By.ID, "dateSelection_OutboundDate-datepicker")
    date_input.send_keys(date)

def submit_form(driver: webdriver.Chrome):
    form = driver.find_element(By.ID, "desktop")
    form.submit()

def scrape_price(driver: webdriver.Chrome, to, date = TEMP_DATE):
    set_departure(driver)
    set_destination(driver, to)
    set_one_way(driver)
    set_date(driver, date)
    submit_form(driver)



def main():
    # for city in itertools.chain(*DESTINATIONS.values()):
    #     scrape_price
    driver.get(URL)
    scrape_price(driver, 'IBZ')

if __name__ == "__main__":
    main()