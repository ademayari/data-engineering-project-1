from selenium.webdriver.common.by import By

from utils.driver import driver

def click_by_css(element):
  return driver.find_element(By.CSS_SELECTOR, element).click()

def find_by_css(element):
  return driver.find_element(By.CSS_SELECTOR, element)
  
def click_by_class(element):
  return driver.find_element(By.CLASS_NAME, element).click()
  
def click_by_xpath(xpath):
  return driver.find_element("xpath", xpath).click()
  
def find_by_xpath(xpath):
  return driver.find_element("xpath", xpath)

