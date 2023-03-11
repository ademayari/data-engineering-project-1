
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

LOGIN_URL = "https://accounts.google.com/v3/signin/identifier?dsh=S-821657923%3A1678318471454155&continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAmgQ&hl=nl&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&ifkv=AWnogHdm2F6NGrRX_srcwnZ_2Frlw_0a3IwoS9vSymRJ3CsV-Oi1-FkSqEqmQtFMAl5ncJ0CH85f5g"
LOGIN_EMAIL = "dep12.test@gmail.com"
LOGIN_PASSWORD = "q.Qn2Jp7PAUmGV3TbAeY"

def login_gmail(driver: webdriver.Chrome):
    driver.implicitly_wait(5)
    driver.get(LOGIN_URL)

    email_input = driver.find_element(By.XPATH, "//input[@type='email']")
    email_input.send_keys(LOGIN_EMAIL)

    first_submit_button = driver.find_element(By.XPATH, "//span[contains(text(),'Volgende')]")
    first_submit_button.click()

    sleep(3)

    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    password_input.send_keys(LOGIN_PASSWORD)

    second_submit_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Volgende')]")
    second_submit_button.click()

    sleep(5)

    