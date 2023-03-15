import csv
import json
import os
import calendar
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


destination_codes = ["ALC", "IBZ", "AGP", "PMI", "TFS", "BDS", "NAP", "PMO", "FAO", "HER", "RHO", "CFU"]
#dep_date = datetime.now().strftime("%Y-%m-%d")
start_date = datetime(2023, 6, 1)
end_date = datetime(2023, 6, 30)


csv_headers = ["Departure Airport Name","Departure Airport Code","Arrival Airport Name","Arrival Airport Code","DepartureTime","ArrivalTime","Flight_duration","TotalStops","Price","AvailableSeats","FlightNumber","Data_scraped"]
csv_file_path = "flight_data.csv"
if not os.path.exists("TUI_data"):
    os.mkdir("TUI_data")
if not os.path.exists(csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)


PATH = "C:\School\Data engineering project\chromedriver_win32\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--ignore-certificate-errors')
driver_service = Service(executable_path=PATH)
driver = webdriver.Chrome(service=driver_service, options=options)
driver.maximize_window()
driver.implicitly_wait(10)



for dest_code in destination_codes:
    for day in range((end_date - start_date).days + 1):
        dep_date = (start_date + timedelta(days=day)).strftime("%Y-%m-%d")
        url = f"https://www.tuifly.be/flight/nl/search?flyingFrom%5B%5D=BRU&flyingTo%5B%5D={dest_code}&depDate={dep_date}&adults=1&children=0&childAge=&choiceSearch=true&searchType=pricegrid&nearByAirports=true&currency=EUR&isOneWay=true"
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
        print(json_object)
        
        
       
        
        
        
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
            
            with open(csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([dep_airport_name, dep_airport_code, arr_airport_name, arr_airport_code, dep_time, arr_time, flight_duration, stops, price, available_seats, flightNumber, datetime.now()])
        