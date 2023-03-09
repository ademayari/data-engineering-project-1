import calendar
import datetime

from utils.selenium_helpers import *
from utils.driver import driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from datetime import date
from time import sleep
from . config import *
from . scrape_elements import *
  
def extract_flight_data(flights):
  extracted_data = []
  
  for flight in flights:
    if operated_by_brussels_airlines(flight) and flight_available(flight):
      extracted_data.append({ 
        'flight_time': flight.find_element(By.CLASS_NAME, EXTRACT_FLIGHTS.flight_time_class).text, 
        'flight_price': flight.find_element(By.CLASS_NAME, EXTRACT_FLIGHTS.flight_price_class).text, 
        'num_stops': flight.find_element(By.CSS_SELECTOR, EXTRACT_FLIGHTS.num_stops_class).text
      })
    
  return extracted_data

def operated_by_brussels_airlines(flight):
  try:
    find_by_xpath(EXTRACT_FLIGHTS.by_brussels_airlines)
    return True
  except NoSuchElementException:
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

  found_date = False
  while not found_date:
    try:
      find_by_xpath(ELEMENTS.month_header)
      found_date = True
    except NoSuchElementException:
      click_by_css(ELEMENTS.next_month_button)

  element = find_by_xpath(ELEMENTS.day_button)
  webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
  
def execute_search():
  click_by_xpath(SEARCH_BUTTON())
  sleep(5)
  
def get_current_month():
  month_number = date.today().month
  return calendar.month_name[month_number].lower()

def get_day(increment=0):
  date = datetime.datetime.today()
  for i in range(increment): 
    date += datetime.timedelta(days=1)
  return date.day

def check_rate_limit():
  if driver.title == TITLES.RATE_LIMIT:
    sleep(20)
