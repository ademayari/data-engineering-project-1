from selenium.webdriver.common.by import By
from time import sleep
from . config import *
from . scrape_utils import *
from services.utils import *
from datetime import datetime
from datetime import date
import re

def brussels_airlines_scrape(month, start_day, day_increment, destinations):
  navigate_portal()
  set_extra_options()
  set_single_flight()

  for destination in destinations:
    destination = destination.split(":")
    country = destination[0]
    city = destination[1]
    airport = destination[2]
    
    for day in range(start_day, start_day + day_increment + 1):
      # Execute query
      check_rate_limit()
      set_date(month, day)
      set_destination(country, city, airport)
      execute_search()

      # Extract flight data
      flights_data = extract_flight_data()
      for flight in flights_data:
        formatted_data = format_flight_data(flight, day, month, country)
        write_csv_line('brussels_airlines.csv', formatted_data)
      
def format_flight_data(data, day, month, country):
  data = dotdict(data)
  
  time_matches = re.findall(r'[0-3][0-9]:[0-5][0-9]', data.departure_time)
  stops = list(map(lambda stop: re.findall(r'[A-Z]+$', stop)[0], data.stops))
  
  return {
    'departure_date': f'2023-{month}-{day}',
    'destination_country': country,
    'departure_airport': 'BRU',
    'destination_airport': stops[-1],
    'departure_time': time_matches[0], 
    'arrival_time': time_matches[1],
    'price': re.findall(r'[0-9]+,?[0-9]*', data.flight_price)[0], 
    'stops': '-'.join(stops), 
    'flight_numbers': '-'.join(data.flight_numbers), 
    'seats_available': data.num_seats_available
  }