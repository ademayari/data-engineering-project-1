import random
from selenium import webdriver
from selenium.webdriver import ChromeOptions
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
from captcha import solve_captcha_if_present
import itertools

URL = "https://www.transavia.com/nl-BE/home/"

FROM = "BRU"

DESTINATIONS = {
    "spain": ['ALC', 'IBZ', 'AGP', 'PMI', 'TFS'],
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

    captcha_result = solve_captcha_if_present(driver)
    if captcha_result:
        print("bypassed captcha")
    else: print("captcha impossible Sadge")

def randomise_res(driver: webdriver.Chrome):
    size = random.choice(DIMENSIONS)
    driver.set_window_size(size[0], size[1])

def scrape_price(driver: webdriver.Chrome, to, date = TEMP_DATE):
    time.sleep(10000)
    set_departure(driver)
    set_destination(driver, to)
    set_one_way(driver)
    set_date(driver, date)
    submit_form(driver)



def main(driver):
    try:
        # randomising resolution
        randomise_res(driver)
        time.sleep(7)
        # logging in with Gmail before starting
        login_gmail(driver)
        time.sleep(4)

        randomise_res(driver)

        init_transavia_search(driver)

        time.sleep(100000)
    except Exception as e:
        print(e.with_traceback)

    
    # scrape_price(driver, 'IBZ')


if __name__ == "__main__":
    chrome_opts = ChromeOptions()
    # chrome_opts.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_opts)
