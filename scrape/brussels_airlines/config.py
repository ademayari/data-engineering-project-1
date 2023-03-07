from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import locale

def initialize():
  options = webdriver.ChromeOptions()
  options.add_experimental_option("detach", True)
  options.headless = True
  options.add_argument('--ignore-certificate-errors')
  
  driver_service = Service(executable_path=PATH)
  driver = webdriver.Chrome(service=driver_service, options=options)
  driver.maximize_window()
  
  locale.setlocale(locale.LC_ALL, 'nl_NL')
  
  return driver

####### EXPORTS
PATH = os.path.join(os.path.dirname(__file__), "../dependencies/chromedriver")
URL = 'https://www.brusselsairlines.com/lhg/be/nl/o-d/cy-cy/brussel-alicante'
DESTINATIONS = ["ES:ALC:", "ES:IBZ:", "ES:AGP:", "ES:PMI:", "ES:TCI:TCI", "ES:TCI:TFS", "IT:BDS:", "IT:NAP:", "IT:PMO:", "PT:FAO:", "GR:HER:", "GR:RHO:", "GR:CFU:"]
NUM_DAYS = 1 # 7
driver = initialize()