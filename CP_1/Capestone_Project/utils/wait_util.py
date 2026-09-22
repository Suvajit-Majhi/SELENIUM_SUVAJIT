"""
wait_util.py
------------
Thin wrappers around Selenium's WebDriverWait / expected_conditions
so page objects don't repeat boilerplate.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.config_loader import settings


def _first_displayed(by_locator, require_enabled: bool = False):
    """
    Custom expected-condition: return the FIRST *displayed* element among ALL
    matches of the locator.

    Selenium's built-in visibility_of_element_located / element_to_be_clickable
    only inspect the first DOM match. On sites like OpenCart the same link can
    exist twice (e.g. a hidden header-dropdown 'Logout' AND a visible sidebar
    'Logout'), so the built-ins time out on the hidden one even though a
    visible match exists. This scans every match instead.
    """
    def _condition(driver):
        for element in driver.find_elements(*by_locator):
            try:
                if element.is_displayed() and (not require_enabled or element.is_enabled()):
                    return element
            except Exception:
                continue  # stale element while scanning -> skip it
        return False

    return _condition


def wait_for_visible(driver, by_locator, timeout: int = None):
    timeout = timeout or settings.active.explicit_wait
    return WebDriverWait(driver, timeout).until(_first_displayed(by_locator))


def wait_for_clickable(driver, by_locator, timeout: int = None):
    timeout = timeout or settings.active.explicit_wait
    return WebDriverWait(driver, timeout).until(_first_displayed(by_locator, require_enabled=True))


def wait_for_present(driver, by_locator, timeout: int = None):
    timeout = timeout or settings.active.explicit_wait
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(by_locator))


def wait_for_all_present(driver, by_locator, timeout: int = None):
    timeout = timeout or settings.active.explicit_wait
    return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located(by_locator))


def wait_for_alert(driver, timeout: int = None):
    timeout = timeout or settings.active.explicit_wait
    return WebDriverWait(driver, timeout).until(EC.alert_is_present())


def wait_for_stale(driver, element, timeout: int = None):
    """Block until `element` is detached from the DOM (i.e. the page reloaded)."""
    timeout = timeout or settings.active.explicit_wait
    return WebDriverWait(driver, timeout).until(EC.staleness_of(element))


def wait_for_url_contains(driver, fragment: str, timeout: int = None):
    timeout = timeout or settings.active.explicit_wait
    return WebDriverWait(driver, timeout).until(EC.url_contains(fragment))
