import random
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as wait
from gmail import login_gmail
from captcha import solve_captcha_if_present
import itertools
from gmail import *
from captcha import *

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

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

def set_departure(driver: webdriver.Chrome, departure = "Brussel, België"):
    # hidden_departure_input = driver.find_element(By.NAME, "routeSelection.DepartureStation")
    hidden_departure_input = driver.find_element(By.XPATH, '//*[@id="routeSelection_DepartureStation-input"]')
    # click the departure input
    hidden_departure_input.click()
    # select the first element from the dropdown
    first_element = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[1]/section/div/section/div[1]/div[2]/section/form/section/div[2]/div[1]/div[1]/div/div/div[1]/section/ul/li[1]')
    first_element.click()
#    hidden_departure_input.send_keys(departure)
    time.sleep(10)

def set_destination(driver: webdriver.Chrome, destination= "Malaga, Spanje"):
    # hidden_destination_input = driver.find_element(By.NAME, "routeSelection.ArrivalStation")
    hidden_destination_input = driver.find_element(By.XPATH, '//*[@id="routeSelection_ArrivalStation-input"]')
    hidden_destination_input.send_keys(destination)
    time.sleep(10)
    
def set_one_way(driver: webdriver.Chrome):
    # is_return_flight_input = driver.find_element(By.ID, "dateSelection.isReturnFlight")
    is_return_flight_input = driver.find_element(By.XPATH, '//*[@id="dateSelection.isReturnFlight"]')
    if is_return_flight_input.is_selected(): is_return_flight_input.click()
    time.sleep(10)

def set_date(driver: webdriver.Chrome, date):
    # date_input = driver.find_element(By.ID, "dateSelection_OutboundDate-datepicker")
    date_input = driver.find_element(By.XPATH, '//*[@id="dateSelection_OutboundDate-datepicker"]')
    date_input.send_keys(date)
    time.sleep(10)

def submit_form(driver: webdriver.Chrome):
    # form = driver.find_element(By.ID, "desktop")
    form = driver.find_element(By.XPATH, '//*[@id="desktop"]')
    form.submit()
    time.sleep(10)

def init_transavia_search(driver: webdriver.Chrome):
    driver.get(URL)
    time.sleep(10)

    captcha_result = solve_captcha_if_present(driver)
    if captcha_result:
        print("bypassed captcha")
    else: print("captcha impossible Sadge")

def randomise_res(driver: webdriver.Chrome):
    size = random.choice(DIMENSIONS)
    driver.set_window_size(size[0], size[1])

def scrape_price(driver: webdriver.Chrome, to, date = TEMP_DATE):
    time.sleep(5000)
    set_departure(driver)
    set_destination(driver, to)
    set_one_way(driver)
    set_date(driver, date)
    submit_form(driver)
    time.sleep(30)

def uitgebreid_zoeken(driver: webdriver.Chrome):
    zoeken = driver.find_element(By.CSS_SELECTOR, 'li.HV-gs-type-e--bp0:nth-child(1) > a:nth-child(1)')
    zoeken.click()

def uitgebreid_zoeken(driver: webdriver.Chrome):
    zoeken = driver.find_element(By.CSS_SELECTOR, 'li.HV-gs-type-e--bp0:nth-child(1) > a:nth-child(1)')
    zoeken.click()

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

# def main():
    
#     login_gmail(driver=driver)

#     time.sleep(30)

#     driver.get(URL)
#     time.sleep(20)
    

#     click_captcha(driver)

#     time.sleep(20)
#     uitgebreid_zoeken(driver)
#     time.sleep(30)


#     scrape_price(driver, 'IBZ')


if __name__ == "__main__":
    chrome_opts = ChromeOptions()
    # chrome_opts.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_opts)
