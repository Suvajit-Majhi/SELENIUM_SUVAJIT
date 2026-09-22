from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://testautomationpractice.blogspot.com/")

wait = WebDriverWait(driver, 10)

driver.execute_script("window.scrollTo({top: 800, left: 0, behavior: 'smooth'});")
time.sleep(2)

parent_menu = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Point Me')]")))
driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", parent_menu)
time.sleep(1)

act = ActionChains(driver)

# Hover over the parent to trigger the dropdown
act.move_to_element(parent_menu).perform()

# NOW wait for the submenu item to actually be visible, then locate it fresh
sub_option = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Mobiles')]")))

# Move to it (still hovering the parent) and click
act.move_to_element(sub_option).click().perform()

print("Hovered over menu and selected Mobiles successfully.")

time.sleep(3)
driver.quit()