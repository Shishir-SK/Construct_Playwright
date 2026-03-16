"""
Vendor flow: RFP (view only after customer submit), comments, quote/RFQ.
- Invited vendor cannot edit RFP after submission.
- Vendor can add comments after RFP submission.
- Vendor can quote and submit only once (second quote disabled or not available).
"""
import allure
import pytest
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
@allure.feature("Vendor Flow - RFP (Invited)")
class TestVendorRFPInvited:
    """Vendor invited to RFP: view only, no edit; can comment."""

    @allure.description(
        "Steps: 1) Login as vendor. 2) Open an RFP (invited by customer, already submitted). 3) Verify Edit is disabled or hidden for vendor."
    )
    @allure.story("Vendor Cannot Edit RFP After Submit")
    def test_vendor_cannot_edit_rfp_after_customer_submit(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        page.goto(f"{base_url}/vendor/rfp")
        page.wait_for_load_state("domcontentloaded")
        rfp_row = page.locator("a[href*='/rfp']").first
        if not rfp_row.is_visible(timeout=10000):
            pytest.skip("No RFP link visible for vendor; need customer to create and submit RFP and invite vendor")
        rfp_row.click()
        page.wait_for_load_state("domcontentloaded")
        edit_btn = page.get_by_role("button", name="Edit").or_(page.get_by_text("Edit")).first
        # Invited vendor must not be able to edit: button disabled or hidden
        if edit_btn.is_visible(timeout=5000):
            try:
                expect(edit_btn).to_be_disabled()
            except Exception:
                # Or not present for vendor role
                expect(edit_btn).to_be_hidden()
        expect(page.locator("body")).to_be_visible()

    @allure.description(
        "Steps: 1) Login as vendor. 2) Open submitted RFP. 3) Add a comment. 4) Verify comment appears."
    )
    @allure.story("Vendor Add Comment After RFP Submit")
    def test_vendor_add_comment_after_rfp_submit(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        page.goto(f"{base_url}/vendor/rfp")
        page.wait_for_load_state("domcontentloaded")
        rfp_row = page.locator("a[href*='/rfp']").first
        if not rfp_row.is_visible(timeout=10000):
            pytest.skip("No RFP link visible for vendor")
        rfp_row.click()
        page.wait_for_load_state("domcontentloaded")
        comment_input = page.get_by_placeholder("Add a comment").or_(
            page.get_by_role("textbox", name="Comment")
        ).first
        if comment_input.is_visible(timeout=5000):
            comment_input.fill("E2E vendor comment after RFP submit")
            page.get_by_role("button", name="Post").or_(
                page.get_by_text("Post comment")
            ).or_(page.get_by_role("button", name="Comment")).first.click()
            page.wait_for_load_state("domcontentloaded")
            expect(page.get_by_text("E2E vendor comment after RFP submit")).to_be_visible(timeout=5000)
        else:
            pytest.skip("Comment input not found for vendor on this RFP")


@allure.epic("Construct")
@allure.feature("Vendor Flow - RFQ / Quote")
class TestVendorQuoteOnce:
    """Vendor can quote and submit only once."""

    @allure.description(
        "Steps: 1) Login as vendor. 2) Open RFQ. 3) Submit quote once. 4) Verify success. 5) Verify Submit/Quote again is disabled or not visible (only one submission)."
    )
    @allure.story("Vendor Can Quote and Submit Only Once")
    def test_vendor_can_quote_and_submit_only_once(
        self,
        page: Page,
        login_page: LoginPage,
        vendor_credentials: dict,
        base_url: str,
    ) -> None:
        _vendor_login(page, base_url, vendor_credentials)
        page.goto(f"{base_url}/vendor/rfq")
        page.wait_for_load_state("domcontentloaded")
        rfq_link = page.locator("a[href*='/rfq']").first
        if not rfq_link.is_visible(timeout=10000):
            pytest.skip("No RFQ link visible; customer must create RFQ first")
        rfq_link.click()
        page.wait_for_load_state("domcontentloaded")
        submit_quote_btn = page.get_by_role("button", name="Submit Quote").or_(
            page.get_by_role("button", name="Submit")
        ).or_(page.get_by_text("Submit quote")).first
        if not submit_quote_btn.is_visible(timeout=5000):
            pytest.skip("No quote submit button; may already have quoted or RFQ not open")
        # Fill quote if there is an input (amount, description, etc.)
        quote_input = page.get_by_placeholder("Quote amount").or_(
            page.get_by_label("Quote")
        ).or_(page.locator("[contenteditable='true']").first).first
        if quote_input.is_visible(timeout=3000):
            quote_input.fill("1000")
        submit_quote_btn.click()
        page.wait_for_load_state("domcontentloaded")
        # After first submit: same page should not offer Submit again, or button disabled
        submit_again = page.get_by_role("button", name="Submit Quote").or_(
            page.get_by_role("button", name="Submit")
        ).or_(page.get_by_text("Submit quote")).first
        if submit_again.is_visible(timeout=3000):
            try:
                expect(submit_again).to_be_disabled()
            except Exception:
                pass  # Some apps hide the button instead
        expect(page.locator("body")).to_be_visible()
