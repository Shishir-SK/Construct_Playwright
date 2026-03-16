"""Customer dashboard tests."""
import allure


@allure.epic("Construct")
@allure.feature("Customer Dashboard")
class TestCustomerDashboard:
    """Customer dashboard / post-login checks."""

    @allure.description(
        "Steps: 1) Login as customer. 2) Verify redirect to dashboard or create-organization page. 3) Verify no longer on login page."
    )
    @allure.story("Customer Post-Login")
    def test_dashboard_or_org_setup_loaded(
        self,
        logged_in_customer_page,
        base_url: str,
    ):
        """Verify customer login succeeds and reaches dashboard or org setup."""
        with allure.step("Verify URL is not login page"):
            url = logged_in_customer_page.url
            assert f"{base_url}/login" not in url
        with allure.step("Verify on dashboard or create-organization"):
            assert "dashboard" in url or "create-organization" in url
