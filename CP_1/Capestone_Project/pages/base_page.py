"""
base_page.py
------------
BasePage is the foundation every Page Object inherits from.

UNIQUE APPROACH #1 - Self-healing locators
-------------------------------------------
Instead of a single (By.X, "value") tuple per element, each element in
the locators/*.yaml files maps to an ORDERED LIST of fallback locator
strategies, e.g.:

    email_field:
      - "id:input-email"
      - "name:email"
      - "css:input[placeholder='E-Mail Address']"
      - "xpath://input[@id='input-email']"

find_element() below walks that list in order. The first strategy that
resolves to an element wins. If a locator breaks because the dev team
changed an id, the framework "heals itself" by silently falling
through to the next strategy in the list instead of failing outright,
and it LOGS which strategy actually worked -- so you get visibility
into which locators are becoming stale over time (a real signal a QA
lead would want) without the test suite breaking on day one of a UI
tweak.

UNIQUE APPROACH #3 - Externalized locator repository
------------------------------------------------------
Locators live in YAML files under locators/, not hardcoded in page
classes. Page objects reference them by key
(e.g. self.find("email_field")). If the UI changes, you edit the YAML,
not the code.
"""

from pathlib import Path
from typing import List, Tuple

import yaml
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    InvalidElementStateException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from utils.logger import get_logger
from utils.retry_util import retry
from utils.wait_util import wait_for_clickable, wait_for_present, wait_for_visible

log = get_logger(__name__)

LOCATOR_DIR = Path(__file__).resolve().parent.parent / "locators"

_STRATEGY_MAP = {
    "id": By.ID,
    "name": By.NAME,
    "css": By.CSS_SELECTOR,
    "xpath": By.XPATH,
    "link_text": By.LINK_TEXT,
    "partial_link_text": By.PARTIAL_LINK_TEXT,
    "class_name": By.CLASS_NAME,
    "tag_name": By.TAG_NAME,
}


def _parse_locator_string(locator_str: str) -> Tuple[str, str]:
    """'css:input[name=email]' -> (By.CSS_SELECTOR, 'input[name=email]')"""
    if ":" not in locator_str:
        raise ValueError(
            f"Locator '{locator_str}' is malformed. Expected format 'strategy:value', "
            f"e.g. 'id:input-email'."
        )
    strategy, value = locator_str.split(":", 1)
    strategy = strategy.strip().lower()
    if strategy not in _STRATEGY_MAP:
        raise ValueError(
            f"Unknown locator strategy '{strategy}' in '{locator_str}'. "
            f"Supported: {list(_STRATEGY_MAP.keys())}"
        )
    return _STRATEGY_MAP[strategy], value.strip()


