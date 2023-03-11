from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import undetected_chromedriver as uc 

PATH = os.path.join(os.path.dirname(__file__), "../dependencies/")


def init_chrome():
  options = uc.ChromeOptions()
  options.headless = True
  
  driver = uc.Chrome(options=options)
  driver.maximize_window()
  
  return driver
  
def init_firefox():
  options = webdriver.FirefoxOptions()
  options.headless = True
  
  driver = webdriver.Firefox(executable_path=(PATH + 'geckodriver'), options=options) 
  
  return driver

driver = init_chrome()