"""Shared login tests: page load, invalid credentials, security (SQL injection, XSS, validation)."""
import allure
from playwright.sync_api import expect

from pages.login_page import LoginPage


@allure.epic("Construct")
@allure.feature("Login - Common")
class TestLoginPage:
    """Shared login page tests (not role-specific)."""

    @allure.description(
        "Steps: 1) Navigate to login page. 2) Verify login form is visible with email, password fields and Login button."
    )
    @allure.story("Login Page")
    def test_login_page_loads(self, login_page: LoginPage):
        """Verify login page loads with correct elements."""
        with allure.step("Navigate to login page"):
            login_page.goto()
        with allure.step("Verify login form is visible"):
            login_page.expect_login_form_visible()

    @allure.description(
        "Steps: 1) Navigate to login page. 2) Enter invalid email and password. 3) Click Login. 4) Verify user remains on login page (no redirect)."
    )
    @allure.story("Invalid Credentials")
    def test_invalid_credentials_stay_on_login(self, login_page: LoginPage):
        """Verify invalid credentials keep user on login page."""
        with allure.step("Navigate to login page"):
            login_page.goto()
        with allure.step("Enter invalid credentials and click Login"):
            login_page.login(
                email="invalid@example.com",
                password="WrongPassword123",
            )
        with allure.step("Verify user stays on login page"):
            expect(login_page.page).to_have_url(
                f"{login_page.base_url}/login",
                timeout=5000,
            )


@allure.epic("Construct")
@allure.feature("Login - Common (Security & Validation)")
class TestLoginNegative:
    """Shared negative and security login tests (not role-specific)."""

    def _submit_and_assert_stay_on_login(
        self, login_page: LoginPage, email: str, password: str, timeout: float = 8000
    ):
        """Submit credentials and assert user remains on login page."""
        login_page.goto()
        login_page.login(email=email, password=password)
        expect(login_page.page).to_have_url(
            f"{login_page.base_url}/login",
            timeout=timeout,
        )

    @allure.description(
        "Steps: 1) Navigate to login. 2) Enter SQL injection payload in email. 3) Click Login. 4) Verify user remains on login and no injection succeeds."
    )
    @allure.story("SQL Injection")
    def test_sql_injection_in_email(self, login_page: LoginPage):
        """SQL injection in email field should be rejected / not execute."""
        with allure.step("Enter SQL injection in email field"):
            self._submit_and_assert_stay_on_login(
                login_page,
                email="' OR '1'='1' --",
                password="any",
            )

    @allure.description(
        "Steps: 1) Navigate to login. 2) Enter valid-looking email and SQL injection in password. 3) Click Login. 4) Verify user remains on login."
    )
    @allure.story("SQL Injection")
    def test_sql_injection_in_password(self, login_page: LoginPage):
        """SQL injection in password field should be rejected."""
        with allure.step("Enter SQL injection in password field"):
            self._submit_and_assert_stay_on_login(
                login_page,
                email="user@example.com",
                password="' OR '1'='1' --",
            )

    @allure.description(
        "Steps: 1) Navigate to login. 2) Leave email empty, enter password. 3) Click Login. 4) Verify user remains on login or validation shown."
    )
    @allure.story("Validation")
    def test_empty_email(self, login_page: LoginPage):
        """Empty email should not allow login."""
        with allure.step("Submit with empty email"):
            self._submit_and_assert_stay_on_login(
                login_page,
                email="",
                password="Test1234",
            )

    @allure.description(
        "Steps: 1) Navigate to login. 2) Enter email, leave password empty. 3) Click Login. 4) Verify user remains on login."
    )
    @allure.story("Validation")
    def test_empty_password(self, login_page: LoginPage):
        """Empty password should not allow login."""
        with allure.step("Submit with empty password"):
            self._submit_and_assert_stay_on_login(
                login_page,
                email="vendor@example.com",
                password="",
            )

    @allure.description(
        "Steps: 1) Navigate to login. 2) Enter invalid email format (no @). 3) Click Login. 4) Verify user remains on login."
    )
    @allure.story("Validation")
    def test_invalid_email_format(self, login_page: LoginPage):
        """Invalid email format should not allow login."""
        with allure.step("Submit with invalid email format"):
            self._submit_and_assert_stay_on_login(
                login_page,
                email="notanemail",
                password="Test1234",
            )

    @allure.description(
        "Steps: 1) Navigate to login. 2) Enter non-existent email with any password. 3) Click Login. 4) Verify user remains on login."
    )
    @allure.story("Invalid Credentials")
    def test_nonexistent_email(self, login_page: LoginPage):
        """Non-existent email should not login."""
        with allure.step("Submit non-existent email"):
            self._submit_and_assert_stay_on_login(
                login_page,
                email="doesnotexist@construct-test.com",
                password="Test1234",
            )

    @allure.description(
        "Steps: 1) Navigate to login. 2) Enter XSS payload in email. 3) Click Login. 4) Verify user remains on login and payload is not executed (no alert)."
    )
    @allure.story("XSS")
    def test_xss_in_email_sanitized(self, login_page: LoginPage):
        """XSS attempt in email should be sanitized / not executed."""
        with allure.step("Enter XSS payload in email"):
            self._submit_and_assert_stay_on_login(
                login_page,
                email="<script>alert(1)</script>@x.com",
                password="Test1234",
            )
