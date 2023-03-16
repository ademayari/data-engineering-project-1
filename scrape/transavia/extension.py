from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

EXTENSION_URL ="https://chrome.google.com/webstore/detail/buster-captcha-solver-for/mpbjkejclgfgadiemmefgebjfooflfhl"

def installExtension(driver: webdriver.Chrome, extension_url = EXTENSION_URL):
    driver.get(extension_url)
    sleep(5)
    
    add_to_chrome_button = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div[2]/div[2]/div")
    add_to_chrome_button.click()
    sleep(5)
    add_extension_button = driver.find_element(By.XPATH, "//span[contains(text(),'Toevoegen')]")
    add_extension_button.click()
    sleep(5)
    close_button = driver.find_element(By.XPATH, "//span[contains(text(),'Sluiten')]")
    close_button.click()
    sleep(5)
    driver.refresh()
    sleep(5)