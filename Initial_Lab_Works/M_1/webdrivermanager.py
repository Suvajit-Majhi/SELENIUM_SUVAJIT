from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService

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

driver.get("https://testautomationpractice.blogspot.com/")
driver.maximize_window()

# Name
driver.find_element(By.XPATH, "//input[@id='name']").send_keys("Suvajit")

# Email
driver.find_element(By.XPATH, "//input[@id='email']").send_keys("test@example.com")

# Phone
driver.find_element(By.XPATH, "//input[@id='phone']").send_keys("9876543210")

# Address
driver.find_element(By.XPATH, "//textarea[@id='textarea']").send_keys(
    "Kolkata, West Bengal"
)


time.sleep(3)

driver.quit()