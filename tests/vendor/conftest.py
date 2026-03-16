"""Vendor-specific fixtures."""
import pytest

from pages.login_page import LoginPage


@pytest.fixture
def logged_in_vendor_page(page, login_page: LoginPage, vendor_credentials: dict, base_url: str):
    """Fixture that provides a page logged in as vendor on the vendor dashboard."""
    login_page.goto()
    login_page.login(
        email=vendor_credentials["email"],
        password=vendor_credentials["password"],
    )
    login_page.wait_for_login_complete()
    if "/vendor/dashboard" not in page.url:
        page.goto(f"{base_url}/vendor/dashboard")
        page.wait_for_load_state("domcontentloaded")
    return page
