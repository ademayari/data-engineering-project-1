from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

class ElementLocatedInFlight:
    def __init__(self, flight, locator):
        self.flight = flight
        self.locator = locator

    def __call__(self, driver):
        try:
            element = self.flight.find_element(*self.locator)
            return element if element.is_displayed() else None
        except StaleElementReferenceException:
            return None
