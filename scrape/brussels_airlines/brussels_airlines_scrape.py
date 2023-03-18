from selenium.webdriver.common.by import By
from time import sleep
from . scrape_utils import *
from services.utils import *
from datetime import datetime
from datetime import date
from date_generator import update_airline_dates
from services.utils import write_csv_line
import re
import os
import json

def brussels_airlines_scrape(dest_dates_list):    
    # for destination in dest_dates_list.keys():
        # scrape_destination(dest_dates_list, destination, dest_dates_list[destination])
    scrape_destination(dest_dates_list, 'ALC')

def scrape_destination(dest_dates_list, destination):
    destination_data = dest_dates_list[destination]
    destination_data.reverse()

    while len(destination_data):
        month, day = map(int, destination_data.pop().split('-'))
        
        if driver.current_url == 'chrome://welcome/':
            search_flights(month, day, destination)  
        elif driver.title == 'Flight selection':
            day_clicked = click_date(day)
            
            if day_clicked != -1:
                while day < day_clicked:
                    month, day = map(int, destination_data.pop().split('-'))
            else:
                search_flights(month, day, destination)

        flights_data = extract_flights_data()
        for flight in flights_data:
            write_csv_line('brussels_airlines.csv', format_flight_data(flight, day, month, destination))
      
    sleep(10000)

def format_flight_data(data, month, day, destination):
    data = dotdict(data)

    return {
        'departure_date': f'2023-{month}-{day}',
        'departure_airport': 'BRU',
        'destination_airport': destination,
        'departure_time': data.departure_time, 
        'arrival_time': data.arrival_time,
        'price': data.flight_price, 
        'stops': '-'.join([re.findall(r"[A-Z]+", stop)[0] for stop in data.stops[:-1]]), 
        'flight_numbers': '-'.join(data.flight_numbers).replace(' ', ''), 
        # 'seats_available': data.num_seats_available
    }
    