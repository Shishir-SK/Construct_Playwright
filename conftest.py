"""Pytest configuration and shared fixtures for Construct automation."""
import os

import pytest

def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: marks tests as smoke tests (run first for basic functionality)")

# Allow headed mode for debugging
@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Allow headed mode for debugging; can be overridden with --headed."""
    return {"headless": False}

# Use project-local browser cache (avoids sandbox path conflicts)
_project_dir = os.path.dirname(os.path.abspath(__file__))
_browsers_path = os.path.join(_project_dir, ".playwright-browsers")
# Force project-local path (override any sandbox/cache path)
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = _browsers_path

from config import BASE_URL
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the Construct application."""
    return BASE_URL


@pytest.fixture
def login_page(page, base_url):
    """Login page object with navigated page."""
    return LoginPage(page, base_url)


@pytest.fixture
def vendor_credentials():
    """Vendor user credentials."""
    from config import VENDOR_EMAIL, PASSWORD
    return {"email": VENDOR_EMAIL, "password": PASSWORD}


@pytest.fixture
def customer_credentials():
    """Customer user credentials."""
    from config import CUSTOMER_EMAIL, PASSWORD
    return {"email": CUSTOMER_EMAIL, "password": PASSWORD}
