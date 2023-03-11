from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep

def captcha_present(driver: webdriver.Chrome):
    try:
        top_frame = driver.find_element(By.XPATH, "//iframe[@id='main-iframe']")
        driver.switch_to.frame(top_frame)

        sleep(3)

        captcha_frame = driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
        driver.switch_to.frame(captcha_frame)

    except NoSuchElementException:
        return False
    return True
