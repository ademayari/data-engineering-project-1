from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from services.driver import driver


wait = WebDriverWait(driver, 10)

# BY CLASS
def click_by_class(class_name, root=driver):
    element = root.find_element(By.CLASS_NAME, class_name)
    element.click()
    return element

def find_elements_by_class(class_name, root=driver):
    return root.find_elements(By.CLASS_NAME, class_name)

def find_element_by_class(class_name, root=driver):
    return root.find_element(By.CLASS_NAME, class_name)


# BY TAG
def click_by_tag(tag, root=driver):
    element = root.find_element(By.TAG_NAME, tag)
    element.click()
    return element

def find_elements_by_tag(tag, root=driver):
    return root.find_elements(By.TAG_NAME, tag)

def find_element_by_tag(tag, root=driver):
    return root.find_element(By.TAG_NAME, tag)

# BY XPATH
def click_by_xpath(xpath, root=driver):
    root.find_element(By.XPATH, xpath).click()
   
def find_elements_by_xpath(xpath, root=driver):
     return root.find_elements(By.XPATH, xpath)

def find_element_by_xpath(xpath, root=driver):
     return root.find_element(By.XPATH, xpath)


# BY CSS
def click_by_css(element, root=driver):
    root.find_element(By.CSS_SELECTOR, element).click()

def find_element_by_css(element, root=driver):
     return root.find_element(By.CSS_SELECTOR, element)


# MISC
def element_not_covered(element):
    try:
        element.click()
        return True
    except WebDriverException:
        return False
    
# WAIT
def wait_clickable(xpath):
    return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

def wait_invisible(element):
    wait.until(EC.invisibility_of_element(element))