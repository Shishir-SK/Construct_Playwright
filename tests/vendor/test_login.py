"""Vendor login flow tests."""
import allure
from playwright.sync_api import expect

from pages.dashboard_page import VendorDashboardPage
from pages.login_page import LoginPage


@allure.epic("Construct")
@allure.feature("Login - Vendor Flow")
class TestVendorLoginFlow:
    """Vendor login: success and vendor-specific negative cases."""

    @allure.description(
        "Steps: 1) Navigate to login page. 2) Enter vendor email and password. 3) Click Login. 4) Verify redirect to vendor dashboard."
    )
    @allure.story("Vendor Login Success")
    def test_vendor_login_success(
        self,
        page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ):
        """Verify vendor can login and reach vendor dashboard."""
        with allure.step("Navigate to login page"):
            login_page.goto()
        with allure.step("Enter vendor credentials and click Login"):
            login_page.login(
                email=vendor_credentials["email"],
                password=vendor_credentials["password"],
            )
        with allure.step("Wait for login to complete and redirect"):
            login_page.wait_for_login_complete()
        with allure.step("Navigate to vendor dashboard if on welcome page"):
            if "/vendor/dashboard" not in page.url:
                page.goto(f"{base_url}/vendor/dashboard")
        with allure.step("Wait for dashboard page to stabilize"):
            page.wait_for_load_state("domcontentloaded")
            page.locator("a[href*='/vendor/dashboard']").first.wait_for(state="visible", timeout=15000)
        with allure.step("Verify vendor dashboard is loaded"):
            vendor_dashboard = VendorDashboardPage(page, base_url)
            vendor_dashboard.expect_vendor_dashboard_loaded()

    @allure.description(
        "Steps: 1) Navigate to login. 2) Enter valid vendor email with wrong password. 3) Click Login. 4) Verify user remains on login page."
    )
    @allure.story("Vendor - Wrong Password")
    def test_vendor_wrong_password(
        self, login_page: LoginPage, vendor_credentials: dict
    ):
        """Vendor email with wrong password should not login."""
        login_page.goto()
        login_page.login(
            email=vendor_credentials["email"],
            password="WrongPassword999!",
        )
        expect(login_page.page).to_have_url(
            f"{login_page.base_url}/login",
            timeout=8000,
        )
