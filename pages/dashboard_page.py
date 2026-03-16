"""Dashboard page objects for Construct application."""
from playwright.sync_api import Page, expect

from .base_page import BasePage


class VendorDashboardPage(BasePage):
    """Page object for the vendor dashboard."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        # Use href so we find the nav link even if accessible name differs
        self._dashboard_link = page.locator("a[href*='/vendor/dashboard']").first
        self._rfp_link = page.locator("a[href*='/vendor/rfp']").first
        self._rfq_link = page.locator("a[href*='/vendor/rfq']").first

    def expect_vendor_dashboard_loaded(self, timeout: float = 20000):
        """Assert vendor dashboard is loaded."""
        expect(self.page).to_have_url(f"{self.base_url}/vendor/dashboard", timeout=timeout)
        expect(self._dashboard_link).to_be_visible(timeout=timeout)

    def is_on_vendor_dashboard(self) -> bool:
        """Check if current page is vendor dashboard."""
        return "/vendor/dashboard" in self.get_current_url()


class CustomerDashboardPage(BasePage):
    """Page object for the customer dashboard."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self._dashboard_link = page.get_by_role("link", name="Dashboard")

    def expect_customer_dashboard_loaded(self):
        """Assert customer dashboard is loaded."""
        expect(self.page).to_have_url(f"{self.base_url}/customer/dashboard")
        expect(self._dashboard_link).to_be_visible()

    def is_on_customer_dashboard(self) -> bool:
        """Check if current page is customer dashboard."""
        return "/customer/dashboard" in self.get_current_url()
