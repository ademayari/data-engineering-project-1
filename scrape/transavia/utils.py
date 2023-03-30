from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException


import random

from config import DIMENSIONS


def randomise_res(driver: webdriver.Chrome):
    size = random.choice(DIMENSIONS)
    driver.set_window_size(size[0], size[1])

def accept_cookies_if_present(driver: webdriver.Chrome):
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cb__button--accept-none"))
        )
        cookie_button.click()
        print("cb found and clicked")
    except NoSuchElementException:
        print("cb button not found")
    except ElementNotInteractableException:
        print("cb button not interactable")
    except TimeoutException:
        print("cb timeout")
# [
#     "flight_id",
#     "from_airport",
#     "to_airport",
#     "departure_date_time",
#     "arrival_date_time",
#     "marketing_airline_name",
#     "flight_number",
#     "price",
#     "link"
# ]
def json_to_csv(res_json):
    result = []
    for flight in res_json["flightOffer"]:
        flight_result = [
            flight["outboundFlight"]["id"],
            flight["outboundFlight"]["departureAirport"]["locationCode"],
            flight["outboundFlight"]["arrivalAirport"]["locationCode"],
            flight["outboundFlight"]["departureDateTime"],
            flight["outboundFlight"]["arrivalDateTime"],
            flight["outboundFlight"]["marketingAirline"]["companyShortName"],
            str(flight["outboundFlight"]["flightNumber"]),
            str(flight["pricingInfoSum"]["totalPriceOnePassenger"]),
            flight["deeplink"]["href"]
        ]
        result.append(';'.join(flight_result))
    return '\n'.join(result)

    

