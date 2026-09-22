# Open an URL and use Sliders which includes MAX and MIN, print both. Select the current date and a future date and print both.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()

# STEP 1: Open URL
driver.get("https://testautomationpractice.blogspot.com/")
time.sleep(2)

# STEP 2: Find and drag MIN Slider
min_slider = driver.find_element(By.XPATH, "//*[@id="slider-range"]/span[1]")
actions = ActionChains(driver)
actions.drag_and_drop(min_slider, (50, 0)).perform()
time.sleep(1)
min_value = min_slider.get_attribute("value")
print(f"MIN Slider Value: {min_value}")

# STEP 3: Find and drag MAX Slider
max_slider = driver.find_element(By.XPATH, "//*[@id="slider-range"]/span[2]")
actions = ActionChains(driver)
actions.drag_and_drop(max_slider, (200, 0)).perform()
time.sleep(1)
max_value = max_slider.get_attribute("value")
print(f"MAX Slider Value: {max_value}")

# STEP 4: Select Current Date
current_date_field = driver.find_element(By.ID, "start")
current_date_field.send_keys("09/21/2026")
time.sleep(1)
current_date = current_date_field.get_attribute("value")
print(f"Current Date: {current_date}")

# STEP 5: Select Future Date
future_date_field = driver.find_element(By.ID, "end")
future_date_field.send_keys("12/25/2026")
time.sleep(1)
future_date = future_date_field.get_attribute("value")
print(f"Future Date: {future_date}")

time.sleep(2)
driver.quit()