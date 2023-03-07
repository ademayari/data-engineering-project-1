from selenium.webdriver.common.by import By
from time import sleep
from config import *
from utils import *

# Setup
month = get_current_month()
full_data = {}

# Scraping Script -------------------------------------------
navigate_portal()
set_extra_options()
set_single_flight()

for destination in DESTINATIONS:
  destination = destination.split(":")
  country = destination[0]
  city = destination[1]
  airport = destination[2]
  full_data[city] = []
  
  for i in range(NUM_DAYS):    
    day = get_day(i)
    
    check_rate_limit()
    set_date(month, day)
    set_destination(country, city, airport)
    execute_search()

    # Extract data
    flights = driver.find_elements(By.TAG_NAME, "cont-avail")
    extracted_data = extract_flight_data(flights)
    full_data[city].append({
      f'{day} {month}': extracted_data
    })
    
print(full_data)