"""
test_cart.py
------------
Full end-to-end flow: search -> add to cart -> update quantity ->
verify cart contents/total. Chains the three page objects together,
demonstrating the POM composition the capstone brief asks for.
"""

import pytest

from config.config_loader import settings
from pages.cart_page import CartPage
from pages.search_page import SearchPage
from tests.base_test import BaseTest


@pytest.mark.regression
class TestCart(BaseTest):

    PRODUCT_NAME = "MacBook"

    def test_update_quantity_and_verify_cart(self):
        # 1. Search and add to cart
        search_page = SearchPage(self.driver)
        search_page.open(settings.active.base_url)
        search_page.search_product(self.PRODUCT_NAME)
        self.assertTrue(search_page.has_results(), f"No results for '{self.PRODUCT_NAME}'.")

        search_page.open_product_by_name(self.PRODUCT_NAME)
        search_page.add_to_cart()
        search_page.accept_alert_if_present(timeout=2)

        # 2. Go to cart and verify the item landed there
        cart_page = CartPage(self.driver)
        cart_page.open_cart_page()
        row_count_before = cart_page.get_cart_row_count()
        self.assertGreater(row_count_before, 0, "Cart is empty after adding a product.")

        # 3. Update quantity
        total_before = cart_page.get_cart_total_text()
        cart_page.update_quantity(3)

        # 4. Verify the cart really updated: quantity box shows 3 and the total changed
        self.assertEqual(cart_page.get_quantity(), 3, "Quantity box did not persist the updated value.")
        total_text = cart_page.get_cart_total_text()
        self.assertNotEqual(total_text, total_before, "Cart total did not change after quantity update.")
        self.assertTrue(len(total_text) > 0, "Cart total is empty after quantity update.")
        self.assertIn("$", total_text, f"Expected a currency-formatted total, got '{total_text}'")

    def test_empty_cart_shows_message(self):
        """Sanity check for the cart page's empty state (assuming a fresh session)."""
        cart_page = CartPage(self.driver)
        cart_page.open_cart_page()
        if cart_page.get_cart_row_count() == 0:
            self.assertTrue(
                cart_page.is_cart_empty(),
                "Cart has 0 rows but the empty-cart message is not displayed.",
            )
        else:
            self.skipTest("Cart is not empty in this session; skipping empty-state check.")
