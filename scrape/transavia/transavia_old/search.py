from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.action_chains import ActionChains


import time

from captcha import solve_captcha_if_present
from config import URL, DEPARTURE, DEPARTURE_INPUT_ID, DESTINATION_INPUT_ID, TOGGLE_IDS

# some parts inspired by https://github.com/teo-rakan/transavia-selenium

def init_transavia_search(driver: webdriver.Chrome):
    driver.get(URL)
    time.sleep(10)

    captcha_result = solve_captcha_if_present(driver)
    if captcha_result:
        print("bypassed captcha")
    else: print("no captcha present anymore")

def open_toggle(driver: webdriver.Chrome, index: int):
    try:
        container = driver.find_element(By.CLASS_NAME, TOGGLE_IDS[index])
        container_classes = container.get_attribute("class").split()
        if "is-closed" in container_classes:
            container.click()
    except Exception as e:
        print("error")

def input_departure_airport(driver: webdriver.Chrome, departure_airport = DEPARTURE):
    try:
        dep_input = driver.find_element(By.ID, DEPARTURE_INPUT_ID)
        dep_input.clear()
        dep_input.send_keys(departure_airport)
        dep_option = driver.find_element(By.XPATH, f"//*[@id='{DEPARTURE_INPUT_ID}']/following-sibling::*//li")
        dep_option.click()
    except NoSuchElementException:
        print("from not found")
    except ElementNotInteractableException:
        print("element not interactable")
    except TimeoutException:
        print("timeout")

def input_destination_airport(driver: webdriver.Chrome, destination_airport):
    try:
        dest_input = driver.find_element(By.ID, DESTINATION_INPUT_ID)
        dest_input.clear()
        dest_input.send_keys(destination_airport)
        dest_option = driver.find_element(By.XPATH, f"//*[@id='{DESTINATION_INPUT_ID}']/following-sibling::*//li")
        dest_option.click()
    except NoSuchElementException:
        print("to not found")
    except ElementNotInteractableException:
        print("element not interactable")
    except TimeoutException:
        print("timeout")

def set_no_return(driver: webdriver.Chrome):
    try:
        open_toggle(driver, 1)
        flight_type_input = driver.find_element(By.ID, "data-flight-type")
        type_selection = Select(flight_type_input)
        type_selection.select_by_value("Single")
    except NoSuchElementException:
        print("type select not found")
    except ElementNotInteractableException:
        print("type not interactable")
    except TimeoutException:
        print("type select not found")

def set_specific_day(driver: webdriver.Chrome):
    try:
        open_toggle(driver, 1)
        specific_date_input = driver.find_element(
            By.XPATH, "//*[@data-content-container='[data-specific-date]']/following-sibling::*"
        )
        specific_date_input.click()
    except Exception as e:
        print("exception")

def set_date(driver: webdriver.Chrome, date):
    try:
        open_toggle(1)
        date_input = driver.find_element(By.CLASS_NAME, "date-input").click()
        date_input.send_keys(date)
        
    except Exception as e:
        print(e.with_traceback)