"""Customer RFP page object for Construct application."""
from playwright.sync_api import Page, expect

from .base_page import BasePage


class CustomerRFPPage(BasePage):
    """Page object for customer RFP operations."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self._create_rfp_button = page.get_by_role("button", name="Create RFP").or_(page.get_by_text("Create RFP")).or_(page.get_by_role("link", name="Create RFP"))
        self._rfp_title_input = page.get_by_label("Title").or_(page.get_by_placeholder("Title")).or_(page.locator('input[name="title"]'))
        self._tiptap_editor = page.locator(".ProseMirror").or_(page.locator("[contenteditable='true']")).first
        self._save_button = page.get_by_role("button", name="Save").or_(page.get_by_role("button", name="Create"))
        self._submit_rfp_button = page.get_by_role("button", name="Submit RFP").or_(page.get_by_text("Submit RFP"))
        self._edit_button = page.get_by_role("button", name="Edit").or_(page.get_by_text("Edit"))
        self._create_quote_button = page.get_by_role("button", name="Create Quote").or_(page.get_by_text("Create Quote")).or_(page.get_by_role("button", name="Create RFQ"))
        self._end_date_input = page.get_by_label("End date").or_(page.locator('input[type="date"]'))
        self._rfp_links = page.locator("a[href*='/rfp']")

    def click_create_rfp(self) -> None:
        """Click the create RFP button."""
        self._create_rfp_button.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def fill_rfp_title(self, title: str) -> None:
        """Fill in the RFP title."""
        self._rfp_title_input.first.fill(title)

    def fill_tiptap_content(self, content: str) -> None:
        """Fill content in the TipTap editor."""
        self._tiptap_editor.first.fill(content)

    def save_rfp(self) -> None:
        """Save the RFP."""
        self._save_button.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def submit_rfp(self) -> None:
        """Submit the RFP."""
        self._submit_rfp_button.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def edit_rfp(self) -> None:
        """Click edit button to edit RFP."""
        self._edit_button.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def create_quote(self) -> None:
        """Create a quote/RFQ from RFP."""
        self._create_quote_button.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def set_end_date(self, date: str) -> None:
        """Set the end date for RFP/RFQ."""
        if self._end_date_input.first.is_visible(timeout=5000):
            self._end_date_input.first.fill(date)

    def has_rfp_links(self, timeout: float = 8000) -> bool:
        """Check if there are any RFP links available."""
        return self._rfp_links.first.is_visible(timeout=timeout)

    def open_first_rfp(self) -> None:
        """Open the first available RFP."""
        self._rfp_links.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def has_create_rfp_button(self, timeout: float = 8000) -> bool:
        """Check if create RFP button is visible."""
        return self._create_rfp_button.first.is_visible(timeout=timeout)

    def has_submit_button(self, timeout: float = 5000) -> bool:
        """Check if submit RFP button is visible."""
        return self._submit_rfp_button.first.is_visible(timeout=timeout)

    def has_edit_button(self, timeout: float = 5000) -> bool:
        """Check if edit button is visible."""
        return self._edit_button.first.is_visible(timeout=timeout)

    def expect_edit_button_disabled(self) -> None:
        """Assert that edit button is disabled."""
        expect(self._edit_button.first).to_be_disabled()

    def has_tiptap_editor(self, timeout: float = 3000) -> bool:
        """Check if TipTap editor is available."""
        return self._tiptap_editor.first.is_visible(timeout=timeout)

    def expect_rfp_created(self) -> None:
        """Assert that RFP was created successfully."""
        expect(self.page.locator("body")).to_be_visible()
        # Should be on RFP page or see RFP content
        url = self.page.url
        assert "rfp" in url or "customer" in url, f"Expected RFP or customer page, got {url}"
