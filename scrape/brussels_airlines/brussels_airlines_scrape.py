from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
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

URL = 'https://www.brusselsairlines.com/be/en/homepage'

def brussels_airlines_scrape(dest_dates_list):    
    # for destination in dest_dates_list.keys():
        # scrape_destination(dest_dates_list, destination, dest_dates_list[destination])
    scrape_destination(dest_dates_list, 'ALC')

def scrape_destination(dest_dates_list, destination):
    destination_data = dest_dates_list[destination]
    destination_data.reverse()

    while len(destination_data):
        month, day = map(int, destination_data[-1].split('-'))
        if search_flights_for_day(day, month, destination, destination_data):
            print(f"SCRAPING: {month}-{day}, DAYS LEFT: {len(destination_data)}")
            scrape_day(day, month, destination, destination_data)
        else:
            print(f"NO FLIGHTS FOR: {month}-{day}, DAYS LEFT: {len(destination_data)}")
    
def search_flights_for_day(day, month, destination, destination_data):
    if driver.title == 'Flight selection':
        date_selected = select_date(day)
        
        if date_selected == True:
            # Date has flights!
            return True
        if date_selected == False:
            # Date has no flights
            destination_data.pop()
            return False
        
    search_flights(month, day, destination) 
    return True
    
def scrape_day(day, month, destination, destination_data):
    flights_data = extract_flights_data()
    print(flights_data)
    destination_data.pop()
    for flight in flights_data:
        write_csv_line('brussels_airlines.csv', format_flight_data(flight, day, month, destination)) 

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
        'seats_left': re.findall(r"[0-9]*", data.seats_left)[0]
    }
    