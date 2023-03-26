import datetime
import calendar
import re

from services.selenium_helpers import *
from services.driver import driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from time import sleep
from . locators import ElementLocatedInFlight
from . scrape_elements import *


wait = WebDriverWait(driver, 10)
wait1 = WebDriverWait(driver, 1)
URL = 'https://www.brusselsairlines.com/be/en/homepage'
  
def search_flights(month, day, destination):
    driver.get(URL)
    accept_cookies()
    set_single_flight()
    set_date(month, day)
    set_destination(destination)
    click_by_xpath("//*[text()='Search flights']")
    
def accept_cookies():
    try:
        click_by_css('#cm-acceptAll')
    except:
        pass
  
def has_flight_elements_stabilized(driver):
    initial_flight_count = len(driver.find_elements(By.TAG_NAME, 'refx-upsell-premium-row-pres'))
    sleep(1) 
    final_flight_count = len(driver.find_elements(By.TAG_NAME, 'refx-upsell-premium-row-pres'))
    return initial_flight_count == final_flight_count

def extract_flights_data():
    loading_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "loading-container")))
    wait.until(EC.invisibility_of_element(loading_element))
    wait.until(has_flight_elements_stabilized)
    
    flights = driver.find_elements(By.TAG_NAME, 'refx-upsell-premium-row-pres')
    return [extract_flight_data(flight, i) for i, flight in enumerate(flights) if include_flight(flight)]

def include_flight(flight):
    return operated_by_brussels_airlines(flight) and flight_available(flight)

def extract_flight_data(flight, flight_index):
    stops = extract_stops(flight)
    seats_left = extract_seats_left(flight, flight_index)
    
    return { 
        'departure_time': flight.find_element(By.CLASS_NAME, 'bound-departure-datetime').text, 
        'arrival_time': flight.find_element(By.CLASS_NAME, 'bound-arrival-datetime').text,
        'flight_price': extract_price(flight), 
        'stops': stops['stops'],
        'flight_numbers': stops['flight_numbers'],
        'seats_left': seats_left,
    }
    
def extract_price(flight):
    try:
        return flight.find_element(By.CLASS_NAME, 'price-amount').text
    except:
        return 'N/A'

def extract_stops(flight):
    flight.find_element(By.CLASS_NAME, f"itin-details-link").click()
    dialog = driver.find_element(By.TAG_NAME, 'mat-dialog-container')
    stops = driver.find_elements(By.XPATH, "//bdo[@class='airport-code']")[1::2]
    stops = [stop.text for stop in stops if len(stop.text)]
    flight_numbers = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'seg-marketing-flight-number') or contains(@class, 'seg-marketing-reference-number')]//b")))
    flight_numbers = [flight_number.text for flight_number in flight_numbers]
    click_by_class('close-btn-bottom')

    try:
        wait.until(EC.invisibility_of_element(dialog))
    except:
        click_by_class('close-btn-bottom')

    return {
        "stops": stops,
        "flight_numbers": flight_numbers
    }
    
def extract_seats_left(flight, flight_index):
    # Open expansion panel
    button_locator = (By.XPATH, ".//button[contains(@class, 'flight-card-button-desktop') and contains(@class, 'eco')]")
    button = wait.until(ElementLocatedInFlight(flight, button_locator))
    button.click()
    
    # Expansion panel added to DOM
    flight = get_updated_flight(flight_index)
    expansion_panel = flight.find_element(By.TAG_NAME, 'mat-expansion-panel')
    seats_left = expansion_panel.find_element(By.XPATH, "//span[@class='refx-caption message-value']").text
    
    return seats_left

def operated_by_brussels_airlines(flight):
    names = flight.find_elements(By.CLASS_NAME, "operating-airline-name")
    for name in names:
        if name.text in ["Brussels Airlines", "Lufthansa Cityline", "Lufthansa"]:
            return True
    return False

def flight_available(flight):
    try:
        economy_locator = (By.XPATH, ".//div[contains(@class, 'not-available-cabin-title') and text()='Economy']")
        wait.until(ElementLocatedInFlight(flight, economy_locator))
        return False
    except:
        return True
  
def set_single_flight():
    click_by_class('dropdown-button-secondary')
    click_by_xpath("//div[@role = 'option']", 1)

def set_destination(destination):
    find_by_class('flma-origin-and-destination-input-mb', 1).find_element(By.TAG_NAME, 'input').send_keys(destination)
    sleep(1)
    find_by_class('moving-image').find_element(By.TAG_NAME, 'img').click()
  
def set_date(month_number, day):
    month = calendar.month_name[month_number]
    click_by_xpath("//input[@placeholder = 'Departure']")
    select_month(month_number)
    date_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//td[@aria-label[contains(., '{day} {month}')]]")))
    date_element.click()
    click_by_class('calendar-footer-continue-button')
    
def select_month(month_number):
    month_name = calendar.month_name[month_number]
    wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='March']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='{month_name}']"))).click()

def select_date(target_day):
    try:
        carousel = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'carousel-container')))
    except:
        return None

    li_elems = carousel.find_elements(By.TAG_NAME, 'li')
    dates = [li.find_element(By.CSS_SELECTOR, '.calendar-aria-date').text for li in li_elems]
    dates = [int(re.findall(r" [0-9]* ", date)[0]) for date in dates]
    target_li = [li_elems[i] for i, date in enumerate(dates) if date == target_day]
    
    if len(target_li) == 0:
        # No more days left in carousel
        return None  
    
    button = target_li[0].find_element(By.TAG_NAME, 'button')
    if button.get_attribute('disabled') == 'true':
        # No flights for this day
        return False
    else:
        # There are flights for this day
        button.click()
        return True
    
    return None
            
def get_updated_flight(flight_index):
    return driver.find_elements(By.TAG_NAME, 'refx-upsell-premium-row-pres')[flight_index]