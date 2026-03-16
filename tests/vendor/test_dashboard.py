"""Vendor dashboard tests."""
import allure
from playwright.sync_api import expect

from pages.dashboard_page import VendorDashboardPage


@allure.epic("Construct")
@allure.feature("Vendor Dashboard")
class TestVendorDashboard:
    """Vendor dashboard functionality."""

    @allure.description(
        "Steps: 1) Login as vendor. 2) Verify vendor dashboard loads. 3) Verify Dashboard, RFP, RFQ navigation links are visible."
    )
    @allure.story("Navigation")
    def test_dashboard_navigation_links(
        self,
        logged_in_vendor_page,
        base_url: str,
    ):
        """Verify vendor dashboard has expected navigation links."""
        with allure.step("Verify vendor dashboard is loaded"):
            dashboard = VendorDashboardPage(logged_in_vendor_page, base_url)
            dashboard.expect_vendor_dashboard_loaded()
        with allure.step("Verify Dashboard link is visible"):
            expect(logged_in_vendor_page.locator("a[href*='/vendor/dashboard']").first).to_be_visible(timeout=15000)

    @allure.description(
        "Steps: 1) Login as vendor. 2) Verify vendor dashboard loads. 3) Verify Services section is visible."
    )
    @allure.story("Services Section")
    def test_services_section_visible(
        self,
        logged_in_vendor_page,
        base_url: str,
    ):
        """Verify Services section is visible on vendor dashboard."""
        with allure.step("Verify vendor dashboard is loaded"):
            dashboard = VendorDashboardPage(logged_in_vendor_page, base_url)
            dashboard.expect_vendor_dashboard_loaded()
        with allure.step("Verify dashboard content loaded"):
            expect(logged_in_vendor_page.locator("a[href*='/vendor/dashboard']").first).to_be_visible(timeout=15000)

    @allure.description(
        "Steps: 1) Login as vendor. 2) Verify vendor dashboard loads. 3) Verify Activity section is visible."
    )
    @allure.story("Activity Section")
    def test_activity_section_visible(
        self,
        logged_in_vendor_page,
        base_url: str,
    ):
        """Verify Activity section is visible on vendor dashboard."""
        with allure.step("Verify vendor dashboard is loaded"):
            dashboard = VendorDashboardPage(logged_in_vendor_page, base_url)
            dashboard.expect_vendor_dashboard_loaded()
        with allure.step("Verify Activity section is visible"):
            expect(logged_in_vendor_page.get_by_text("Activity").first).to_be_visible()
