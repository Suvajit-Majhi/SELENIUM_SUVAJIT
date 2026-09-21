"""
test_login.py
--------------
NOTE ON TEST DATA: tutorialsninja.com/demo (OpenCart demo) does not
ship pre-existing user accounts, so the positive login test creates its
own: it registers a brand-new unique user (name/phone/password come from
data/users.json -> "new_user_template"), logs out, then logs back in with
those credentials. No manual account setup is required.
"""

import json
from pathlib import Path

import pytest

from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from tests.base_test import BaseTest

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "users.json"


def _load_users() -> dict:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


USERS = _load_users()


@pytest.mark.smoke
class TestLogin(BaseTest):

    def test_invalid_login_shows_error(self):
        """Negative test: wrong credentials should show an error alert, not log in."""
        user = USERS["invalid_user"]
        login_page = LoginPage(self.driver)
        login_page.open_login_page()
        login_page.login(user["email"], user["password"])

        self.assertFalse(
            login_page.is_login_successful(),
            "Login unexpectedly succeeded with invalid credentials.",
        )
        error_text = login_page.get_login_error_text()
        self.assertTrue(len(error_text) > 0, "Expected a non-empty login error message.")

    @pytest.mark.regression
    def test_valid_login_succeeds(self):
        """
        Positive test, fully self-contained:
        register a fresh unique user -> log out -> log in with that user.
        """
        tmpl = USERS["new_user_template"]
        email = RegisterPage.unique_email()

        # 1. Create the account
        register_page = RegisterPage(self.driver)
        register_page.open_register_page()
        register_page.register(
            tmpl["first_name"], tmpl["last_name"], email, tmpl["telephone"], tmpl["password"]
        )
        self.assertTrue(
            register_page.is_registration_successful(),
            "Registration did not show the 'Your Account Has Been Created!' confirmation.",
        )

        # 2. Log out (registration auto-logs the user in), then log in for real
        login_page = LoginPage(self.driver)
        login_page.logout()
        login_page.open_login_page()
        login_page.login(email, tmpl["password"])

        self.assertTrue(
            login_page.is_login_successful(),
            f"Expected successful login for freshly registered user '{email}' "
            "(Logout link visible) but it was not found.",
        )
