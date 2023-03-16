import datetime
import calendar

from services.selenium_helpers import *
from services.driver import driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from time import sleep
from . scrape_elements import *
  
def extract_flight_data():
    flights = driver.find_elements(By.CLASS_NAME, 'basic-flight-card-layout-container')
    extracted_data = []
    
    for flight in flights:
        if operated_by_brussels_airlines(flight):
            extracted_data.append({ 
                'departure_time': flight.find_element(By.CLASS_NAME, 'bound-departure-datetime').text, 
                'flight_price': flight.find_element(By.CLASS_NAME, 'price-amount').text, 
                'stops': extract_stops(flight),
                'flight_numbers': extract_flight_numbers(flight),
                'num_seats_available': extract_seats(flight)
            })
        
    return extracted_data

def extract_stops(flight):
  stops = flight.find_element(By.CLASS_NAME, 'segments').find_elements(By.TAG_NAME, 'span')
  extracted_stops = []
  for stop in stops:
    extracted_stops.append(stop.text)
  return extracted_stops

def extract_flight_numbers(flight):
  flight_numbers = flight.find_elements(By.CLASS_NAME, EXTRACT_FLIGHTS.flight_number_class)
  extracted_flight_numbers = []
  for flight_number in flight_numbers:
    extracted_flight_numbers.append(flight_number.text)
  return extracted_flight_numbers

def extract_seats(flight):
  try:
    seats_available = flight.find_element(By.CLASS_NAME, EXTRACT_FLIGHTS.seats_available_class).text
    return seats_available.split(' ')[0]
  except NoSuchElementException:
    return 'NULL'

def operated_by_brussels_airlines(flight):
    names = flight.find_elements(By.CLASS_NAME, "operating-airline-name")
    for name in names:
        if name in ["Brussels Airlines", "Lufthansa Cityline", "Lufthansa"]
            return True
    return False
  
def set_extra_options():
  click_by_xpath(extra_options_button)
  
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
  
def execute_search():
  click_by_xpath(SEARCH_BUTTON())
  sleep(5)

def check_rate_limit():
  if driver.title == TITLES.RATE_LIMIT:
    sleep(20)
