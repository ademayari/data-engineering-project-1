from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import os
from time import sleep

abs_path = os.path.dirname(__file__)
PATH = os.path.join(abs_path, "../dependencies/chromedriver")
URL = 'https://www.brusselsairlines.com/lhg/be/nl/o-d/cy-cy/brussel-'

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
# options.headless = True
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(PATH, options=options)
driver.maximize_window()

# Initialize destinations
spain = ['alicante', 'ibiza', 'malaga', 'palma', 'tenerife']
portugal = ['faro']
italy = ['brindisi, napels, palermo']
greece = ['corfu, kreta, rhodos']
destinations = spain + portugal + italy + greece

################ Functions
def setDate():
  # Select Departure Date
  driver.find_element(By.CSS_SELECTOR, "[formcontrolname='departureDate1']").click()
  driver.find_element(By.CSS_SELECTOR, "[class='resetButton']").click()
  driver.find_element(By.CSS_SELECTOR, "[class='closeBtn ng-star-inserted']").click()
  sleep(1) # TODO find a way to remove the sleep here
  driver.find_element(By.CSS_SELECTOR, "[formcontrolname='departureDate1']").click()

  date_exists = False  
  while not date_exists:
    driver.find_element(By.CSS_SELECTOR, "[aria-label='Volgende maand']").click()
    try:
      driver.find_element(By.CSS_SELECTOR, "[aria-label='zaterdag 1st april 2023']")
      date_exists = True
    except NoSuchElementException:
        date_exists = False
    
  driver.find_element(By.CSS_SELECTOR, "[aria-label='zaterdag 1st april 2023']").click()
  
def extractFlightData(flights):
  extracted_data = []
  
  for flight in flights:
    if not operatedByBrusselsAirlines(flight):
      continue
    
    try:
      flight.find_element_by_xpath("// span[contains(text(),\' niet beschikbaar ')]")
    except NoSuchElementException:
      flight_time = flight.find_element(By.CLASS_NAME, "time").text
      flight_price = flight.find_element(By.CLASS_NAME, "cabinPrice").text
      num_stops = flight.find_element(By.CSS_SELECTOR, "[class='nbStops ng-star-inserted']").text
      
      extracted_data.append((flight_time, flight_price, num_stops))
    
  return extracted_data
    
def operatedByBrusselsAirlines(flight):
  try:
    flight.find_element_by_xpath("// div[contains(text(),\'Brussels Airlines')]")
  except NoSuchElementException:
    return False
  return True

################ Script

# Set up query
driver.get(URL + 'alicante')
sleep(3)
driver.find_element_by_xpath("// button[contains(text(),\'Akkoord')]").click()
driver.find_element_by_xpath("// a[contains(text(),\' Vluchten vinden ')]").click()
sleep(20)
driver.find_element_by_xpath("// span[contains(text(),\'Meer reisgegevens')]").click()
driver.find_element_by_xpath("// span[contains(text(),\'Enkele reis')]").click()
setDate()

# Search
driver.find_element_by_xpath("// span[contains(text(),\'Start nieuwe zoekopdracht')]").click()
sleep(5)

# Extract data
flights = driver.find_elements(By.TAG_NAME, "cont-avail")
extracted_data = extractFlightData(flights)

for flight_data in extracted_data:
  flight_time = flight_data[0]
  flight_price = flight_data[1]
  num_stops = flight_data[2]
  
  print("FLIGHT DATA -----------------------------------------------")
  print('Destination: Alicante')
  print('Flight Time: ' + flight_time)
  print('Flight Price: ' + flight_price.split(" ")[1] + " EUR")
  print('Number of Stops: ' + num_stops)

driver.quit()
