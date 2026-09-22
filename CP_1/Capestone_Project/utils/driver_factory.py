"""
driver_factory.py
------------------
Creates and configures a Selenium WebDriver instance based on the
active environment settings (browser, headless, timeouts).

NOTE: This uses Selenium 4's built-in Selenium Manager, which
auto-resolves the correct driver binary for the installed browser
version -- no manual chromedriver download / webdriver-manager
dependency required. Selenium Manager needs outbound internet access
to fetch driver binaries the first time it runs on a machine; in a
locked-down/offline environment, point it at a pre-installed
chromedriver via the CHROME_DRIVER_PATH env var instead (see below).
"""

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.config_loader import settings
from utils.logger import get_logger

log = get_logger(__name__)


def _build_chrome_driver(headless: bool) -> webdriver.Chrome:
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver_path = os.getenv("CHROME_DRIVER_PATH")
    if driver_path:
        log.info(f"Using explicit chromedriver at {driver_path}")
        service = ChromeService(executable_path=driver_path)
        return webdriver.Chrome(service=service, options=options)

    log.info("Using Selenium Manager to auto-resolve chromedriver")
    return webdriver.Chrome(options=options)


def _build_firefox_driver(headless: bool) -> webdriver.Firefox:
    options = FirefoxOptions()
    if headless:
        options.add_argument("-headless")
    return webdriver.Firefox(options=options)


def _build_edge_driver(headless: bool) -> webdriver.Edge:
    options = EdgeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    return webdriver.Edge(options=options)


def get_driver() -> webdriver.Remote:
    """Build a WebDriver instance configured from the active environment."""
    env = settings.active
    browser = env.browser
    log.info(f"Launching browser='{browser}' headless={env.headless} env='{settings.active_env_name}'")

    if browser == "chrome":
        driver = _build_chrome_driver(env.headless)
    elif browser == "firefox":
        driver = _build_firefox_driver(env.headless)
    elif browser == "edge":
        driver = _build_edge_driver(env.headless)
    else:
        raise ValueError(f"Unsupported browser '{browser}' in config.yaml")

    driver.implicitly_wait(env.implicit_wait)
    driver.set_page_load_timeout(env.page_load_timeout)
    if not env.headless:
        driver.maximize_window()

    return driver
