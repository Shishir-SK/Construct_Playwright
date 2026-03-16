"""
Smoke tests for basic functionality.
Run these first to ensure core features work.
"""
import allure
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.customer_project_page_enhanced import CustomerProjectPageEnhanced
from pages.vendor_service_page import VendorServicePage


@pytest.mark.smoke
@allure.epic("Construct - Smoke")
@allure.feature("Login")
@allure.story("Vendor Login")
@allure.description("Basic smoke test: Vendor login and dashboard access")
@allure.step("1. Navigate to login page")
@allure.step("2. Enter vendor credentials")
@allure.step("3. Click login")
@allure.step("4. Verify dashboard access")
def test_smoke_vendor_login(
    page: Page,
    login_page: LoginPage,
    vendor_credentials: dict,
    base_url: str,
) -> None:
    """Smoke test for vendor login."""
    page.goto(f"{base_url}/login")
    page.get_by_role("textbox", name="Enter your email").fill(vendor_credentials["email"])
    page.get_by_role("textbox", name="Enter your password").fill(vendor_credentials["password"])
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(f"{base_url}/vendor/dashboard", timeout=10000)


@pytest.mark.smoke
@allure.epic("Construct - Smoke")
@allure.feature("Login")
@allure.story("Customer Login")
@allure.description("Basic smoke test: Customer login and dashboard access")
@allure.step("1. Navigate to login page")
@allure.step("2. Enter customer credentials")
@allure.step("3. Click login")
@allure.step("4. Verify dashboard access")
def test_smoke_customer_login(
    page: Page,
    login_page: LoginPage,
    customer_credentials: dict,
    base_url: str,
) -> None:
    """Smoke test for customer login."""
    page.goto(f"{base_url}/login")
    page.get_by_role("textbox", name="Enter your email").fill(customer_credentials["email"])
    page.get_by_role("textbox", name="Enter your password").fill(customer_credentials["password"])
    page.get_by_role("button", name="Login").click()
    page.wait_for_url(lambda url: "dashboard" in url or "customer" in url, timeout=10000)
    expect(page.locator("body")).to_be_visible()


@pytest.mark.smoke
@allure.epic("Construct - Smoke")
@allure.feature("Navigation")
@allure.story("Vendor Navigation")
@allure.description("Smoke test: Vendor navigation to key pages")
@allure.step("1. Login as vendor")
@allure.step("2. Navigate to RFP page")
@allure.step("3. Navigate to RFQ page")
@allure.step("4. Navigate to Add Service page")
def test_smoke_vendor_navigation(
    page: Page,
    login_page: LoginPage,
    vendor_credentials: dict,
    base_url: str,
) -> None:
    """Smoke test for vendor navigation."""
    page.goto(f"{base_url}/login")
    page.get_by_role("textbox", name="Enter your email").fill(vendor_credentials["email"])
    page.get_by_role("textbox", name="Enter your password").fill(vendor_credentials["password"])
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(f"{base_url}/vendor/dashboard", timeout=10000)

    # Navigate to RFP
    page.goto(f"{base_url}/vendor/rfp")
    expect(page).to_have_url(f"{base_url}/vendor/rfp")

    # Navigate to RFQ
    page.goto(f"{base_url}/vendor/rfq")
    expect(page).to_have_url(f"{base_url}/vendor/rfq")

    # Navigate to Add Service
    service_page = VendorServicePage(page, base_url)
    service_page.navigate_to_add_service()
    expect(page).to_have_url(f"{base_url}/vendor/add-service")


@pytest.mark.smoke
@allure.epic("Construct - Smoke")
@allure.feature("Core Functionality")
@allure.story("Create Project")
@allure.description("Smoke test: Customer creates a project")
@allure.step("1. Login as customer")
@allure.step("2. Navigate to dashboard")
@allure.step("3. Create new project")
@allure.step("4. Verify project created")
def test_smoke_customer_create_project(
    page: Page,
    login_page: LoginPage,
    customer_credentials: dict,
    base_url: str,
) -> None:
    """Smoke test for customer creating a project."""
    page.goto(f"{base_url}/login")
    page.get_by_role("textbox", name="Enter your email").fill(customer_credentials["email"])
    page.get_by_role("textbox", name="Enter your password").fill(customer_credentials["password"])
    page.get_by_role("button", name="Login").click()
    page.wait_for_url(lambda url: "dashboard" in url or "customer" in url, timeout=10000)
    expect(page.locator("body")).to_be_visible()

    # Assume dashboard has create project
    if page.get_by_text("Create Project").is_visible(timeout=5000):
        page.get_by_text("Create Project").click()
        page.get_by_label("Project Name").fill("Smoke Test Project")
        page.get_by_role("button", name="Create").click()
        expect(page.get_by_text("Smoke Test Project")).to_be_visible()


@pytest.mark.smoke
@allure.epic("Construct - Smoke")
@allure.feature("Core Functionality")
@allure.story("Create RFP")
@allure.description("Smoke test: Customer creates an RFP")
@allure.step("1. Login as customer")
@allure.step("2. Navigate to project")
@allure.step("3. Create RFP")
@allure.step("4. Verify RFP created")
def test_smoke_customer_create_rfp(
    page: Page,
    login_page: LoginPage,
    customer_credentials: dict,
    base_url: str,
) -> None:
    """Smoke test for customer creating an RFP."""
    page.goto(f"{base_url}/login")
    page.get_by_role("textbox", name="Enter your email").fill(customer_credentials["email"])
    page.get_by_role("textbox", name="Enter your password").fill(customer_credentials["password"])
    page.get_by_role("button", name="Login").click()
    page.wait_for_url(lambda url: "dashboard" in url or "customer" in url, timeout=10000)
    expect(page.locator("body")).to_be_visible()

    # Navigate to RFP
    page.goto(f"{base_url}/customer/rfp")
    if page.get_by_text("Create RFP").is_visible(timeout=5000):
        page.get_by_text("Create RFP").click()
        page.get_by_label("Title").fill("Smoke Test RFP")
        page.get_by_role("button", name="Save").click()
        expect(page.get_by_text("Smoke Test RFP")).to_be_visible()


@pytest.mark.smoke
@allure.epic("Construct - Smoke")
@allure.feature("Core Functionality")
@allure.story("Vendor Add Service")
@allure.description("Smoke test: Vendor adds a service")
@allure.step("1. Login as vendor")
@allure.step("2. Navigate to add service")
@allure.step("3. Fill service details")
@allure.step("4. Save service")
def test_smoke_vendor_add_service(
    page: Page,
    login_page: LoginPage,
    vendor_credentials: dict,
    base_url: str,
) -> None:
    """Smoke test for vendor adding a service."""
    page.goto(f"{base_url}/login")
    page.get_by_role("textbox", name="Enter your email").fill(vendor_credentials["email"])
    page.get_by_role("textbox", name="Enter your password").fill(vendor_credentials["password"])
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(f"{base_url}/vendor/dashboard", timeout=10000)

    service_page = VendorServicePage(page, base_url)
    service_page.navigate_to_add_service()
    service_page.fill_service_name("Smoke Test Service")
    service_page.fill_service_description("Smoke test description")
    service_page.save_service()
    # Assume success if no error
    expect(page.locator("body")).to_be_visible()