from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import locale
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../utils/"))

def initialize():
  locale.setlocale(locale.LC_ALL, 'nl_NL')
  
  return init_chrome()

def init_chrome():
  options = webdriver.ChromeOptions()
  options.add_experimental_option("detach", True)
  options.headless = True
  options.add_argument('--ignore-certificate-errors')

  user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
  options.add_argument(f'user-agent={user_agent}')
  
  driver_service = Service(executable_path=(PATH + 'chromedriver'))
  driver = webdriver.Chrome(service=driver_service, options=options)
  driver.maximize_window()
  
  return driver
  
def init_firefox():
  options = webdriver.FirefoxOptions()
  # options.headless = True
  
  driver = webdriver.Firefox(executable_path=(PATH + 'geckodriver'), options=options) 
  
  return driver


####### EXPORTS
PATH = os.path.join(os.path.dirname(__file__), "../dependencies/")
URL = 'https://www.brusselsairlines.com/lhg/be/nl/o-d/cy-cy/brussel-alicante'
DESTINATIONS = ["ES:ALC:", "ES:IBZ:", "ES:AGP:", "ES:PMI:", "ES:TCI:TCI", "ES:TCI:TFS", "IT:BDS:", "IT:NAP:", "IT:PMO:", "PT:FAO:", "GR:HER:", "GR:RHO:", "GR:CFU:"]
NUM_DAYS = 1 # 7
driver = initialize()