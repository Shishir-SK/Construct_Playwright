"""Customer-specific fixtures."""
import pytest

from pages.login_page import LoginPage


@pytest.fixture
def logged_in_customer_page(page, login_page: LoginPage, customer_credentials: dict, base_url: str):
    """Fixture that provides a page logged in as customer."""
    login_page.goto()
    login_page.login(
        email=customer_credentials["email"],
        password=customer_credentials["password"],
    )
    page.wait_for_url(
        lambda url: "dashboard" in url or "create-organization" in url,
        timeout=15000,
    )
    return page
