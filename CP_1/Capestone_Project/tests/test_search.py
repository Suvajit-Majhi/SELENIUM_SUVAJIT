"""
test_search.py
---------------
Data-driven product search + add-to-cart, driven by data/test_data.csv.

IMPORTANT DESIGN NOTE (a real gotcha this framework specifically
avoids): pytest.mark.parametrize does NOT work on unittest.TestCase
methods -- pytest collects TestCase classes through unittest's own
TestLoader, which ignores parametrize marks entirely (silently runs
the test once, un-parametrized). This is a well-known pytest
limitation, not a bug in this framework.

The correct, unittest-compatible way to data-drive a TestCase method
is Python's built-in `self.subTest()` context manager: it still runs
under one test method, but reports each data row as an independent
sub-result (a failure in one subTest doesn't stop the others, and
failures are reported per-row). That's what's used below.
"""

import csv
from pathlib import Path

import pytest

from config.config_loader import settings
from pages.search_page import SearchPage
from tests.base_test import BaseTest

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "test_data.csv"


def _load_csv_rows():
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


PRODUCT_NAMES = [row["product_name"] for row in _load_csv_rows()]


@pytest.mark.regression
class TestSearch(BaseTest):

    def test_search_returns_results_for_each_product(self):
        """Data-driven via subTest: one sub-result per row in test_data.csv."""
        search_page = SearchPage(self.driver)

        for product_name in PRODUCT_NAMES:
            with self.subTest(product=product_name):
                search_page.open(settings.active.base_url)
                search_page.search_product(product_name)
                self.assertTrue(
                    search_page.has_results(),
                    f"Expected at least one search result for '{product_name}'.",
                )

    def test_add_product_to_cart(self):
        from config.config_loader import settings
        search_page = SearchPage(self.driver)
        search_page.open(settings.active.base_url)
        search_page.search_product(PRODUCT_NAMES[0])
        self.assertTrue(search_page.has_results(), "No search results to add to cart.")

        search_page.open_product_by_name(PRODUCT_NAMES[0])
        search_page.add_to_cart()
        search_page.accept_alert_if_present(timeout=2)

        success_msg = search_page.get_success_message()
        self.assertIn(
            "success",
            success_msg.lower(),
            f"Expected a success message after adding to cart, got: '{success_msg}'",
        )
