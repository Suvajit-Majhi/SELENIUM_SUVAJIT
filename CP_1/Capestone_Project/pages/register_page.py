"""
register_page.py
----------------
Page Object for the account registration form (route=account/register).

Why this exists: tutorialsninja.com/demo ships with NO pre-existing user
accounts, so a positive-login test cannot rely on hard-coded credentials.
Instead the test registers a brand-new, unique user on the fly and then
logs in with it -- no manual setup, no stale data in users.json.
"""

import uuid

from config.config_loader import settings
from pages.base_page import BasePage


class RegisterPage(BasePage):
    locator_file = "register_locators.yaml"

    REGISTER_URL = settings.active.base_url.rstrip("/") + "/index.php?route=account/register"

    def open_register_page(self):
        self.open(self.REGISTER_URL)
        return self

    @staticmethod
    def unique_email(prefix: str = "qa") -> str:
        return f"{prefix}.{uuid.uuid4().hex[:10]}@example.com"

    def register(self, first_name: str, last_name: str, email: str, telephone: str, password: str):
        self.type_text("firstname_field", first_name)
        self.type_text("lastname_field", last_name)
        self.type_text("email_field", email)
        self.type_text("telephone_field", telephone)
        self.type_text("password_field", password)
        self.type_text("confirm_password_field", password)
        self.click("agree_checkbox")
        self.click("continue_button")
        return self

    def is_registration_successful(self) -> bool:
        if not self.is_displayed("success_heading", timeout=10):
            return False
        return "account has been created" in self.get_text("success_heading").lower()

    def get_error_text(self) -> str:
        return self.get_text("register_error_alert")
