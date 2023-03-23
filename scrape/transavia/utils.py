from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException

from time import sleep

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
