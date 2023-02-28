import csv
import os
import json
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\School\Data engineering project\chromedriver_win32\chromedriver.exe"

destinations = {
    "spanje": ["ALC", "IBZ", "AGP", "PMI"],
    "italie": ["BDS", "NAP", "PMO"],
    "portugal": ["FAO"],
    "griekenland": ["HER", "RHO","CFU"]
}



options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--ignore-certificate-errors')
driver_service = Service(executable_path=PATH)
driver = webdriver.Chrome(service=driver_service,options=options)
driver.maximize_window()
driver.implicitly_wait(25)

for country, codes in destinations.items():
    for code in codes:
        url = f"https://www.tuifly.be/flight/nl/search?flyingFrom%5B%5D=BRU&flyingTo%5B%5D={code}&depDate=2023-04-07&adults=1&children=0&childAge=&choiceSearch=true&searchType=pricegrid&nearByAirports=true&currency=EUR&isOneWay=true&returnDate=2023-04-14"
        driver.get(url)
        driver.find_element(By.CSS_SELECTOR, "#cmCloseBanner").click()

        element = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#page div.container footer > script"))
        )

# retrieve the data from the var searchResultsJson
data = driver.execute_script("return searchResultsJson")

print(data)


# get the flight search criteria
search_criteria = data['flightSearchCriteria']


dep_airport = data['depAirportData'][0] 
dep_airport_name = dep_airport['name']
dep_airport_code = dep_airport['id']
arr_airport = data['arrAirportData'][0] 
arr_airport_name = arr_airport['name']
arr_airport_code = arr_airport['id']


outbound_data = data['dateAvailabilityData']['outboundAvailabilityData']
selected_date_data = next(filter(lambda x: x['selected'], outbound_data))
price = selected_date_data['currencyAppendedPrice']



file_path = 'TUI_data/flight_data.csv'


if os.path.exists(file_path):
    
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow([dep_airport_name, dep_airport_code, arr_airport_name, arr_airport_code, price])
else:
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Departure Airport Name', 'Departure Airport Code', 'Arrival Airport Name', 'Arrival Airport Code', 'Price'])
        
        writer.writerow([dep_airport_name, dep_airport_code, arr_airport_name, arr_airport_code, price])




    

    