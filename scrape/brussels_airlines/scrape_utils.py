import datetime
import calendar
import re

from services.selenium_helpers import *
from services.driver import driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from time import sleep
from . scrape_elements import *

wait = WebDriverWait(driver, 20)
URL = 'https://www.brusselsairlines.com/be/en/homepage'
  
def search_flights(month, day, destination):
    driver.get(URL)
    accept_cookies()
    set_single_flight()
    set_date(month, day)
    set_destination(destination)
    click_by_xpath("//*[text()='Search flights']")
    
def accept_cookies():
    try:
        click_by_css('#cm-acceptAll')
    except:
        pass
  
def has_flight_elements_stabilized(driver):
    initial_flight_count = len(driver.find_elements(By.TAG_NAME, 'refx-upsell-premium-row-pres'))
    sleep(1) 
    final_flight_count = len(driver.find_elements(By.TAG_NAME, 'refx-upsell-premium-row-pres'))
    return initial_flight_count == final_flight_count

def extract_flights_data():
    loading_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "loading-container")))
    wait.until(EC.staleness_of(loading_element))
    WebDriverWait(driver, 30).until(has_flight_elements_stabilized)

    flights = driver.find_elements(By.TAG_NAME, 'refx-upsell-premium-row-pres')
    return [extract_flight_data(flight) for flight in flights if operated_by_brussels_airlines(flight)]

def extract_flight_data(flight):
    stops = extract_stops(flight)
    
    return { 
        'departure_time': flight.find_element(By.CLASS_NAME, 'bound-departure-datetime').text, 
        'arrival_time': flight.find_element(By.CLASS_NAME, 'bound-arrival-datetime').text,
        'flight_price': flight.find_element(By.CLASS_NAME, 'price-amount').text, 
        'stops': stops['stops'],
        'flight_numbers': stops['flight_numbers'],
        # 'seats_left': expansion_panel.find_element(By.CLASS_NAME, 'message-value').get_attribute('textContent'),
    }

def extract_stops(flight):
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, f"itin-details-link"))).click()
    stops = driver.find_elements(By.XPATH, "//bdo[@class='airport-code']")[1::2]
    stops = [stop.text for stop in stops if len(stop.text)]
    flight_numbers = driver.find_elements(By.XPATH, "//span[@class='seg-marketing-flight-number']//b")
    flight_numbers = [flight_number.text for flight_number in flight_numbers]
    click_by_class('close-btn-bottom')

    return {
        "stops": stops,
        "flight_numbers": flight_numbers
    }

def operated_by_brussels_airlines(flight):
    names = flight.find_elements(By.CLASS_NAME, "operating-airline-name")
    for name in names:
        if name.text in ["Brussels Airlines", "Lufthansa Cityline", "Lufthansa"]:
            return True
    return False
  
def set_single_flight():
    click_by_class('dropdown-button-secondary')
    click_by_xpath("//div[@role = 'option']", 1)

def set_destination(destination):
    find_by_class('flma-origin-and-destination-input-mb', 1).find_element(By.TAG_NAME, 'input').send_keys(destination)
    sleep(1)
    find_by_class('moving-image').find_element(By.TAG_NAME, 'img').click()
  
def set_date(month_number, day):
    month = calendar.month_name[month_number]
    click_by_xpath("//input[@placeholder = 'Departure']")
    select_month(month_number)
    date_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//td[@aria-label[contains(., '{day} {month}')]]")))
    date_element.click()
    click_by_class('calendar-footer-continue-button')
    
def select_month(month_number):
    month_name = calendar.month_name[month_number]
    wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='March']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='{month_name}']"))).click()

def click_date(target_day):
    try:
        carousel = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'carousel-container')))
    except:
        return -1

    li_elems = carousel.find_elements(By.TAG_NAME, 'li')
    dates = [li.find_element(By.CLASS_NAME, 'cdk-visually-hidden').text for li in li_elems]
    i_days = [(i, int(re.findall(r"[0-9]+", date_)[0])) for (i, date_) in enumerate(dates) if len(date_)]
    i_days = [(i_day[0], i_day[1]) for i_day in i_days if i_day[1] >= target_day]
    
    for next_day in i_days:
        button = li_elems[next_day[0]].find_element(By.TAG_NAME, 'button')
        if 'active' not in button.get_attribute('class').split():
            button.click()
        else:
            continue
        return next_day[1]
    
    return -1

