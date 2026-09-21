"""
search_page.py
---------------
Page Object for product search + add-to-cart from the search results /
product detail page.
"""

from pages.base_page import BasePage


class SearchPage(BasePage):
    locator_file = "search_locators.yaml"

    def search_product(self, product_name: str):
        self.type_text("search_input", product_name)
        self.click("search_button")
        return self

    def has_results(self) -> bool:
        return self.is_displayed("product_title_on_result", timeout=8)

    def open_product_by_name(self, product_name: str):
        self.click("product_link_by_name_template", name=product_name)
        return self

    def add_to_cart(self):
        self.click("add_to_cart_button")
        # OpenCart adds to cart via AJAX. Wait for the green success banner so a
        # following navigation (e.g. straight to the cart page) can't abort the request.
        self.find_element("success_alert", wait="visible")
        return self

    def get_success_message(self) -> str:
        return self.get_text("success_alert")
