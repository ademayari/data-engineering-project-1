from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# returns true if captcha solved succesfully, false if captcha went to imageselection phase
def solve_captcha_if_present(driver: webdriver.Chrome):
    try:
        # navigate to find main iframe
        top_frame = driver.find_element(By.ID, "main-iframe")
        driver.switch_to.frame(top_frame)

        # navigate to inner frame containing captcha
        captcha_frame = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(captcha_frame)

        # wait for checkbox element to appear and click it
        checkbox_element = wait(driver, 10).until(EC.presence_of_element_located((By.ID, "recaptcha-anchor")))
        checkbox_element.click()

        sleep(3)

        popup_element = driver.find_element(By.TAG_NAME, "iframe")
        print("Captcha popup present, resorting to other options")
        return False
    except NoSuchElementException:
        print("something went wrong, captcha not found")
    return True
