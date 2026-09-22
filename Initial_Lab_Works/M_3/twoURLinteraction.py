from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://testautomationpractice.blogspot.com/")
parent_window = driver.current_window_handle
time.sleep(2)

new_tab = driver.find_element(By.XPATH, "//a[text()='New Tab']")
new_tab.click()
time.sleep(2)

windows = driver.window_handles

driver.switch_to.window(windows[1])
time.sleep(2)

print("New tab URL:", driver.current_url)

driver.close()
time.sleep(1)

driver.switch_to.window(parent_window)

name_field = driver.find_element(By.ID, "name")  # Adjust ID as needed
name_field.send_keys("Yashraj")

time.sleep(2)
driver.quit()