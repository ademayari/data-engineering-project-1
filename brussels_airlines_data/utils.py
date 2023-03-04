import calendar
import datetime

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import date
from time import sleep
from config import URL

def set_date(driver, month, day):
  # Reset departure date
  driver.find_element(By.CSS_SELECTOR, "[formcontrolname='departureDate1']").click()
  driver.find_element(By.CSS_SELECTOR, "[class='resetButton']").click()
  driver.find_element(By.CSS_SELECTOR, "[class='closeBtn ng-star-inserted']").click()
  sleep(1) # TODO find a way to remove the sleep here
  
  # Set date
  driver.find_element(By.CSS_SELECTOR, "[formcontrolname='departureDate1']").click()

  date_found = False  
  while not date_found:
    driver.find_element(By.CSS_SELECTOR, "[aria-label='Volgende maand']").click()
    
    try:
      driver.find_element("xpath", f"// h5[contains(text(),\'{month} 2023')]")
      date_found = True
    except NoSuchElementException:
      date_found = False
    
  driver.find_element(By.CLASS_NAME, f"day{day}").click()
  
def extract_flight_data(flights):
  extracted_data = []
  
  for flight in flights:
    if not operated_by_brussels_airlines(flight):
      continue
    
    try:
      flight.find_element("xpath", "// span[contains(text(),\' niet beschikbaar ')]")
    except NoSuchElementException:
      flight_time = flight.find_element(By.CLASS_NAME, "time").text
      flight_price = flight.find_element(By.CLASS_NAME, "cabinPrice").text
      num_stops = flight.find_element(By.CSS_SELECTOR, "[class='nbStops ng-star-inserted']").text
      
      extracted_data.append((flight_time, flight_price, num_stops))
    
  return extracted_data

def operated_by_brussels_airlines(flight):
  try:
    flight.find_element("xpath", "// div[contains(text(),\'Brussels Airlines')]")
  except NoSuchElementException:
    return False
  return True

def navigate_portal(driver):
  driver.get(URL + 'alicante')
  sleep(3)
  driver.find_element("xpath", "// button[contains(text(),\'Akkoord')]").click()
  driver.find_element("xpath", "// a[contains(text(),\' Vluchten vinden ')]").click()
  sleep(20)
  
def set_initial_query(driver):
  driver.find_element("xpath", "// span[contains(text(),\'Meer reisgegevens')]").click()
  driver.find_element("xpath", "// span[contains(text(),\'Enkele reis')]").click()
  
def execute_search(driver):
  driver.find_element("xpath", "// span[contains(text(),\'Start nieuwe zoekopdracht')]").click()
  sleep(5)
  
def get_current_month():
  month_number = date.today().month
  return calendar.month_name[month_number]

def get_day(increment=0):
  date = datetime.datetime.today()
  print(date.day)
  
  for i in range(increment): 
    date += datetime.timedelta(days=1)
    print(date.day)

  return date.day


  
  
