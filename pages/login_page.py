"""Login page object for Construct application."""
from playwright.sync_api import Page, expect

from .base_page import BasePage


class LoginPage(BasePage):
    """Page object for the Construct login page."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self._email_input = page.get_by_placeholder("Enter your email")
        self._password_input = page.get_by_placeholder("Enter your password")
        self._login_button = page.get_by_role("button", name="Login")

    def goto(self):
        """Navigate to the login page."""
        self.navigate("/login")

    def login(self, email: str, password: str):
        """Perform login with given credentials."""
        self._email_input.fill(email)
        self._password_input.fill(password)
        self._login_button.click()

    def is_login_visible(self) -> bool:
        """Check if login form is visible."""
        return self._login_button.is_visible()

    def wait_for_login_complete(self, timeout: int = 25000):
        """Wait for login to complete and redirect (dashboard or welcome)."""
        self.page.wait_for_url(
            lambda url: "dashboard" in url or "welcome" in url,
            timeout=timeout,
        )

    def expect_login_form_visible(self):
        """Assert login form is visible."""
        expect(self._login_button).to_be_visible()
