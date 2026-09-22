"""
login_page.py
--------------
Page Object for the login page (route=account/login).
"""

from pages.base_page import BasePage
from config.config_loader import settings


class LoginPage(BasePage):
    locator_file = "login_locators.yaml"

    LOGIN_URL = settings.active.base_url.rstrip("/") + "/index.php?route=account/login"
    LOGOUT_URL = settings.active.base_url.rstrip("/") + "/index.php?route=account/logout"

    def open_login_page(self):
        self.open(self.LOGIN_URL)
        return self

    def logout(self):
        """Log out by hitting the logout route directly (the header link sits in a hidden dropdown)."""
        self.open(self.LOGOUT_URL)
        return self

    def login(self, email: str, password: str):
        self.type_text("email_field", email)
        self.type_text("password_field", password)
        self.click("login_button")
        return self

    def get_login_error_text(self) -> str:
        return self.get_text("login_error_alert")

    def is_login_successful(self) -> bool:
        """OpenCart redirects to the account page and shows a Logout link on success."""
        return self.is_displayed("logout_link", timeout=8)
