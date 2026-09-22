from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import time


# Browser selection

browsername = "chrome"

if browsername.lower() == "chrome":

    driver = webdriver.Chrome(
        service=ChromeService(
            ChromeDriverManager().install()
        )
    )

elif browsername.lower() == "firefox":

    driver = webdriver.Firefox(
        service=FirefoxService(
            GeckoDriverManager().install()
        )
    )

else:

    raise Exception(
        "Invalid browser name. Please choose 'chrome' or 'firefox'."
    )


try:

    # Open website

    driver.get(
        "https://testautomationpractice.blogspot.com/"
    )

    driver.maximize_window()

    time.sleep(5)


    # Click Alert button

    driver.find_element(
        By.ID,
        "alertBtn"
    ).click()

    time.sleep(2)


    # Switch to alert

    alert = driver.switch_to.alert


    # Get alert message

    print("\nAlert message:", alert.text)


    # Accept alert

    alert.accept()

    print("Alert accepted successfully")


    time.sleep(3)


   
    print("Task 1 Completed Successfully")
    


    # Hold browser

    input(
        "\nPress ENTER to close the browser..."
    )


finally:

    # Close browser

    driver.quit()