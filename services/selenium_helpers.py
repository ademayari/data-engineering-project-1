from selenium.webdriver.common.by import By

from services.driver import driver

def click_by_css(element):
    return driver.find_element(By.CSS_SELECTOR, element).click()

def find_by_css(element):
     return driver.find_element(By.CSS_SELECTOR, element)
  
def click_by_class(element):
    return driver.find_element(By.CLASS_NAME, element).click()
  
def find_by_class(element, index=0):
    return driver.find_elements(By.CLASS_NAME, element)[index]

def click_by_xpath(xpath, index=0):
    driver.find_elements("xpath", xpath)[index].click()
  
def find_by_xpath(xpath):
     return driver.find_element("xpath", xpath)

