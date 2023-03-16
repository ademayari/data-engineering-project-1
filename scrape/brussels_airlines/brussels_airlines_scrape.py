from selenium.webdriver.common.by import By
from time import sleep
from . scrape_utils import *
from services.utils import *
from datetime import datetime
from datetime import date
from date_generator import update_airline_dates
import re
import os
import json

URL = 'https://www.brusselsairlines.com/gb/en/homepage'

def brussels_airlines_scrape(dest_dates_list):    
    # for destination in dest_dates_list.keys():
        # scrape_destination(dest_dates_list, destination, dest_dates_list[destination])
    scrape_destination(dest_dates_list, 'ALC')

def scrape_destination(dest_dates_list, destination):
    destination_data = dest_dates_list[destination]
    month, day = map(int, destination_data[0].split('-'))
    
    driver.get(URL)
    click_by_css('#cm-acceptAll')
    set_destination(destination)
    set_single_flight()
    set_date(month, day)
    click_by_xpath("//*[text()='Search flights']")
    sleep(20000)

    for date in destination_data:
        month, day = map(int, date.split('-'))

        # Extract flight data
        flights_data = extract_flight_data()
        # for flight in flights_data:
        #     formatted_data = format_flight_data(flight, day, month, country)
        #     write_csv_line('brussels_airlines.csv', formatted_data)
        
        # # Remove the scraped date and update the JSON file
        # destination_data.remove(date)
        # dest_dates_list[destination] = destination_data
      
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