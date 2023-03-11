import datetime

from services.selenium_helpers import *
from services.driver import driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from time import sleep
from . config import *
from . scrape_elements import *
  
def extract_flight_data():
  flights = driver.find_elements(By.TAG_NAME, EXTRACT_FLIGHTS.flight_tag)
  extracted_data = []
  
  for flight in flights:
    if operated_by_brussels_airlines(flight) and flight_available(flight):
      extracted_data.append({ 
        'departure_time': flight.find_element(By.CLASS_NAME, EXTRACT_FLIGHTS.flight_time_class).text, 
        'flight_price': flight.find_element(By.CLASS_NAME, EXTRACT_FLIGHTS.flight_price_class).text, 
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
  for name in flight.find_elements(By.CLASS_NAME, "airlineName"):
    if (name.text in ["Brussels Airlines", 'Lufthansa']):
      return True
  return False

def flight_available(flight):
  try:
    find_by_xpath(EXTRACT_FLIGHTS.flight_unavailable)
    return False
  except NoSuchElementException:
    return True

def navigate_portal():
  driver.get(URL)
  sleep(3)
  click_by_xpath(PORTAL.confirm_button)
  click_by_xpath(PORTAL.nav_flights_button)
  check_rate_limit()
  
def set_extra_options():
  click_by_xpath(extra_options_button)
  
def set_single_flight():
  click_by_xpath(single_flight_button)
  
def set_destination(country, city, airport):
  ELEMENTS = SET_DESTINATION(country, city, airport)
  
  sleep(3)
  click_by_css(ELEMENTS.input_button)
  
  try:
    click_by_css(ELEMENTS.country_button)
  except NoSuchElementException:
    click_by_xpath("// span[contains(text(),'Sluiten')]")
    sleep(3)
    click_by_css(ELEMENTS.input_button)
    click_by_css(ELEMENTS.country_button)
    
  click_by_css(ELEMENTS.city_button)
  if airport:
    click_by_css(ELEMENTS.airport_button) 
  click_by_css(ELEMENTS.confirm_button)
  
def set_date(month, day):
  ELEMENTS = SET_DATE(month, day)
  
  # Set departure date
  click_by_css(ELEMENTS.input_elem)
  click_by_css(ELEMENTS.reset_button)
  click_by_css(ELEMENTS.close_button)
  sleep(1) # TODO find a way to remove the sleep here
  click_by_css(ELEMENTS.input_elem)

  # Set month
  for i in range(month - datetime.datetime.now().month):
    click_by_css(ELEMENTS.next_month_button)

  element = find_by_xpath(ELEMENTS.day_button)
  webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
  
def execute_search():
  click_by_xpath(SEARCH_BUTTON())
  sleep(5)

def check_rate_limit():
  if driver.title == TITLES.RATE_LIMIT:
    sleep(20)
