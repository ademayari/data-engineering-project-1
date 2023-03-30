from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

from time import sleep


class ElementLocatedIn:
    def __init__(self, element, xpath):
        self.element = flight
        self.xpath = xpath

    def __call__(self, driver):
        try:
            element = self.element.find_element(By.XPATH, self.xpath)
            return element if element.is_displayed() else None
        except StaleElementReferenceException:
            return None

def has_flight_elements_stabilized(driver):
    initial_flight_count = len(driver.find_elements(By.TAG_NAME, 'refx-upsell-premium-row-pres'))
    sleep(1) 
    final_flight_count = len(driver.find_elements(By.TAG_NAME, 'refx-upsell-premium-row-pres'))
    return initial_flight_count == final_flight_count