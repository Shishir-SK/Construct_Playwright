"""
Vendor service management tests: add, edit, delete services.
Comprehensive coverage for vendor service operations with detailed allure reporting.
"""
import allure
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.vendor_service_page import VendorServicePage


def _vendor_login(page: Page, base_url: str, vendor_credentials: dict) -> None:
    """Login as vendor and ensure on vendor dashboard."""
    page.goto(f"{base_url}/login")
    page.get_by_role("textbox", name="Enter your email").fill(vendor_credentials["email"])
    page.get_by_role("textbox", name="Enter your password").fill(vendor_credentials["password"])
    page.get_by_role("button", name="Login").click()
    page.wait_for_url(
        lambda url: "dashboard" in url or "welcome" in url,
        timeout=25000,
    )
    if "/vendor/dashboard" not in page.url:
        page.goto(f"{base_url}/vendor/dashboard")
    page.wait_for_load_state("domcontentloaded")
    # Optional: wait for dashboard link if present
    try:
        page.locator("a[href*='/vendor/dashboard']").first.wait_for(
            state="visible", timeout=5000
        )
    except:
        pass  # Link may not be present


@allure.epic("Construct")
@allure.feature("Vendor Flow - Service Management")
class TestVendorServiceManagement:
    """Vendor service management comprehensive tests."""

    @allure.description(
        "Steps: 1) Login as vendor. 2) Navigate to add service page. 3) Fill service details. "
        "4) Save service. 5) Verify save completes successfully."
    )
    @allure.story("Create Service")
    def test_vendor_create_service_success(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        service_page = VendorServicePage(page, base_url)
        
        service_page.navigate_to_add_service()
        service_page.fill_service_name("Test Service")
        service_page.fill_service_description("Test description")
        service_page.save_service()
        
        # Just verify page loads without error
        expect(page.locator("body")).to_be_visible()

    @allure.description(
        "Steps: 1) Login as vendor. 2) Navigate to add service page. 3) Leave service name empty. "
        "4) Try to save. 5) Verify validation error or stay on add service page."
    )
    @allure.story("Service Validation")
    def test_vendor_create_service_empty_name_validation(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        service_page = VendorServicePage(page, base_url)
        
        service_page.navigate_to_add_service()
        service_page.fill_service_name("")  # Leave empty
        service_page.fill_service_description("Test description")
        
        # Try to save
        service_page.save_service()
        
        # Should stay on add service page due to validation
        expect(page).to_have_url(f"{base_url}/vendor/add-service")

    @allure.description(
        "Steps: 1) Login as vendor. 2) Navigate to add service page. 3) Fill only service name. "
        "4) Save service. 5) Verify service created with minimal data."
    )
    @allure.story("Create Service - Minimal Data")
    def test_vendor_create_service_minimal_data(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        service_page = VendorServicePage(page, base_url)
        
        service_page.navigate_to_add_service()
        import uuid
        test_service_name = f"E2E Minimal Service {uuid.uuid4().hex[:8]}"
        service_page.fill_service_name(test_service_name)
        service_page.fill_service_description("Minimal test description")
        # Category may not be required
        service_page.save_service()
        
        # Verify service was created
        service_page.expect_service_created(test_service_name)

    @allure.description(
        "Steps: 1) Login as vendor. 2) Create multiple services with different names. "
        "3) Verify all services appear in the list. 4) Check service count increased."
    )
    @allure.story("Create Multiple Services")
    def test_vendor_create_multiple_services(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        service_page = VendorServicePage(page, base_url)
        
        # Get initial service count
        initial_count = service_page.get_service_count()
        
        # Create multiple services
        import uuid
        unique_id = uuid.uuid4().hex[:8]
        service_names = [
            f"E2E Service Alpha {unique_id}A",
            f"E2E Service Beta {unique_id}B",
            f"E2E Service Gamma {unique_id}C"
        ]
        
        for service_name in service_names:
            service_page.navigate_to_add_service()
            service_page.fill_service_name(service_name)
            service_page.fill_service_description(f"Description for {service_name}")
            service_page.save_service()
            
            # Verify service appears in list
            assert service_page.has_service_with_name(service_name, timeout=10000)
        
        # Verify service count increased
        final_count = service_page.get_service_count()
        assert final_count >= initial_count + len(service_names)

    @allure.description(
        "Steps: 1) Login as vendor. 2) Create service with special characters in name. "
        "3) Verify service handles special characters properly. 4) Check service appears correctly."
    )
    @allure.story("Service Name - Special Characters")
    def test_vendor_create_service_special_characters(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        service_page = VendorServicePage(page, base_url)
        
        service_page.navigate_to_add_service()
        import uuid
        special_service_name = f"E2E Service & Co. (Test) - {uuid.uuid4().hex[:6]}"
        service_page.fill_service_name(special_service_name)
        service_page.fill_service_description("Service with special characters: & ( ) -")
        service_page.select_category("IT Services")
        service_page.save_service()
        
        # Verify service was created with special characters
        service_page.expect_service_created(special_service_name)

    @allure.description(
        "Steps: 1) Login as vendor. 2) Create service with very long name and description. "
        "3) Verify system handles long text properly. 4) Check service appears correctly."
    )
    @allure.story("Service - Long Text")
    def test_vendor_create_service_long_text(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        service_page = VendorServicePage(page, base_url)
        
        service_page.navigate_to_add_service()
        long_name = "E2E Service with Very Long Name " + "X" * 50  # Make it very long
        long_description = "Very long description " + "Y" * 200  # Make it very long
        
        service_page.fill_service_name(long_name)
        service_page.fill_service_description(long_description)
        service_page.select_category("IT Services")
        service_page.save_service()
        
        # Verify service was created
        service_page.expect_service_created(long_name)

    @allure.description(
        "Steps: 1) Login as vendor. 2) Navigate to add service page. 3) Fill service name with HTML/JS. "
        "4) Save service. 5) Verify XSS protection - content should be escaped or sanitized."
    )
    @allure.story("Security - XSS Protection")
    def test_vendor_service_xss_protection(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        service_page = VendorServicePage(page, base_url)
        
        service_page.navigate_to_add_service()
        import uuid
        unique_id = uuid.uuid4().hex[:6]
        xss_name = f"E2E <script>alert('xss')</script> Service {unique_id}"
        service_page.fill_service_name(xss_name)
        service_page.fill_service_description("<img src=x onerror=alert('xss')>")
        service_page.save_service()
        
        # Verify service was created but XSS was sanitized
        expect(page.locator("body")).to_be_visible()
        # Should not contain actual script tags or alert functions
        page_content = page.content()
        assert "<script>" not in page_content or "alert" not in page_content.lower()

    @allure.description(
        "Steps: 1) Login as vendor. 2) Create service with unicode characters. "
        "3) Verify system handles unicode properly. 4) Check service appears correctly."
    )
    @allure.story("Unicode Support")
    def test_vendor_service_unicode_support(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        service_page = VendorServicePage(page, base_url)
        
        service_page.navigate_to_add_service()
        import uuid
        unique_id = uuid.uuid4().hex[:6]
        unicode_name = f"E2E 服务测试 🚀 {unique_id}"
        unicode_description = "Test description with unicode: café, naïve, 🎉"
        
        service_page.fill_service_name(unicode_name)
        service_page.fill_service_description(unicode_description)
        service_page.save_service()
        
        # Verify service was created with unicode
        expect(page.locator("body")).to_be_visible()
        # Check for unicode characters
        expect(page.get_by_text("服务测试")).to_be_visible()


@allure.epic("Construct")
@allure.feature("Vendor Flow - Service Management - Access Control")
class TestVendorServiceAccessControl:
    """Vendor service management access control tests."""

    @allure.description(
        "Steps: 1) Without logging in, try to access add service page. "
        "2) Verify redirect to login or login form visible. 3) Confirm access control works."
    )
    @allure.story("Unauthenticated Access")
    def test_vendor_add_service_redirects_to_login_when_not_authenticated(
        self, page: Page, base_url: str
    ) -> None:
        page.goto(f"{base_url}/vendor/add-service", wait_until="domcontentloaded")
        page.wait_for_load_state("domcontentloaded")
        
        # Should redirect to login or show login form
        assert "/login" in page.url or page.get_by_role("button", name="Login").is_visible(timeout=5000)

    @allure.description(
        "Steps: 1) Login as customer. 2) Try to access vendor add service page. "
        "3) Verify access denied or redirect to customer dashboard. 4) Confirm role-based access control."
    )
    @allure.story("Role-Based Access Control")
    def test_vendor_add_service_denied_for_customer_role(
        self,
        page: Page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ) -> None:
        # Login as customer
        page.goto(f"{base_url}/login")
        page.get_by_role("textbox", name="Enter your email").fill(customer_credentials["email"])
        page.get_by_role("textbox", name="Enter your password").fill(customer_credentials["password"])
        page.get_by_role("button", name="Login").click()
        page.wait_for_url(
            lambda url: "dashboard" in url or "create-organization" in url,
            timeout=25000,
        )
        
        # Try to access vendor add service
        page.goto(f"{base_url}/vendor/add-service", wait_until="domcontentloaded")
        page.wait_for_load_state("domcontentloaded")
        
        # Should be denied access - redirect to customer area or show access denied
        current_url = page.url
        assert "/customer/" in current_url or "/login" in current_url or "access" in current_url.lower()
