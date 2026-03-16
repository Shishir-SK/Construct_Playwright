"""Vendor RFQ page object for Construct application."""
from playwright.sync_api import Page, expect

from .base_page import BasePage


class VendorRFQPage(BasePage):
    """Page object for vendor RFQ/Quote operations."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self._rfq_list_link = page.locator("a[href*='/vendor/rfq']").first
        self._rfq_row_links = page.locator("a[href*='/rfq']")
        self._submit_quote_button = page.get_by_role("button", name="Submit Quote").or_(page.get_by_role("button", name="Submit")).or_(page.get_by_text("Submit quote"))
        self._quote_input = page.get_by_placeholder("Quote amount").or_(page.get_by_label("Quote")).or_(page.locator("[contenteditable='true']").first)

    def navigate_to_rfq_list(self) -> None:
        """Navigate to vendor RFQ list page."""
        self._rfq_list_link.click()
        self.page.wait_for_load_state("domcontentloaded")

    def get_first_rfq_link(self):
        """Get the first available RFQ link."""
        return self._rfq_row_links.first

    def has_rfq_links(self, timeout: float = 10000) -> bool:
        """Check if there are any RFQ links available."""
        return self._rfq_row_links.first.is_visible(timeout=timeout)

    def open_first_rfq(self) -> None:
        """Open the first available RFQ."""
        self.get_first_rfq_link().click()
        self.page.wait_for_load_state("domcontentloaded")

    def has_submit_quote_button(self, timeout: float = 5000) -> bool:
        """Check if submit quote button is visible."""
        return self._submit_quote_button.first.is_visible(timeout=timeout)

    def has_quote_input(self, timeout: float = 3000) -> bool:
        """Check if quote input field is available."""
        return self._quote_input.first.is_visible(timeout=timeout)

    def fill_quote_amount(self, amount: str) -> None:
        """Fill in the quote amount."""
        self._quote_input.first.fill(amount)

    def submit_quote(self) -> None:
        """Submit the quote."""
        self._submit_quote_button.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def expect_submit_button_disabled(self) -> None:
        """Assert that submit button is disabled."""
        expect(self._submit_quote_button.first).to_be_disabled()

    def expect_submit_button_hidden(self) -> None:
        """Assert that submit button is hidden."""
        expect(self._submit_quote_button.first).to_be_hidden()
