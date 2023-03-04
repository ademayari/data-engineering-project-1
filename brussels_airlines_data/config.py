from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import os

abs_path = os.path.dirname(__file__)
PATH = os.path.join(abs_path, "../dependencies/chromedriver")
URL = 'https://www.brusselsairlines.com/lhg/be/nl/o-d/cy-cy/brussel-'

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
# options.headless = True
options.add_argument('--ignore-certificate-errors')
driver_service = Service(executable_path=PATH)
driver = webdriver.Chrome(service=driver_service, options=options)
driver.maximize_window()

# Initialize destinations
destinations = ['alicante', 'ibiza', 'malaga', 'palma', 'tenerife', 'faro', 'brindisi', 'napels', 'palermo', 'corfu', 'kreta', 'rhodos']