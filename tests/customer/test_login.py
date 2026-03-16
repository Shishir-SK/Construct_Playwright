"""Customer login flow tests."""
import allure
from playwright.sync_api import expect

from pages.login_page import LoginPage


@allure.epic("Construct")
@allure.feature("Login - Customer Flow")
class TestCustomerLoginFlow:
    """Customer login: success and customer-specific negative cases."""

    @allure.description(
        "Steps: 1) Navigate to login page. 2) Enter customer email and password. 3) Click Login. 4) Verify redirect to dashboard or org setup."
    )
    @allure.story("Customer Login Success")
    def test_customer_login_success(
        self,
        page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ):
        """Verify customer can login and reach dashboard or org setup."""
        with allure.step("Navigate to login page"):
            login_page.goto()
        with allure.step("Enter customer credentials and click Login"):
            login_page.login(
                email=customer_credentials["email"],
                password=customer_credentials["password"],
            )
        with allure.step("Wait for redirect to dashboard or create-organization"):
            page.wait_for_url(
                lambda url: "dashboard" in url or "create-organization" in url,
                timeout=15000,
            )
        with allure.step("Verify no longer on login page"):
            assert f"{base_url}/login" not in page.url

    @allure.description(
        "Steps: 1) Navigate to login. 2) Enter valid customer email with wrong password. 3) Click Login. 4) Verify user remains on login page."
    )
    @allure.story("Customer - Wrong Password")
    def test_customer_wrong_password(
        self, login_page: LoginPage, customer_credentials: dict
    ):
        """Customer email with wrong password should not login."""
        login_page.goto()
        login_page.login(
            email=customer_credentials["email"],
            password="WrongPassword999!",
        )
        expect(login_page.page).to_have_url(
            f"{login_page.base_url}/login",
            timeout=8000,
        )
