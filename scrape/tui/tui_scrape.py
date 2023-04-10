import csv
import json
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from services.driver import driver



datenow = datetime.now().strftime("%Y-%m-%d")

def tui_scrape(tui_dates):


    csv_headers = ["Departure Airport Name","Departure Airport Code","Arrival Airport Name","Arrival Airport Code","DepartureTime","ArrivalTime","Flight_duration","TotalStops","Price","AvailableSeats","FlightNumber"]
    csv_file_path = f'TUI_flight_data_{datenow}.csv'

    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(csv_headers)


        for city, dates in tui_dates.items():
            for date in dates:
            
                url = f"https://www.tuifly.be/flight/nl/search?flyingFrom%5B%5D=BRU&flyingTo%5B%5D={city}&depDate=2023-{date}&adults=1&children=0&childAge=&choiceSearch=true&searchType=pricegrid&nearByAirports=true&currency=EUR&isOneWay=true"
                driver.get(url)

                try:
                    driver.find_element(By.CSS_SELECTOR, "#cmCloseBanner").click()
                except:
                    pass

                element = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div#page div.container footer > script"))
                )

                data = driver.execute_script("return JSON.stringify(searchResultsJson)")
                json_object = json.loads(data)
                

                for flight in json_object['flightViewData']:
                    dep_airport_name = flight['journeySummary']['departAirportName']
                    dep_airport_code = flight['journeySummary']['departAirportCode']
                    arr_airport_name = flight['journeySummary']['arrivalAirportName']
                    arr_airport_code = flight['journeySummary']['arrivalAirportCode']
                    dep_date = flight['journeySummary']['departDate']
                    dep_time = flight['journeySummary']['depTime']
                    arr_date = flight['journeySummary']['arrivalDate']
                    arr_time = flight['journeySummary']['arrivalTime']
                    flight_duration = flight['journeySummary']['journeyDuration']
                    price = flight['originalTotalPrice']
                    stops = flight['journeySummary']['totalNumberOfStops']
                    available_seats = flight['journeySummary']['availableSeats']
                    flightNumber = flight['flightsectors'][0]['flightNumber']

                    print(f"SCRAPING FOR DEPARTURE {dep_airport_name} TO {arr_airport_name} ON {dep_date} AT {dep_time}")


                        
                    with open(csv_file_path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([dep_airport_name, dep_airport_code, arr_airport_name, arr_airport_code,dep_date + ' ' + dep_time, arr_date + ' ' + arr_time, flight_duration, stops, price, available_seats, flightNumber])

       