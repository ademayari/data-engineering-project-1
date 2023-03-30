import datetime
import calendar
import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from services.selenium_helpers import *
from services.driver import driver
from .conditions import *


wait = WebDriverWait(driver, 10)
URL = 'https://www.brusselsairlines.com/be/en/homepage'
operator_names = ["Brussels Airlines", "Lufthansa Cityline", "Lufthansa"]
current_month_name = calendar.month_name[datetime.datetime.now().month]

### Elements
FLIGHT_ROW_TAG = 'refx-upsell-premium-row-pres'
ECONOMY_AVAILABLE = ".//div[contains(@class, 'not-available-cabin-title') and text()='Economy']"
EXPANSION_PANEL_BUTTON = ".//button[contains(@class, 'eco')]"
NUM_SEATS = ".//span[@class='refx-caption message-value']"
SEARCH_FLIGHTS_BUTTON = "//*[text()='Search flights']"
ACCEPT_COOKIES_BUTTON = "//button[@id='cm-acceptAll']"
DEPARTURE_TIME = "bound-departure-datetime"
ARRIVAL_TIME = "bound-arrival-datetime"
STOP = "//bdo[@class='airport-code']"
FLIGHT_NUMBER = "//span[contains(@class, 'seg-marketing-flight-number') or contains(@class, 'seg-marketing-reference-number')]//b"
OPEN_CALENDAR_BUTTON = "//input[@placeholder = 'Departure - return']"
ONE_WAY_BUTTON = "//span[@class='custom-control-description']"
CALENDAR_CONTINUE = "calendar-footer-continue-button"
CAROUSEL = "carousel-container"
CAROUSEL_DATE = '.calendar-aria-date'
DESTINATION_INPUT = "//input[@placeholder='To']"
REMOVE_FOCUS_IMAGE = "//div[@class='moving-image']//img"
MONTH_DROPDOWN = f"//span[text()='{current_month_name}']"
MONTH_OPTION = lambda month_name: f"//div[text()='{month_name}']"
DAY_BUTTON = lambda day, month_name: f"//td[@aria-label[contains(., '{day} {month_name}')]]"
OPERATING_AIRLINE = "operating-airline-name"
LOADING_CONTAINER = "loading-container"
ITIN_DETAILS_BUTTON = "itin-details-link"
ITIN_DIALOG = "mat-dialog-container"
ITIN_CLOSE = "close-btn-bottom"
EXPANSION_PANEL = "mat-expansion-panel"
FLIGHT_PRICE = ".//button[contains(@class, 'eco')]//*[contains(@class, 'price-amount')]"
  

def search_flights(month, day, destination):
    driver.get(URL)
    accept_cookies()
    set_destination(destination)
    set_date(month, day)
    click_by_xpath(SEARCH_FLIGHTS_BUTTON)
    
def accept_cookies():
    try:
        button = click_by_xpath(ACCEPT_COOKIES_BUTTON)
        wait_invisible(button)
    except:
        # Cookies already accepted
        pass

def extract_flights_data():
    wait_invisible(find_element_by_class(LOADING_CONTAINER))
    wait.until(has_flight_elements_stabilized)
    flights = find_elements_by_tag(FLIGHT_ROW_TAG)
    return [extract_flight_data(flight, i) for i, flight in enumerate(flights) if include_flight(flight)]


def include_flight(flight):
    return operated_by_brussels_airlines(flight) and flight_available(flight)


def extract_flight_data(flight, flight_index):
    stops = extract_stops(flight)
    seats_left = extract_seats_left(flight, flight_index)
    
    return { 
        'departure_time': find_element_by_class(DEPARTURE_TIME, flight).text, 
        'arrival_time': find_element_by_class(ARRIVAL_TIME, flight).text,
        'flight_price': extract_price(flight), 
        'stops': stops[0],
        'flight_numbers': stops[1],
        'seats_left': seats_left,
    }

    
def extract_price(flight):
    try:
        price_element = flight.find_element_by_xpath(FLIGHT_PRICE)
        return price_element.text
    except:
        return 'N/A'


def extract_stops(flight):
    click_by_class(ITIN_DETAILS_BUTTON, flight)
    dialog = find_elements_by_tag(ITIN_DIALOG)
    stops = [stop.text for stop in find_elements_by_xpath(STOP)[1::2] if len(stop.text)]
    flight_numbers = [flight_number.text for flight_number in find_elements_by_xpath(FLIGHT_NUMBER)]
    click_by_class(ITIN_CLOSE)

    try:
        wait_invisible(dialog)
    except:
        click_by_class(ITIN_CLOSE)

    return (stops, flight_numbers)

    
def extract_seats_left(flight, flight_index):
    click_by_xpath(EXPANSION_PANEL_BUTTON, flight)
    
    # Expansion panel added to DOM
    flight = find_elements_by_tag(FLIGHT_ROW_TAG)[flight_index]
    expansion_panel = find_element_by_tag(EXPANSION_PANEL, flight)
    
    return find_element_by_class(NUM_SEATS, expansion_panel).text


def operated_by_brussels_airlines(flight):
    for name in find_elements_by_class(OPERATING_AIRLINE, flight):
        if name.text in operator_names:
            return True
    return False


def flight_available(flight):
    try:
        wait.until(ElementLocatedIn(flight, ECONOMY_AVAILABLE))
        return False
    except:
        return True


def set_destination(destination):
    find_element_by_xpath(DESTINATION_INPUT).send_keys(destination)
    sleep(1)
    click_by_xpath(REMOVE_FOCUS_IMAGE)


def set_date(month_number, day):
    month = calendar.month_name[month_number]
    click_by_xpath(OPEN_CALENDAR_BUTTON)
    wait_clickable(ONE_WAY_BUTTON).click()
    wait_clickable(MONTH_DROPDOWN).click()
    wait_clickable(MONTH_OPTION(month)).click()
    wait_clickable(DAY_BUTTON(day, month)).click()
    click_by_class(CALENDAR_CONTINUE)


def select_date(target_day):
    try:
        carousel = find_element_by_class(CAROUSEL)
    except:
        return None

    li_elems = find_elements_by_tag('li', carousel)
    dates = [find_element_by_css(CAROUSEL_DATE, li).text for li in li_elems]
    dates = [int(re.findall(r" [0-9]* ", date)[0]) for date in dates]
    target_li = [li_elems[i] for i, date in enumerate(dates) if date == target_day]
    
    if len(target_li) == 0:
        # No more days left in carousel
        return None  
    
    button = find_element_by_tag('button', target_li[0])
    if button.get_attribute('disabled') == 'true':
        # No flights for this day
        return False
    else:
        # There are flights for this day
        button.click()
        return True
    
    return None
