import datetime
import calendar

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
  
def extract_flights_data():
    # Wait for flights to be loaded
    loading_element = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Loading')]"))
    )
    wait.until(EC.staleness_of(loading_element))
    sleep(3)
    
    flights = wait.until(EC.presence_of_all_elements_located((
        By.CSS_SELECTOR, "[class='upsell-premium-row-pres has-indicator-ribbons']"
    )))
    print(len(flights))
    
    return [extract_flight_data(flight) for flight in flights if operated_by_brussels_airlines(flight)]

def extract_flight_data(flight):
    stops = extract_stops(flight)
    
    expansion_panel = flight.find_element(By.TAG_NAME, 'mat-expansion-panel')
    price_cards = expansion_panel.find_elements(By.TAG_NAME, 'refx-price-card')
    
    return { 
        'departure_time': flight.find_element(By.CLASS_NAME, 'bound-departure-datetime').text, 
        'arrival_time': flight.find_element(By.CLASS_NAME, 'bound-arrival-datetime').text,
        'flight_price': flight.find_element(By.CLASS_NAME, 'price-amount').text, 
        'stops': stops['stops'],
        'flight_numbers': stops['flight_numbers'],
        # 'seats_left': expansion_panel.find_element(By.CLASS_NAME, 'message-value').get_attribute('textContent'),
    }

def extract_stops(flight):
    flight.find_element(By.CLASS_NAME, 'itin-details-link').click()
    stop_wrappers = driver.find_elements(By.TAG_NAME, 'refx-segment-details-pres')
    stop_xpath = "//div[contains(@class, 'seg-details-arv-airport')]//bdo[@class='airport-code']"
    stops = [stop.find_element(By.XPATH, stop_xpath).text for stop in stop_wrappers]
    flight_number_xpath = "//span[contains(@class, 'seg-marketing-flight-number')]//b"
    flight_numbers = [stop.find_element(By.XPATH, flight_number_xpath).text for stop in stop_wrappers]
    click_by_class('close-btn-bottom')
    sleep(0.3)

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
    sleep(1) # Remove focus from input
    find_by_class('moving-image').find_element(By.TAG_NAME, 'img').click()
  
def set_date(month_number, day):
    month = calendar.month_name[month_number]
    click_by_xpath("//input[@placeholder = 'Departure']")
    sleep(2)
    try:
        click_by_xpath("//*[text()='Reset Calendar']")
        sleep(2)
    except:
        pass
    find_by_xpath(f"//td[@aria-label[contains(., '{day} {month}')]]").click()
    click_by_class('calendar-footer-continue-button')
