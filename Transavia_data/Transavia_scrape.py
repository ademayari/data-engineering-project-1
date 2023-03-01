from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import itertools

URL = "https://www.transavia.com/nl-BE/home/"

abs_path = os.path.dirname(__file__)
PATH = os.path.join(abs_path, "../dependencies/chromedriver")

options = webdriver.ChromeOptions()
# options.headless = True

driver = webdriver.Chrome(PATH, options=options)

FROM = "Brussel"

DESTINATIONS = {
    "spain": "alicante,ibiza,malaga,palma,tenerife".split(","),
    "portugal": ["faro"],
    "italy": "brindisi,napels,palermo".split(","),
    "greece": "corfu,kreta,rhodos".split(",")
}

# FROM: Brussels
# TO: x
# date: today + (4 hours, 1 day, 7 days, 14 days, 1 month, 2 months, 4 months, 6 months)
# people: 1 adult
# deselect return flight

def setDeparture(driver: webdriver.Chrome, departure = "BRU"):
    hidden_departure_input = driver.find_element(By.NAME, "routeSelection.DepartureStation")
    hidden_departure_input.send_keys(departure)

def set_destination(driver: webdriver.Chrome, destination):
    hidden_destination_input = driver.find_element(By.NAME, "routeSelection.ArrivalStation")
    hidden_destination_input.send_keys(destination)
    
def set_one_way(driver: webdriver.Chrome):
    is_return_flight_input = driver.find_element(By.ID, "dateSelection.isReturnFlight")
    if is_return_flight_input.is_selected(): is_return_flight_input.click()

def main():
    for city in itertools.chain(*DESTINATIONS.values()):
        pass

if __name__ == "__main__":
    main()