class BasePage:
    """
    Every Page Object subclasses this. It loads its own locator file
    (passed by subclasses via `locator_file`) and exposes self-healing
    find/click/type helpers.
    """

    locator_file: str = None  # subclasses set this, e.g. "login_locators.yaml"

    def __init__(self, driver):
        self.driver = driver
        self._locators = self._load_locators()

    # ------------------------------------------------------------------
    # Locator loading
    # ------------------------------------------------------------------
    def _load_locators(self) -> dict:
        if not self.locator_file:
            raise NotImplementedError(
                f"{self.__class__.__name__} must set a class attribute 'locator_file'."
            )
        path = LOCATOR_DIR / self.locator_file
        if not path.exists():
            raise FileNotFoundError(f"Locator file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data

    def _get_fallback_list(self, key: str, **format_kwargs) -> List[str]:
        if key not in self._locators:
            raise KeyError(
                f"Locator key '{key}' not found in {self.locator_file}. "
                f"Available keys: {list(self._locators.keys())}"
            )
        raw_list = self._locators[key]
        if format_kwargs:
            return [s.format(**format_kwargs) for s in raw_list]
        return raw_list

    # ------------------------------------------------------------------
    # Self-healing element resolution
    # ------------------------------------------------------------------
    def find_element(self, key: str, wait: str = "present", timeout: int = None, **format_kwargs):
        """
        Resolve a locator key to a live WebElement, trying each
        fallback strategy in order.

        wait: "present" | "visible" | "clickable" -- which explicit
        wait condition to apply to each candidate locator.
        """
        wait_fn = {
            "present": wait_for_present,
            "visible": wait_for_visible,
            "clickable": wait_for_clickable,
        }.get(wait, wait_for_present)

        candidates = self._get_fallback_list(key, **format_kwargs)
        last_error = None

        for index, locator_str in enumerate(candidates):
            by, value = _parse_locator_string(locator_str)
            try:
                element = wait_fn(self.driver, (by, value), timeout=timeout)
                if index > 0:
                    log.warning(
                        f"[self-heal] '{key}': primary locator(s) failed, "
                        f"healed using fallback #{index + 1} -> {locator_str}"
                    )
                else:
                    log.debug(f"'{key}' resolved via primary locator -> {locator_str}")
                return element
            except (TimeoutException, NoSuchElementException) as e:
                last_error = e
                log.debug(f"'{key}' candidate #{index + 1} ({locator_str}) failed: {type(e).__name__}")
                continue

        log.error(
            f"[self-heal] '{key}': ALL {len(candidates)} locator strategies failed in "
            f"{self.locator_file}. Candidates tried: {candidates}"
        )
        raise NoSuchElementException(
            f"Could not resolve element '{key}' using any of the {len(candidates)} "
            f"configured locator strategies: {candidates}"
        ) from last_error

    def find_elements(self, key: str, **format_kwargs):
        """Self-healing version that returns a list of matching elements."""
        candidates = self._get_fallback_list(key, **format_kwargs)
        for index, locator_str in enumerate(candidates):
            by, value = _parse_locator_string(locator_str)
            elements = self.driver.find_elements(by, value)
            if elements:
                if index > 0:
                    log.warning(f"[self-heal] '{key}' (multi): healed using fallback #{index + 1} -> {locator_str}")
                return elements
        log.warning(f"'{key}' (multi): no elements found with any of {len(candidates)} strategies")
        return []

    # ------------------------------------------------------------------
    # Common interactions (retry-wrapped for transient flakiness)
    # ------------------------------------------------------------------
    @retry(exceptions=(TimeoutException,))
    def click(self, key: str, **format_kwargs):
        element = self.find_element(key, wait="clickable", **format_kwargs)
        try:
            element.click()
        except ElementClickInterceptedException:
            # Something (sticky header, tooltip, custom-styled checkbox label...) is
            # covering the element. Scroll it into view and click via JS instead.
            log.warning(f"Native click on '{key}' was intercepted; retrying via JavaScript click")
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", element
            )
        log.info(f"Clicked '{key}'")

    @staticmethod
    def _to_editable(element):
        """
        Guard against locators that resolve to a WRAPPER of an input (e.g. a
        <div class="input-group"> around the real <input>). Selenium raises
        InvalidElementStateException if you clear()/send_keys() on such an element,
        so descend to the first <input>/<textarea> inside it when needed.
        """
        if element.tag_name.lower() in ("input", "textarea"):
            return element
        inner = element.find_elements(By.CSS_SELECTOR, "input:not([type='hidden']), textarea")
        if inner:
            log.warning("[self-heal] resolved element was a wrapper, not an input; using the inner input")
            return inner[0]
        return element

    @retry(exceptions=(TimeoutException,))
    def type_text(self, key: str, text: str, clear_first: bool = True, **format_kwargs):
        element = self._to_editable(self.find_element(key, wait="visible", **format_kwargs))
        if clear_first:
            try:
                element.clear()
            except InvalidElementStateException:
                # Fallback for fields that refuse clear(): select-all + delete
                log.warning(f"clear() rejected on '{key}'; falling back to CTRL+A / DELETE")
                element.send_keys(Keys.CONTROL, "a")
                element.send_keys(Keys.DELETE)
        element.send_keys(text)
        log.info(f"Typed into '{key}': {'*' * len(text) if 'password' in key else text}")

    def get_text(self, key: str, **format_kwargs) -> str:
        element = self.find_element(key, wait="visible", **format_kwargs)
        return element.text.strip()

    def is_displayed(self, key: str, timeout: int = 5, **format_kwargs) -> bool:
        try:
            element = self.find_element(key, wait="visible", timeout=timeout, **format_kwargs)
            return element.is_displayed()
        except NoSuchElementException:
            return False

    def open(self, url: str):
        log.info(f"Navigating to {url}")
        self.driver.get(url)

    # ------------------------------------------------------------------
    # Popup / alert handling
    # ------------------------------------------------------------------
    def accept_alert_if_present(self, timeout: int = 3) -> bool:
        """Accepts a native JS alert/confirm/prompt if one appears within `timeout`s."""
        from utils.wait_util import wait_for_alert
        try:
            wait_for_alert(self.driver, timeout=timeout)
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            log.info(f"Accepted native alert: '{alert_text}'")
            return True
        except TimeoutException:
            return False
