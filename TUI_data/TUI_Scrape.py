import csv
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


departure_codes = ["BRU", "OST", "ANR", "LGG"]
destination_codes = ["ALC", "IBZ", "AGP", "PMI", "TFS", "BDS", "NAP", "PMO", "FAO", "HER", "RHO", "CFU"]


csv_headers = ["departure_airport_name", "departure_airport_code", "destination_airport_name", "destination_airport_code", "price", "date_scraped"]
csv_file_path = "TUI_data/flight_data.csv"
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


for dep_code in departure_codes:
    for dest_code in destination_codes:
        
        url = f"https://www.tuifly.be/flight/nl/search?flyingFrom%5B%5D={dep_code}&flyingTo%5B%5D={dest_code}&depDate=2023-04-07&adults=1&children=0&childAge=&choiceSearch=true&searchType=pricegrid&nearByAirports=true&currency=EUR&isOneWay=true&returnDate=2023-04-14"
        driver.get(url)

        try:
            driver.find_element(By.CSS_SELECTOR, "#cmCloseBanner").click()
        except:
            pass

        element = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#page div.container footer > script"))
        )

        data = driver.execute_script("return searchResultsJson")

        dep_airport = data['depAirportData'][0]
        dep_airport_name = dep_airport['name']
        dep_airport_code = dep_airport['id']
        arr_airport = data['arrAirportData'][0] 
        arr_airport_name = arr_airport['name']
        arr_airport_code = arr_airport['id']
        outbound_data = data['dateAvailabilityData']['outboundAvailabilityData']
        selected_date_data = next(filter(lambda x: x['selected'], outbound_data))
        price = selected_date_data['currencyAppendedPrice']

    
        with open(csv_file_path, mode='a', newline='') as file:
          writer = csv.writer(file)
          writer.writerow([dep_airport_name, dep_airport_code, arr_airport_name, arr_airport_code, price, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
