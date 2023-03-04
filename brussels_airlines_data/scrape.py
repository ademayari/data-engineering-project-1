from selenium.webdriver.common.by import By
from time import sleep
from config import driver, destinations, URL
from utils import set_date, extract_flight_data, navigate_portal, set_initial_query, execute_search, get_day, get_current_month

# Setup
current_month = get_current_month()
full_data = {
  'alicante': {}
}

# Scraping Script -------------------------------------------

navigate_portal(driver)
set_initial_query(driver)

for i in range(7):
  day_data = {}
  
  print(current_month, get_day(i))
  set_date(driver, current_month, get_day(i))
  execute_search(driver)

  # Extract data
  flights = driver.find_elements(By.TAG_NAME, "cont-avail")
  extracted_data = extract_flight_data(flights)

  for flight_data in extracted_data:
    flight_time = flight_data[0]
    flight_price = flight_data[1]
    num_stops = flight_data[2]
    
    day_data['flight_time'] = flight_data[0]
    day_data['flight_price'] = flight_data[1]
    day_data['num_stops'] = flight_data[2]
    
  full_data['alicante'][f'day{i}'] = day_data
  print(day_data)
    
print(full_data)