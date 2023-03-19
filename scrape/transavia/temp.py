from selenium import webdriver
from selenium.webdriver.common.by import By

import time


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