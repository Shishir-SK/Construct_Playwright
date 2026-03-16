"""Base page object with common functionality."""
from playwright.sync_api import Page


class BasePage:
    """Base class for all page objects."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def navigate(self, path: str = ""):
        """Navigate to a path relative to base URL."""
        url = f"{self.base_url}{path}" if path.startswith("/") else f"{self.base_url}/{path}"
        self.page.goto(url)

    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.page.url
