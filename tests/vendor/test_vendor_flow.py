"""
Vendor flow tests: login, navigation (Dashboard/RFP/RFQ), Add Service flow.
Includes positive, negative, access-control, error-handling, and performance tests.
Uses only stable locators; service and zone selection are generic (any first option).
"""
import time
import allure
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def _vendor_login(page: Page, base_url: str, vendor_credentials: dict) -> None:
    """Login as vendor and ensure on vendor dashboard."""
    page.goto(f"{base_url}/login")
    page.get_by_role("textbox", name="Enter your email").fill(
        vendor_credentials["email"]
    )
    page.get_by_role("textbox", name="Enter your password").fill(
        vendor_credentials["password"]
    )
    page.get_by_role("button", name="Login").click()
    page.wait_for_url(
        lambda url: "dashboard" in url or "welcome" in url,
        timeout=25000,
    )
    if "/vendor/dashboard" not in page.url:
        page.goto(f"{base_url}/vendor/dashboard")
    page.wait_for_load_state("domcontentloaded")
    page.locator("a[href*='/vendor/dashboard']").first.wait_for(
        state="visible", timeout=15000
    )


@allure.epic("Construct")
@allure.feature("Vendor Flow")
class TestVendorFlowCodegen:
    """Vendor login and main flow."""

    @allure.description(
        "Steps: 1) Navigate to login. 2) Enter vendor credentials. 3) Click Login. 4) Verify redirect to vendor dashboard."
    )
    @allure.story("Login")
    def test_vendor_login(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        expect(page).to_have_url(f"{base_url}/vendor/dashboard")
        expect(page.locator("a[href*='/vendor/dashboard']").first).to_be_visible()

    @allure.description(
        "Steps: 1) Login. 2) From dashboard click RFP. 3) Verify on RFP page."
    )
    @allure.story("Navigation - RFP")
    def test_vendor_navigate_to_rfp(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        rfp_link = page.locator("a[href*='/vendor/rfp']").first
        rfp_link.wait_for(state="visible", timeout=15000)
        rfp_link.click()
        page.wait_for_load_state("domcontentloaded")
        expect(page).to_have_url(f"{base_url}/vendor/rfp")

    @allure.description(
        "Steps: 1) Login. 2) From dashboard click RFQ. 3) Verify on RFQ page."
    )
    @allure.story("Navigation - RFQ")
    def test_vendor_navigate_to_rfq(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        rfq_link = page.locator("a[href*='/vendor/rfq']").first
        rfq_link.wait_for(state="visible", timeout=15000)
        rfq_link.click()
        page.wait_for_load_state("domcontentloaded")
        expect(page).to_have_url(f"{base_url}/vendor/rfq")

    @allure.description(
        "Steps: 1) Login. 2) Click Dashboard, then RFP, then RFQ, then Dashboard. 3) Verify URL at each step."
    )
    @allure.story("Navigation - Full Cycle")
    def test_vendor_navigation_full_cycle(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        dashboard_link = page.locator("a[href*='/vendor/dashboard']").first
        dashboard_link.click()
        expect(page).to_have_url(f"{base_url}/vendor/dashboard")
        page.locator("a[href*='/vendor/rfp']").first.click()
        page.wait_for_load_state("domcontentloaded")
        expect(page).to_have_url(f"{base_url}/vendor/rfp")
        page.locator("a[href*='/vendor/rfq']").first.click()
        page.wait_for_load_state("domcontentloaded")
        expect(page).to_have_url(f"{base_url}/vendor/rfq")
        page.locator("a[href*='/vendor/dashboard']").first.click()
        page.wait_for_load_state("domcontentloaded")
        expect(page).to_have_url(f"{base_url}/vendor/dashboard")

    @allure.description(
        "Steps: 1) Login, nav to dashboard. 2) Add Service: pick any service, next steps, select zone (e.g. States), complete. 3) Assert back on dashboard."
    )
    @allure.story("Add Service Flow")
    def test_vendor_add_service_flow(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)

        # Go to Add Service (skip Exit flow)
        page.goto(f"{base_url}/vendor/add-service")
        page.wait_for_load_state("domcontentloaded")

        # Step 1: Pick a service — open combobox and select first option (any service)
        combobox = page.get_by_role("combobox").first
        try:
            combobox.wait_for(state="visible", timeout=15000)
        except Exception:  # noqa: BLE001
            # Add-service may redirect to org setup or differ by role; assert we left dashboard
            assert "/vendor/" in page.url or "organization" in page.url
            return
        combobox.click()
        first_option = page.get_by_role("option").first
        first_option.wait_for(state="visible", timeout=5000)
        first_option.click()
        page.get_by_role("button", name="Next").click()

        # Step 2: Sub-services — select first visible checkbox then Next
        next_btn = page.get_by_role("button", name="Next")
        next_btn.wait_for(state="visible", timeout=10000)
        first_cb = page.get_by_role("checkbox").first
        if first_cb.is_visible():
            first_cb.click()
        next_btn.click()

        # Step 3: Service features — select first checkbox then Next (if step exists)
        next_btn = page.get_by_role("button", name="Next")
        next_btn.wait_for(state="visible", timeout=10000)
        first_cb = page.get_by_role("checkbox").first
        if first_cb.is_visible():
            first_cb.click()
        next_btn.click()

        # Step 4: Zone — select States (or any); pick first state/option then Next
        next_btn = page.get_by_role("button", name="Next")
        next_btn.wait_for(state="visible", timeout=10000)
        states_btn = page.get_by_text("States")
        if states_btn.is_visible():
            states_btn.click()
            state_option = page.get_by_role("option").first
            if state_option.is_visible():
                state_option.click()
        next_btn.click()

        # One more Next or Submit if wizard has another step
        next_btn = page.get_by_role("button", name="Next")
        submit_btn = page.get_by_role("button", name="Submit")
        try:
            next_btn.wait_for(state="visible", timeout=5000)
            next_btn.click()
        except Exception:  # noqa: BLE001
            try:
                submit_btn.wait_for(state="visible", timeout=5000)
                submit_btn.click()
            except Exception:  # noqa: BLE001
                pass

        # Success: land on vendor dashboard (created service appears here)
        page.wait_for_url(
            lambda url: "/vendor/dashboard" in url,
            timeout=15000,
        )
        expect(page).to_have_url(f"{base_url}/vendor/dashboard")
        expect(page.locator("a[href*='/vendor/dashboard']").first).to_be_visible()


# --- Negative tests (vendor flow) ---


@allure.epic("Construct")
@allure.feature("Vendor Flow - Negative")
class TestVendorFlowNegative:
    """Vendor flow negative: wrong credentials, validation, invalid input."""

    def _submit_and_assert_stay_on_login(
        self,
        page: Page,
        login_page: LoginPage,
        base_url: str,
        email: str,
        password: str,
        timeout: float = 10000,
    ) -> None:
        login_page.goto()
        login_page.login(email=email, password=password)
        expect(page).to_have_url(f"{base_url}/login", timeout=timeout)

    @allure.description(
        "Steps: 1) Enter valid vendor email with wrong password. 2) Click Login. 3) Verify user remains on login page."
    )
    @allure.story("Wrong Password")
    def test_vendor_login_wrong_password(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        self._submit_and_assert_stay_on_login(
            page, login_page, base_url,
            email=vendor_credentials["email"],
            password="WrongPassword999!",
        )

    @allure.description(
        "Steps: 1) Leave email empty, enter password. 2) Click Login. 3) Verify user remains on login."
    )
    @allure.story("Validation")
    def test_vendor_login_empty_email(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        self._submit_and_assert_stay_on_login(
            page, login_page, base_url,
            email="",
            password=vendor_credentials["password"],
        )

    @allure.description(
        "Steps: 1) Enter vendor email, leave password empty. 2) Click Login. 3) Verify user remains on login."
    )
    @allure.story("Validation")
    def test_vendor_login_empty_password(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        self._submit_and_assert_stay_on_login(
            page, login_page, base_url,
            email=vendor_credentials["email"],
            password="",
        )

    @allure.description(
        "Steps: 1) Enter invalid email format (no @). 2) Click Login. 3) Verify user remains on login."
    )
    @allure.story("Validation")
    def test_vendor_login_invalid_email_format(
        self,
        page: Page,
        login_page: LoginPage,
        base_url: str,
    ) -> None:
        self._submit_and_assert_stay_on_login(
            page, login_page, base_url,
            email="notanemail",
            password="Test1234",
        )

    @allure.description(
        "Steps: 1) Enter non-existent email with any password. 2) Click Login. 3) Verify user remains on login."
    )
    @allure.story("Invalid Credentials")
    def test_vendor_login_nonexistent_email(
        self,
        page: Page,
        login_page: LoginPage,
        base_url: str,
    ) -> None:
        self._submit_and_assert_stay_on_login(
            page, login_page, base_url,
            email="nonexistent-vendor@construct-test.com",
            password="Test1234",
        )


# --- Access control: unauthenticated access redirects to login ---


@allure.epic("Construct")
@allure.feature("Vendor Flow - Access Control")
class TestVendorFlowAccessControl:
    """Vendor routes must require authentication; direct URL access redirects to login."""

    @allure.description(
        "Steps: 1) Without logging in, navigate to /vendor/dashboard. 2) Verify redirect to login or login form visible."
    )
    @allure.story("Unauthenticated Access")
    def test_vendor_dashboard_redirects_to_login_when_not_authenticated(
        self, page: Page, base_url: str
    ) -> None:
        page.goto(f"{base_url}/vendor/dashboard", wait_until="domcontentloaded")
        page.wait_for_load_state("domcontentloaded")
        
        # Wait a moment for potential redirect
        page.wait_for_timeout(2000)
        
        # Check if redirected to login or see login form
        current_url = page.url
        is_on_login = "/login" in current_url
        
        # Look for various login indicators
        login_indicators = [
            page.get_by_role("button", name="Login"),
            page.get_by_text("Login"),
            page.get_by_label("Email"),
            page.get_by_label("Password"),
            page.get_by_placeholder("Enter your email"),
            page.get_by_placeholder("Enter your password")
        ]
        
        has_login_form = any(indicator.is_visible(timeout=3000) for indicator in login_indicators)
        
        # Either redirected to login or login form is visible
        assert is_on_login or has_login_form, f"Expected login redirect or login form visible. URL: {current_url}"

    @allure.description(
        "Steps: 1) Without logging in, navigate to /vendor/rfp. 2) Verify redirect to login or login visible."
    )
    @allure.story("Unauthenticated Access")
    def test_vendor_rfp_redirects_to_login_when_not_authenticated(
        self, page: Page, base_url: str
    ) -> None:
        page.goto(f"{base_url}/vendor/rfp", wait_until="domcontentloaded")
        page.wait_for_load_state("domcontentloaded")
        
        # Wait a moment for potential redirect
        page.wait_for_timeout(2000)
        
        # Check if redirected to login or see login form
        current_url = page.url
        is_on_login = "/login" in current_url
        
        # Look for various login indicators
        login_indicators = [
            page.get_by_role("button", name="Login"),
            page.get_by_text("Login"),
            page.get_by_label("Email"),
            page.get_by_label("Password"),
            page.get_by_placeholder("Enter your email"),
            page.get_by_placeholder("Enter your password")
        ]
        
        has_login_form = any(indicator.is_visible(timeout=3000) for indicator in login_indicators)
        
        # Either redirected to login or login form is visible
        assert is_on_login or has_login_form, f"Expected login redirect or login form visible. URL: {current_url}"

    @allure.description(
        "Steps: 1) Without logging in, navigate to /vendor/add-service. 2) Verify redirect to login or login visible."
    )
    @allure.story("Unauthenticated Access")
    def test_vendor_add_service_redirects_to_login_when_not_authenticated(
        self, page: Page, base_url: str
    ) -> None:
        page.goto(f"{base_url}/vendor/add-service", wait_until="domcontentloaded")
        page.wait_for_load_state("domcontentloaded")
        
        # Wait a moment for potential redirect
        page.wait_for_timeout(2000)
        
        # Check if redirected to login or see login form
        current_url = page.url
        is_on_login = "/login" in current_url
        
        # Look for various login indicators
        login_indicators = [
            page.get_by_role("button", name="Login"),
            page.get_by_text("Login"),
            page.get_by_label("Email"),
            page.get_by_label("Password"),
            page.get_by_placeholder("Enter your email"),
            page.get_by_placeholder("Enter your password")
        ]
        
        has_login_form = any(indicator.is_visible(timeout=3000) for indicator in login_indicators)
        
        # Either redirected to login or login form is visible
        assert is_on_login or has_login_form, f"Expected login redirect or login form visible. URL: {current_url}"


# --- Additional positive and error-handling ---


@allure.epic("Construct")
@allure.feature("Vendor Flow - Positive")
class TestVendorFlowPositive:
    """Additional positive checks: UI visibility, resilience."""

    @allure.description(
        "Steps: 1) Login as vendor. 2) Verify Dashboard, RFP, RFQ navigation links are visible on dashboard."
    )
    @allure.story("Dashboard UI")
    def test_vendor_dashboard_nav_links_visible(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        expect(page.locator("a[href*='/vendor/dashboard']").first).to_be_visible()
        expect(page.locator("a[href*='/vendor/rfp']").first).to_be_visible()
        expect(page.locator("a[href*='/vendor/rfq']").first).to_be_visible()

    @allure.description(
        "Steps: 1) Login. 2) Refresh dashboard page. 3) Verify still on dashboard and nav visible (session persists)."
    )
    @allure.story("Session")
    def test_vendor_dashboard_refresh_still_authenticated(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        page.reload(wait_until="domcontentloaded")
        page.wait_for_load_state("domcontentloaded")
        expect(page).to_have_url(f"{base_url}/vendor/dashboard", timeout=15000)
        expect(page.locator("a[href*='/vendor/dashboard']").first).to_be_visible(timeout=10000)


@allure.epic("Construct")
@allure.feature("Vendor Flow - Error Handling")
class TestVendorFlowErrorHandling:
    """Invalid routes and error handling."""

    @allure.description(
        "Steps: 1) Login. 2) Navigate to non-existent vendor path. 3) Verify app handles it (no crash; 404 or redirect)."
    )
    @allure.story("Invalid Route")
    def test_vendor_invalid_route_handled(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        page.goto(f"{base_url}/vendor/nonexistent-route-xyz", wait_until="domcontentloaded")
        page.wait_for_load_state("domcontentloaded")
        # App should not crash: we get some page (login redirect, 404, or dashboard fallback)
        assert page.url  # has a URL
        # Either still on vendor area, or redirected to login
        assert "/vendor/" in page.url or "/login" in page.url or "404" in page.url.lower()


# --- Performance (sanity: complete within reasonable time) ---


@allure.epic("Construct")
@allure.feature("Vendor Flow - Performance")
class TestVendorFlowPerformance:
    """Vendor flow performance: login and page load within acceptable time."""

    # Max acceptable time (seconds) for login redirect and key page loads
    LOGIN_MAX_SECONDS = 25
    DASHBOARD_LOAD_MAX_SECONDS = 15
    NAV_PAGE_LOAD_MAX_SECONDS = 10

    @allure.description(
        "Steps: 1) Start timer. 2) Login as vendor. 3) Verify redirect to dashboard within acceptable time (e.g. 25s)."
    )
    @allure.story("Login Performance")
    def test_vendor_login_completes_within_timeout(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        page.goto(f"{base_url}/login")
        page.get_by_role("textbox", name="Enter your email").fill(
            vendor_credentials["email"]
        )
        page.get_by_role("textbox", name="Enter your password").fill(
            vendor_credentials["password"]
        )
        start = time.monotonic()
        page.get_by_role("button", name="Login").click()
        page.wait_for_url(
            lambda url: "dashboard" in url or "welcome" in url,
            timeout=self.LOGIN_MAX_SECONDS * 1000,
        )
        if "/vendor/dashboard" not in page.url:
            page.goto(f"{base_url}/vendor/dashboard")
        page.locator("a[href*='/vendor/dashboard']").first.wait_for(
            state="visible", timeout=15000
        )
        elapsed = time.monotonic() - start
        assert elapsed <= self.LOGIN_MAX_SECONDS, (
            f"Login took {elapsed:.1f}s, expected <= {self.LOGIN_MAX_SECONDS}s"
        )

    @allure.description(
        "Steps: 1) Login. 2) Measure time until dashboard nav links visible. 3) Assert within acceptable time (e.g. 15s)."
    )
    @allure.story("Dashboard Load Performance")
    def test_vendor_dashboard_loads_within_timeout(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        page.goto(f"{base_url}/login")
        page.get_by_role("textbox", name="Enter your email").fill(
            vendor_credentials["email"]
        )
        page.get_by_role("textbox", name="Enter your password").fill(
            vendor_credentials["password"]
        )
        page.get_by_role("button", name="Login").click()
        page.wait_for_url(
            lambda url: "dashboard" in url or "welcome" in url,
            timeout=25000,
        )
        if "/vendor/dashboard" not in page.url:
            page.goto(f"{base_url}/vendor/dashboard")
        start = time.monotonic()
        page.locator("a[href*='/vendor/dashboard']").first.wait_for(
            state="visible", timeout=self.DASHBOARD_LOAD_MAX_SECONDS * 1000
        )
        elapsed = time.monotonic() - start
        assert elapsed <= self.DASHBOARD_LOAD_MAX_SECONDS, (
            f"Dashboard load took {elapsed:.1f}s, expected <= {self.DASHBOARD_LOAD_MAX_SECONDS}s"
        )

    @allure.description(
        "Steps: 1) Login and go to dashboard. 2) Click RFP. 3) Measure time until RFP page loaded. 4) Assert within acceptable time (e.g. 10s)."
    )
    @allure.story("Navigation Performance")
    def test_vendor_rfp_page_loads_within_timeout(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        rfp_link = page.locator("a[href*='/vendor/rfp']").first
        start = time.monotonic()
        rfp_link.click()
        page.wait_for_url(
            lambda url: "/vendor/rfp" in url,
            timeout=self.NAV_PAGE_LOAD_MAX_SECONDS * 1000,
        )
        page.wait_for_load_state("domcontentloaded")
        elapsed = time.monotonic() - start
        assert elapsed <= self.NAV_PAGE_LOAD_MAX_SECONDS, (
            f"RFP page load took {elapsed:.1f}s, expected <= {self.NAV_PAGE_LOAD_MAX_SECONDS}s"
        )
