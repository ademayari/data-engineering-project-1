from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import undetected_chromedriver as uc 

def init_chrome():
    options = uc.ChromeOptions()
    # options.headless = True

    driver = uc.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    return driver

driver = init_chrome()