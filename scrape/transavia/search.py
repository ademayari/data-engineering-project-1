from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


import time

from captcha import solve_captcha_if_present
from config import URL, DEPARTURE, DEPARTURE_INPUT_ID, DESTINATION_INPUT_ID

# some parts inspired by https://github.com/teo-rakan/transavia-selenium

def init_transavia_search(driver: webdriver.Chrome):
    driver.get(URL)
    time.sleep(10)

    captcha_result = solve_captcha_if_present(driver)
    if captcha_result:
        print("bypassed captcha")
    else: print("no captcha present anymore")

def input_departure_airport(driver: webdriver.Chrome, departure_airport = DEPARTURE):
    try:
        dep_input = driver.find_element(By.ID, DEPARTURE_INPUT_ID)
        dep_input.clear()
        dep_input.send_keys("Brussel")
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
        dep_input = driver.find_element(By.ID, DEPARTURE_INPUT_ID)
        dep_input.clear()
        dep_input.send_keys("Brussel")
        dep_option = driver.find_element(By.XPATH, f"//*[@id='{DEPARTURE_INPUT_ID}']/following-sibling::*//li")
        dep_option.click()
    except NoSuchElementException:
        print("to not found")
    except ElementNotInteractableException:
        print("element not interactable")
    except TimeoutException:
        print("timeout")