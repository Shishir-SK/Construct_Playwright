"""Vendor RFP page object for Construct application."""
from playwright.sync_api import Page, expect

from .base_page import BasePage


class VendorRFPPage(BasePage):
    """Page object for vendor RFP operations."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self._rfp_list_link = page.locator("a[href*='/vendor/rfp']").first
        self._rfp_row_links = page.locator("a[href*='/rfp']")
        self._edit_button = page.get_by_role("button", name="Edit").or_(page.get_by_text("Edit"))
        self._comment_input = page.get_by_placeholder("Add a comment").or_(page.get_by_role("textbox", name="Comment"))
        self._post_comment_button = page.get_by_role("button", name="Post").or_(page.get_by_text("Post comment")).or_(page.get_by_role("button", name="Comment"))

    def navigate_to_rfp_list(self) -> None:
        """Navigate to vendor RFP list page."""
        self._rfp_list_link.click()
        self.page.wait_for_load_state("domcontentloaded")

    def get_first_rfp_link(self):
        """Get the first available RFP link."""
        return self._rfp_row_links.first

    def has_rfp_links(self, timeout: float = 10000) -> bool:
        """Check if there are any RFP links available."""
        return self._rfp_row_links.first.is_visible(timeout=timeout)

    def open_first_rfp(self) -> None:
        """Open the first available RFP."""
        self.get_first_rfp_link().click()
        self.page.wait_for_load_state("domcontentloaded")

    def is_edit_button_visible(self, timeout: float = 5000) -> bool:
        """Check if edit button is visible."""
        return self._edit_button.first.is_visible(timeout=timeout)

    def is_edit_button_enabled(self) -> bool:
        """Check if edit button is enabled."""
        return self._edit_button.first.is_enabled()

    def expect_edit_button_disabled(self) -> None:
        """Assert that edit button is disabled."""
        expect(self._edit_button.first).to_be_disabled()

    def expect_edit_button_hidden(self) -> None:
        """Assert that edit button is hidden."""
        expect(self._edit_button.first).to_be_hidden()

    def add_comment(self, comment_text: str) -> None:
        """Add a comment to the RFP."""
        self._comment_input.first.fill(comment_text)
        self._post_comment_button.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def verify_comment_visible(self, comment_text: str, timeout: float = 5000) -> None:
        """Verify that a comment is visible."""
        expect(self.page.get_by_text(comment_text)).to_be_visible(timeout=timeout)

    def has_comment_input(self, timeout: float = 5000) -> bool:
        """Check if comment input is available."""
        return self._comment_input.first.is_visible(timeout=timeout)
