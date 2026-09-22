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


# ==================================================
# BROWSER SELECTION
# ==================================================

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

    raise Exception(
        "Invalid browser name. Please choose 'chrome' or 'firefox'."
    )


try:

    # ==================================================
    # OPEN WEBSITE
    # ==================================================

    driver.get("https://testautomationpractice.blogspot.com/")

    driver.maximize_window()

    time.sleep(5)


    # ==================================================
    # 1. NAME
    # ==================================================

    driver.find_element(
        By.ID,
        "name"
    ).send_keys("Suvajit")

    time.sleep(2)


    # ==================================================
    # 2. EMAIL
    # ==================================================

    driver.find_element(
        By.ID,
        "email"
    ).send_keys("test@example.com")

    time.sleep(2)


    # ==================================================
    # 3. PHONE
    # ==================================================

    driver.find_element(
        By.ID,
        "phone"
    ).send_keys("9876543210")

    time.sleep(2)


    # ==================================================
    # 4. ADDRESS
    # ==================================================

    driver.find_element(
        By.ID,
        "textarea"
    ).send_keys(
        "Kolkata, West Bengal, India"
    )

    time.sleep(2)


    # ==================================================
    # 5. GENDER - MALE
    # ==================================================

    driver.find_element(
        By.ID,
        "male"
    ).click()

    time.sleep(2)


    # ==================================================
    # 6. SELECT MONDAY TO FRIDAY
    # ==================================================

    days = driver.find_elements(
        By.XPATH,
        "//input[@type='checkbox']"
    )

    for day in days:

        value = day.get_attribute("value")

        if value in [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday"
        ]:

            if not day.is_selected():

                day.click()

                time.sleep(1)


    time.sleep(3)


    # ==================================================
    # 7. COUNTRY - INDIA
    # ==================================================

    country = Select(
        driver.find_element(
            By.ID,
            "country"
        )
    )

    country.select_by_visible_text("India")

    time.sleep(3)


    # ==================================================
    # 8. COLOR - RED
    # ==================================================

    colors = Select(
        driver.find_element(
            By.ID,
            "colors"
        )
    )

    colors.select_by_visible_text("Red")

    time.sleep(3)


    # ==================================================
    # 9. SORTED LIST - CAT
    # ==================================================

    animals = Select(
        driver.find_element(
            By.ID,
            "animals"
        )
    )

    animals.select_by_visible_text("Cat")

    time.sleep(3)


    # ==================================================
    # 10. DATE PICKER 1
    # ==================================================

    driver.execute_script(
        "window.scrollTo(0, 600);"
    )

    time.sleep(4)

    date_picker1 = driver.find_element(
        By.ID,
        "datepicker"
    )

    date_picker1.clear()

    date_picker1.send_keys(
        "08/31/2026"
    )

    time.sleep(4)


    # ==================================================
    # 11. DATE PICKER 2
    # ==================================================

    date_picker2 = driver.find_element(
        By.ID,
        "txtDate"
    )

    # Scroll Date Picker 2 into view
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        date_picker2
    )

    time.sleep(3)


    # ==================================================
    # CHECK WHETHER CALENDAR IS ALREADY OPEN
    # ==================================================

    calendars = driver.find_elements(
        By.CSS_SELECTOR,
        ".ui-datepicker"
    )

    calendar_open = False

    for calendar in calendars:

        if calendar.is_displayed():

            calendar_open = True
            break


    # ==================================================
    # OPEN CALENDAR ONLY IF IT IS NOT ALREADY OPEN
    # ==================================================

    if not calendar_open:

        date_picker2.click()

        time.sleep(3)

    else:

        print("Date Picker 2 calendar is already open.")

        time.sleep(2)


    # ==================================================
    # SELECT 31 FROM DATE PICKER 2
    # ==================================================

    date_31 = WebDriverWait(
        driver,
        10
    ).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//div[contains(@class,'ui-datepicker')]"
                "//td[not(contains(@class,'ui-datepicker-other-month'))]"
                "//a[text()='31']"
            )
        )
    )

    date_31.click()

    print("Date Picker 2: 31 selected.")

    time.sleep(5)


    # ==================================================
    # 12. SCROLL TO DATE PICKER 3
    # ==================================================

    driver.execute_script(
        "window.scrollTo(0, 1000);"
    )

    time.sleep(5)


    # ==================================================
    # 13. FIND DATE PICKER 3 INPUTS
    # ==================================================

    date_inputs = driver.find_elements(
        By.XPATH,
        "//input[@type='date']"
    )

    print(
        "Number of Date Picker 3 inputs found:",
        len(date_inputs)
    )


    # ==================================================
    # CHECK BOTH INPUTS
    # ==================================================

    if len(date_inputs) < 2:

        raise Exception(
            "Could not find both Date Picker 3 inputs."
        )


    # ==================================================
    # 14. START DATE
    # ==================================================

    start_date = date_inputs[0]

    driver.execute_script(
        """
        arguments[0].value = '2026-08-31';

        arguments[0].dispatchEvent(
            new Event('input', {bubbles: true})
        );

        arguments[0].dispatchEvent(
            new Event('change', {bubbles: true})
        );
        """,
        start_date
    )

    time.sleep(4)

    print(
        "Start Date:",
        start_date.get_attribute("value")
    )


    # ==================================================
    # 15. END DATE
    # ==================================================

    end_date = date_inputs[1]

    driver.execute_script(
        """
        arguments[0].value = '2026-09-05';

        arguments[0].dispatchEvent(
            new Event('input', {bubbles: true})
        );

        arguments[0].dispatchEvent(
            new Event('change', {bubbles: true})
        );
        """,
        end_date
    )

    time.sleep(4)

    print(
        "End Date:",
        end_date.get_attribute("value")
    )


    # ==================================================
    # 16. SCROLL TO SUBMIT
    # ==================================================

    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);"
    )

    time.sleep(5)


    # ==================================================
    # 17. SUBMIT
    # ==================================================

    submit_button = driver.find_element(
        By.XPATH,
        "//button[text()='Submit']"
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        submit_button
    )

    time.sleep(4)

    submit_button.click()

    print("Submit button clicked.")

    time.sleep(6)


    # ==================================================
    # 18. HOLD BROWSER
    # ==================================================

    input(
        "\n"
        "============================================\n"
        "AUTOMATION COMPLETED\n"
        "============================================\n"
        "\n"
        "Name       : Suvajit\n"
        "Email      : test@example.com\n"
        "Phone      : 9876543210\n"
        "Address    : Kolkata, West Bengal, India\n"
        "Gender     : Male\n"
        "Days       : Monday to Friday\n"
        "Country    : India\n"
        "Color      : Red\n"
        "Animal     : Cat\n"
        "Date 1     : 08/31/2026\n"
        "Date 2     : 31/08/2026\n"
        "Start Date : 31/08/2026\n"
        "End Date   : 05/09/2026\n"
        "\n"
        "Everything is completed.\n"
        "\n"
        "Press ENTER to close the browser.\n"
        "============================================\n"
    )


finally:

    driver.quit()