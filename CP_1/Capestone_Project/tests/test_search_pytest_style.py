"""
test_search_pytest_style.py
-----------------------------
The other half of the "true hybrid": plain PyTest-style tests (no
unittest.TestCase) where pytest.mark.parametrize DOES work natively,
generating one independent, individually-reportable test per data row
-- something unittest.TestCase + subTest cannot do (subTest rows are
sub-results within one reported test, not separate collected items).

This file intentionally does NOT inherit BaseTest/unittest.TestCase,
to show both approaches correctly, in the situation each is actually
suited for:
  - unittest.TestCase + subTest -> tests/test_search.py
  - plain pytest + parametrize   -> this file
"""

import csv
from pathlib import Path

import pytest

from config.config_loader import settings
from pages.search_page import SearchPage

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "test_data.csv"


def _load_csv_rows():
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


PRODUCT_NAMES = [row["product_name"] for row in _load_csv_rows()]


@pytest.mark.regression
@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_search_returns_results(driver, product_name):
    """Each product_name becomes its own collected+reported test item, e.g.
    test_search_returns_results[MacBook], test_search_returns_results[iPhone], ...
    """
    search_page = SearchPage(driver)
    search_page.open(settings.active.base_url)
    search_page.search_product(product_name)

    assert search_page.has_results(), f"Expected at least one search result for '{product_name}'."
