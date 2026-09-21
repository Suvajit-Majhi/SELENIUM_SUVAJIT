"""
cart_page.py
------------
Page Object for the shopping cart page (route=checkout/cart).
"""

from pages.base_page import BasePage
from config.config_loader import settings
from utils.wait_util import wait_for_stale


class CartPage(BasePage):
    locator_file = "cart_locators.yaml"

    CART_URL = settings.active.base_url.rstrip("/") + "/index.php?route=checkout/cart"

    def open_cart_page(self):
        self.open(self.CART_URL)
        return self

    def get_cart_row_count(self) -> int:
        return len(self.find_elements("cart_table_rows"))

    def get_quantity(self) -> int:
        """Current value of the (first) quantity box, as an int."""
        field = self.find_element("quantity_input", wait="visible")
        return int(field.get_attribute("value"))

    def update_quantity(self, new_quantity: int):
        """
        Type a new quantity and click the refresh/update button, then WAIT for the
        cart page to reload. OpenCart submits a normal form here, so without this
        wait the next read could still see the old (pre-update) page.
        """
        qty_field = self.find_element("quantity_input", wait="visible")
        qty_field.clear()
        qty_field.send_keys(str(new_quantity))
        self.click("update_cart_button")
        wait_for_stale(self.driver, qty_field)
        return self

    def get_cart_total_text(self) -> str:
        return self.get_text("cart_total_row")

    def is_cart_empty(self) -> bool:
        return self.is_displayed("empty_cart_message", timeout=5)

    def remove_item(self):
        self.click("remove_cart_item_button")
        return self
