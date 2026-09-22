from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import Select

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import time

# What actions for Chrome or Firefox browser
browsername = "chrome"

if browsername.lower() == "chrome":
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install())
    )

elif browsername.lower() == "firefox":
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install())
    )

else:
    raise Exception("Invalid browser name. Please choose 'chrome' or 'firefox'.")

driver.get("https://rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()

# Clicking on the second radio button
driver.find_element(By.XPATH, "//input[@value='radio2']").click()

# Selecting Option1 from dropdown
dropdown = Select(
    driver.find_element(By.XPATH, "//select[@id='dropdown-class-example']")
)
dropdown.select_by_visible_text("Option1")

time.sleep(2)

driver.quit()