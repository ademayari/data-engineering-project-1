from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as wait
from gmail import login_gmail
from captcha import solve_captcha_if_present
import itertools
from gmail import *
from captcha import *

from utils import randomise_res, accept_cookies_if_present
from search import init_transavia_search, input_departure_airport, input_destination_airport

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


FROM = "BRU"

DESTINATIONS = {
    "spain": ['ALC', 'IBZ', 'AGP', 'PMI', 'TFS'],
    "portugal": ["FAO"],
    "italy": "BDS,NAP,PMO".split(","),
    "greece": "HER,RHO,CFU".split(",")
}



TEMP_DATE = "30-05-2023"

def main(driver):
    try:
        # randomising resolution
        randomise_res(driver)
        # logging in with Gmail before starting
        login_gmail(driver)
        time.sleep(4)

        # init search
        randomise_res(driver)
        init_transavia_search(driver)
        
        accept_cookies_if_present(driver)
        input_departure_airport(driver)
        input_destination_airport(driver, "IBZ")

        
        time.sleep(100000)
    except Exception as e:
        print(e.with_traceback)
    
if __name__ == "__main__":
    chrome_opts = ChromeOptions()
    # chrome_opts.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_opts)

    main(driver)