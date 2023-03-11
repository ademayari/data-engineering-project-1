import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import sys
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as wait
from gmail import login_gmail
from captcha import captcha_present
import itertools

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

DIMENSIONS = [
    (1920, 1080),
    (1366, 768),
    (1536, 864)
]

TEMP_DATE = "30-05-2023"

# FROM: Brussels
# TO: x
# date: today + (4 hours, 1 day, 7 days, 14 days, 1 month, 2 months, 4 months, 6 months)
# people: 1 adult
# deselect return flight

def set_departure(driver: webdriver.Chrome, departure = "BRU"):
    # hidden_departure_input = driver.find_element(By.NAME, "routeSelection.DepartureStation")
    hidden_departure_input = driver.find_element(By.XPATH, '//*[@name="routeSelection.DepartureStation"]')
    hidden_departure_input.send_keys(departure)

def set_destination(driver: webdriver.Chrome, destination):
    # hidden_destination_input = driver.find_element(By.NAME, "routeSelection.ArrivalStation")
    hidden_destination_input = driver.find_element(By.XPATH, '//*[@name="routeSelection.ArrivalStation"]')
    hidden_destination_input.send_keys(destination)
    
def set_one_way(driver: webdriver.Chrome):
    # is_return_flight_input = driver.find_element(By.ID, "dateSelection.isReturnFlight")
    is_return_flight_input = driver.find_element(By.XPATH, '//*[@id="dateSelection.isReturnFlight"]')
    if is_return_flight_input.is_selected(): is_return_flight_input.click()

def set_date(driver: webdriver.Chrome, date):
    # date_input = driver.find_element(By.ID, "dateSelection_OutboundDate-datepicker")
    date_input = driver.find_element(By.XPATH, '//*[@id="dateSelection_OutboundDate-datepicker"]')
    date_input.send_keys(date)

def submit_form(driver: webdriver.Chrome):
    # form = driver.find_element(By.ID, "desktop")
    form = driver.find_element(By.XPATH, '//*[@id="desktop"]')
    form.submit()

def init_transavia_search(driver: webdriver.Chrome):
    driver.get(URL)
    time.sleep(3)

    

def scrape_price(driver: webdriver.Chrome, to, date = TEMP_DATE):
    time.sleep(10000)
    set_departure(driver)
    set_destination(driver, to)
    set_one_way(driver)
    set_date(driver, date)
    submit_form(driver)



def main():
    # for city in itertools.chain(*DESTINATIONS.values()):
    #     scrape_price

    driver.get(URL)
    time.sleep(10)

    main_iframe = driver.find_element(By.ID, "main-iframe")
    driver.switch_to.frame(main_iframe)

    # navigate to the nested iframe
    nested_iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(nested_iframe)

    # wait for the checkbox element to appear
    checkbox_element = wait(driver, 10).until(EC.presence_of_element_located((By.ID, "recaptcha-anchor")))

    # click the checkbox element
    checkbox_element.click()

    time.sleep(3000)

    # swith to iframe
    # driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="main-iframe"]'))
    
    # driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="reCAPTCHA"]'))
   
    # element = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))
    # element.click()




    #driver.find_element(By.ID, "recaptcha-anchor").click()

    scrape_price(driver, 'IBZ')

if __name__ == "__main__":
    main()