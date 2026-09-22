from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import time


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


try:



    driver.get("https://rahulshettyacademy.com/AutomationPractice/")
    driver.maximize_window()

    time.sleep(5)


    driver.find_element(
        By.XPATH,
        "//input[@value='radio2']"
    ).click()

    time.sleep(3)


    suggestion_box = driver.find_element(
        By.ID,
        "autocomplete"
    )

    suggestion_box.send_keys("ger")

    time.sleep(2)

    # Automatically find and click Germany
    germany = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//li[normalize-space()='Germany']"
            )
        )
    )

    germany.click()

    time.sleep(3)



    dropdown = Select(
        driver.find_element(
            By.ID,
            "dropdown-class-example"
        )
    )

    dropdown.select_by_visible_text("Option1")

    time.sleep(3)

    checkboxes = driver.find_elements(
        By.XPATH,
        "//input[@type='checkbox']"
    )

    for checkbox in checkboxes:

        if not checkbox.is_selected():

            checkbox.click()

            time.sleep(2)



    print("======================================")
    print("Automation completed successfully!")
    print("Radio2       : Selected")
    print("Germany      : Selected")
    print("Dropdown     : Option1 selected")
    print("Checkboxes   : All selected")
    print("======================================")


    # Keep browser open so you can check
    input("\nPress ENTER to close the browser...")


finally:

    driver.quit()