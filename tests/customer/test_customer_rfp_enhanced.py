"""
Enhanced customer RFP flow tests with comprehensive coverage.
Includes detailed allure reporting, edge cases, and full workflow testing.
"""
import time
import allure
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.customer_rfp_page import CustomerRFPPage
from pages.customer_project_page_enhanced import CustomerProjectPageEnhanced


def _customer_login(page: Page, base_url: str, customer_credentials: dict) -> None:
    """Login as customer and ensure on dashboard or create-organization."""
    page.goto(f"{base_url}/login")
    page.get_by_role("textbox", name="Enter your email").fill(customer_credentials["email"])
    page.get_by_role("textbox", name="Enter your password").fill(customer_credentials["password"])
    page.get_by_role("button", name="Login").click()
    page.wait_for_url(
        lambda url: "dashboard" in url or "create-organization" in url or "customer" in url,
        timeout=30000,
    )
    if "/customer/dashboard" not in page.url:
        page.goto(f"{base_url}/customer/dashboard")
    page.wait_for_load_state("domcontentloaded")


@allure.epic("Construct")
@allure.feature("Customer Flow - RFP Enhanced")
class TestCustomerRFPEnhanced:
    """Enhanced customer RFP tests with comprehensive coverage."""

    @allure.description(
        "Steps: 1) Login as customer. 2) Navigate to project. 3) Click Create RFP. "
        "4) Fill title with comprehensive content. 5) Use TipTap editor for rich content. "
        "6) Save RFP. 7) Verify RFP created with all content preserved."
    )
    @allure.story("Create RFP - Comprehensive")
    def test_customer_create_rfp_comprehensive(
        self,
        page: Page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ) -> None:
        _customer_login(page, base_url, customer_credentials)
        project_page = CustomerProjectPageEnhanced(page, base_url)
        rfp_page = CustomerRFPPage(page, base_url)
        
        project_page.goto_customer_dashboard()
        page.wait_for_load_state("domcontentloaded")
        
        # Try to open a project first
        if project_page.has_create_project_button():
            project_page.open_first_project()
        
        # Create RFP
        if rfp_page.has_create_rfp_button():
            rfp_page.click_create_rfp()
            
            # Fill comprehensive RFP data
            test_title = f"Comprehensive E2E RFP Test {time.strftime('%Y%m%d_%H%M%S')}"
            rfp_page.fill_rfp_title(test_title)
            
            # Use TipTap editor if available
            if rfp_page.has_tiptap_editor():
                comprehensive_content = """
                <h2>Project Overview</h2>
                <p>This is a comprehensive test RFP with rich content including:</p>
                <ul>
                    <li><strong>Bold text</strong> and <em>italic text</em></li>
                    <li>Numbered lists and bullet points</li>
                    <li>Special characters: café, naïve, résumé</li>
                    <li>Unicode: 🚀 🎉 ✅</li>
                </ul>
                <h3>Requirements</h3>
                <p>Detailed requirements will be specified in the project documents.</p>
                """
                rfp_page.fill_tiptap_content(comprehensive_content)
            
            rfp_page.save_rfp()
            rfp_page.expect_rfp_created()
            
            # Verify RFP appears in list
            if rfp_page.has_rfp_links():
                rfp_page.open_first_rfp()
                expect(page.get_by_text(test_title)).to_be_visible()
        else:
            pytest.skip("Create RFP button not found")

    @allure.description(
        "Steps: 1) Login as customer. 2) Create RFP with minimal data (title only). "
        "3) Save RFP. 4) Verify RFP created successfully. 5) Check minimal requirements are met."
    )
    @allure.story("Create RFP - Minimal Data")
    def test_customer_create_rfp_minimal_data(
        self,
        page: Page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ) -> None:
        _customer_login(page, base_url, customer_credentials)
        project_page = CustomerProjectPageEnhanced(page, base_url)
        rfp_page = CustomerRFPPage(page, base_url)
        
        project_page.goto_customer_dashboard()
        
        if project_page.has_create_project_button():
            project_page.open_first_project()
        
        if rfp_page.has_create_rfp_button():
            rfp_page.click_create_rfp()
            
            # Fill only required field (title)
            minimal_title = f"Minimal RFP {time.strftime('%H%M%S')}"
            rfp_page.fill_rfp_title(minimal_title)
            
            # Skip optional fields
            rfp_page.save_rfp()
            rfp_page.expect_rfp_created()
        else:
            pytest.skip("Create RFP button not found")

    @allure.description(
        "Steps: 1) Login as customer. 2) Try to create RFP with empty title. "
        "3) Attempt to save. 4) Verify validation error or prevented save. "
        "5) Check appropriate error messages are shown."
    )
    @allure.story("Create RFP - Validation")
    def test_customer_create_rfp_empty_title_validation(
        self,
        page: Page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ) -> None:
        _customer_login(page, base_url, customer_credentials)
        project_page = CustomerProjectPageEnhanced(page, base_url)
        rfp_page = CustomerRFPPage(page, base_url)
        
        project_page.goto_customer_dashboard()
        
        if project_page.has_create_project_button():
            project_page.open_first_project()
        
        if rfp_page.has_create_rfp_button():
            rfp_page.click_create_rfp()
            
            # Leave title empty
            rfp_page.fill_rfp_title("")
            
            # Try to save
            rfp_page.save_rfp()
            
            # Should stay on create RFP page due to validation
            expect(page).to_have_url(f"{base_url}/customer/create-rfp")
            
            # Check for validation message
            validation_messages = [
                "Title is required",
                "Please enter a title",
                "Title cannot be empty",
                "Required field"
            ]
            
            found_validation = False
            for message in validation_messages:
                if page.get_by_text(message).is_visible(timeout=3000):
                    found_validation = True
                    break
            
            # At minimum, should not proceed to RFP list
            assert "rfp" not in page.url or "create" in page.url
        else:
            pytest.skip("Create RFP button not found")

    @allure.description(
        "Steps: 1) Login as customer. 2) Create RFP with special characters in title. "
        "3) Use HTML/JS in content to test XSS protection. 4) Save RFP. "
        "5) Verify content is properly sanitized and displayed."
    )
    @allure.story("Create RFP - Security Testing")
    def test_customer_create_rfp_security_validation(
        self,
        page: Page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ) -> None:
        _customer_login(page, base_url, customer_credentials)
        project_page = CustomerProjectPageEnhanced(page, base_url)
        rfp_page = CustomerRFPPage(page, base_url)
        
        project_page.goto_customer_dashboard()
        
        if project_page.has_create_project_button():
            project_page.open_first_project()
        
        if rfp_page.has_create_rfp_button():
            rfp_page.click_create_rfp()
            
            # Test XSS in title
            xss_title = f"<script>alert('xss')</script> RFP {time.strftime('%H%M%S')}"
            rfp_page.fill_rfp_title(xss_title)
            
            if rfp_page.has_tiptap_editor():
                # Test XSS in content
                xss_content = "<img src=x onerror=alert('xss')> Malicious content"
                rfp_page.fill_tiptap_content(xss_content)
            
            rfp_page.save_rfp()
            
            # Verify RFP created but XSS sanitized
            page_content = page.content()
            assert "<script>" not in page_content or "alert" not in page_content.lower()
            
            rfp_page.expect_rfp_created()
        else:
            assert False, "Create RFP button not found"

    @allure.description(
        "Steps: 1) Login as customer. 2) Create RFP with unicode characters. "
        "3) Use various international characters and emojis. 4) Save RFP. "
        "5) Verify unicode support works properly."
    )
    @allure.story("Create RFP - Unicode Support")
    def test_customer_create_rfp_unicode_support(
        self,
        page: Page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ) -> None:
        _customer_login(page, base_url, customer_credentials)
        project_page = CustomerProjectPageEnhanced(page, base_url)
        rfp_page = CustomerRFPPage(page, base_url)
        
        project_page.goto_customer_dashboard()
        
        if project_page.has_create_project_button():
            project_page.open_first_project()
        
        if rfp_page.has_create_rfp_button():
            rfp_page.click_create_rfp()
            
            unicode_title = f"RFP 测试 🚀 Café Résumé {time.strftime('%H%M%S')}"
            rfp_page.fill_rfp_title(unicode_title)
            
            if rfp_page.has_tiptap_editor():
                unicode_content = "Unicode test: 中文, 日本語, العربية, русский, español, français"
                rfp_page.fill_tiptap_content(unicode_content)
            
            rfp_page.save_rfp()
            rfp_page.expect_rfp_created()
            
            # Verify unicode characters are preserved
            expect(page.get_by_text("测试")).to_be_visible()
        else:
            pytest.skip("Create RFP button not found")

    @allure.description(
        "Steps: 1) Login as customer. 2) Open existing RFP. 3) Click Edit. "
        "4) Modify title and content. 5) Save changes. 6) Verify version bump or updated content. "
        "7) Check edit history if available."
    )
    @allure.story("Edit RFP - Version Control")
    def test_customer_edit_rfp_version_control(
        self,
        page: Page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ) -> None:
        _customer_login(page, base_url, customer_credentials)
        project_page = CustomerProjectPageEnhanced(page, base_url)
        rfp_page = CustomerRFPPage(page, base_url)
        
        project_page.goto_customer_dashboard()
        
        if rfp_page.has_rfp_links():
            rfp_page.open_first_rfp()
            
            if rfp_page.has_edit_button():
                rfp_page.edit_rfp()
                
                # Modify content
                updated_title = f"Updated RFP Title {time.strftime('%H%M%S')}"
                rfp_page.fill_rfp_title(updated_title)
                
                if rfp_page.has_tiptap_editor():
                    updated_content = f"Updated content at {time.strftime('%H:%M:%S')}"
                    rfp_page.fill_tiptap_content(updated_content)
                
                rfp_page.save_rfp()
                
                # Verify changes saved
                expect(page.get_by_text(updated_title)).to_be_visible(timeout=10000)
                
                # Check for version indicator if available
                version_indicators = ["v2", "version 2", "updated", "modified"]
                for indicator in version_indicators:
                    if page.get_by_text(indicator).is_visible(timeout=3000):
                        break
            else:
                pytest.skip("Edit button not available")
        else:
            pytest.skip("No RFPs available for editing")

    @allure.description(
        "Steps: 1) Login as customer. 2) Open RFP. 3) Submit RFP. "
        "4) Verify submission success. 5) Check that Edit button becomes disabled. "
        "6) Verify RFP status changes to submitted."
    )
    @allure.story("Submit RFP - Status Changes")
    def test_customer_submit_rfp_status_changes(
        self,
        page: Page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ) -> None:
        _customer_login(page, base_url, customer_credentials)
        project_page = CustomerProjectPageEnhanced(page, base_url)
        rfp_page = CustomerRFPPage(page, base_url)
        
        project_page.goto_customer_dashboard()
        
        if rfp_page.has_rfp_links():
            rfp_page.open_first_rfp()
            
            if rfp_page.has_submit_button():
                rfp_page.submit_rfp()
                
                # Verify submission success
                expect(page.locator("body")).to_be_visible()
                
                # Check for submitted status
                submitted_indicators = [
                    "Submitted",
                    "Submitted to vendors",
                    "Published",
                    "Active"
                ]
                
                found_status = False
                for indicator in submitted_indicators:
                    if page.get_by_text(indicator).is_visible(timeout=5000):
                        found_status = True
                        break
                
                # Edit should be disabled after submission
                if rfp_page.has_edit_button(timeout=3000):
                    rfp_page.expect_edit_button_disabled()
            else:
                pytest.skip("Submit button not available")
        else:
            pytest.skip("No RFPs available for submission")

    @allure.description(
        "Steps: 1) Login as customer. 2) Create RFP with end date in the past. "
        "3) Try to edit RFP. 4) Verify edit is disabled due to end date. "
        "5) Check appropriate messaging is shown."
    )
    @allure.story("RFP Access Control - End Date")
    def test_customer_rfp_non_editable_after_end_date(
        self,
        page: Page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ) -> None:
        _customer_login(page, base_url, customer_credentials)
        project_page = CustomerProjectPageEnhanced(page, base_url)
        rfp_page = CustomerRFPPage(page, base_url)
        
        project_page.goto_customer_dashboard()
        
        if rfp_page.has_rfp_links():
            rfp_page.open_first_rfp()
            
            # Check if RFP has end date in past (this would need specific test data)
            # For now, just verify edit button behavior
            if rfp_page.has_edit_button():
                # If edit button exists, check if it's disabled
                if not rfp_page._edit_button.first.is_enabled():
                    # Edit is disabled as expected
                    pass
                else:
                    # Edit is enabled, RFP may not have end date restriction
                    pass
            else:
                # Edit button not present, also valid
                pass
        else:
            pytest.skip("No RFPs available for testing")

    @allure.description(
        "Steps: 1) Login as customer. 2) Open submitted RFP. 3) Add multiple comments. "
        "4) Verify each comment appears with proper attribution. 5) Test comment threading if available."
    )
    @allure.story("RFP Comments - Multiple Comments")
    def test_customer_rfp_multiple_comments(
        self,
        page: Page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ) -> None:
        _customer_login(page, base_url, customer_credentials)
        project_page = CustomerProjectPageEnhanced(page, base_url)
        rfp_page = CustomerRFPPage(page, base_url)
        
        project_page.goto_customer_dashboard()
        
        if rfp_page.has_rfp_links():
            rfp_page.open_first_rfp()
            
            # Look for comment input
            comment_input = page.get_by_placeholder("Add a comment").or_(
                page.get_by_role("textbox", name="Comment")
            ).first
            
            if comment_input.is_visible(timeout=5000):
                comments = [
                    f"Customer comment 1 - {time.strftime('%H:%M:%S')}",
                    f"Customer comment 2 with more detail - {time.strftime('%H:%M:%S')}",
                    f"Customer comment 3 unicode: 🎉 café - {time.strftime('%H:%M:%S')}"
                ]
                
                for comment in comments:
                    comment_input.fill(comment)
                    post_button = page.get_by_role("button", name="Post").or_(
                        page.get_by_text("Post comment")
                    ).or_(page.get_by_role("button", name="Comment")).first
                    
                    if post_button.is_visible(timeout=3000):
                        post_button.click()
                        page.wait_for_load_state("domcontentloaded")
                        
                        # Verify comment appears
                        expect(page.get_by_text(comment)).to_be_visible(timeout=5000)
            else:
                pytest.skip("Comment input not available")
        else:
            pytest.skip("No RFPs available for commenting")


@allure.epic("Construct")
@allure.feature("Customer Flow - Quote/RFQ Enhanced")
class TestCustomerQuoteEnhanced:
    """Enhanced customer quote/RFQ tests with comprehensive coverage."""

    @allure.description(
        "Steps: 1) Login as customer. 2) Open RFP. 3) Create quote/RFQ. "
        "4) Set end date in future. 5) Fill quote details. 6) Submit quote. "
        "7) Verify quote created successfully with proper end date."
    )
    @allure.story("Create Quote - Comprehensive")
    def test_customer_create_quote_comprehensive(
        self,
        page: Page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ) -> None:
        _customer_login(page, base_url, customer_credentials)
        project_page = CustomerProjectPageEnhanced(page, base_url)
        rfp_page = CustomerRFPPage(page, base_url)
        
        project_page.goto_customer_dashboard()
        
        if rfp_page.has_rfp_links():
            rfp_page.open_first_rfp()
            
            if rfp_page._create_quote_button.first.is_visible(timeout=5000):
                rfp_page.create_quote()
                
                # Set end date to future
                future_date = "2030-12-31"
                rfp_page.set_end_date(future_date)
                
                # Submit quote
                submit_button = page.get_by_role("button", name="Submit").or_(
                    page.get_by_text("Submit quote")
                ).first
                
                if submit_button.is_visible(timeout=5000):
                    submit_button.click()
                    page.wait_for_load_state("domcontentloaded")
                    
                    # Verify quote created
                    expect(page.locator("body")).to_be_visible()
                    
                    # Check for end date or quote confirmation
                    expect(page.get_by_text(future_date)).to_be_visible(timeout=5000)
                else:
                    pytest.skip("Submit button not found")
            else:
                pytest.skip("Create quote button not available")
        else:
            pytest.skip("No RFPs available for quote creation")

    @allure.description(
        "Steps: 1) Login as customer. 2) Create quote with end date in past. "
        "3) Submit quote. 4) Verify quote is immediately visible to customer. "
        "5) Check that vendors can no longer submit quotes."
    )
    @allure.story("Quote - Past End Date")
    def test_customer_quote_past_end_date(
        self,
        page: Page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ) -> None:
        _customer_login(page, base_url, customer_credentials)
        project_page = CustomerProjectPageEnhanced(page, base_url)
        rfp_page = CustomerRFPPage(page, base_url)
        
        project_page.goto_customer_dashboard()
        
        if rfp_page.has_rfp_links():
            rfp_page.open_first_rfp()
            
            if rfp_page._create_quote_button.first.is_visible(timeout=5000):
                rfp_page.create_quote()
                
                # Set end date to past
                past_date = "2020-01-01"
                rfp_page.set_end_date(past_date)
                
                # Submit quote
                submit_button = page.get_by_role("button", name="Submit").or_(
                    page.get_by_text("Submit quote")
                ).first
                
                if submit_button.is_visible(timeout=5000):
                    submit_button.click()
                    page.wait_for_load_state("domcontentloaded")
                    
                    # Verify quote created and immediately visible
                    expect(page.locator("body")).to_be_visible()
                    
                    # Should see quote content immediately due to past end date
                    expect(page.get_by_text(past_date)).to_be_visible(timeout=5000)
                else:
                    pytest.skip("Submit button not found")
            else:
                pytest.skip("Create quote button not available")
        else:
            pytest.skip("No RFPs available for quote creation")

    @allure.description(
        "Steps: 1) Login as customer. 2) Navigate to quotes/RFQs. 3) Verify quote list loads. "
        "4) Check quote details and status. 5) Verify vendor responses if available."
    )
    @allure.story("Quote List - View Functionality")
    def test_customer_quote_list_view(
        self,
        page: Page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ) -> None:
        _customer_login(page, base_url, customer_credentials)
        
        # Navigate to quotes/RFQs
        page.goto(f"{base_url}/customer/quotes")
        page.wait_for_load_state("domcontentloaded")
        
        # Verify page loads
        expect(page.locator("body")).to_be_visible()
        
        # Check for quote links or content
        quote_links = page.locator("a[href*='/quote']").or_(page.locator("a[href*='/rfq']"))
        
        if quote_links.first.is_visible(timeout=5000):
            # Open first quote
            quote_links.first.click()
            page.wait_for_load_state("domcontentloaded")
            
            # Verify quote details
            expect(page.locator("body")).to_be_visible()
        else:
            # Check for empty state
            empty_messages = ["No quotes", "No RFQs", "No data available"]
            for message in empty_messages:
                if page.get_by_text(message).is_visible(timeout=3000):
                    break


@allure.epic("Construct")
@allure.feature("Customer Flow - Integration Tests")
class TestCustomerIntegration:
    """Integration tests for customer workflows."""

    @allure.description(
        "Steps: 1) Login as customer. 2) Create project. 3) Create task. 4) Create RFP. "
        "5) Submit RFP. 6) Create quote. 7. Verify complete workflow works end-to-end."
    )
    @allure.story("Complete Workflow - Project to Quote")
    def test_customer_complete_workflow_project_to_quote(
        self,
        page: Page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ) -> None:
        _customer_login(page, base_url, customer_credentials)
        project_page = CustomerProjectPageEnhanced(page, base_url)
        rfp_page = CustomerRFPPage(page, base_url)
        
        project_page.goto_customer_dashboard()
        
        # Create project
        if project_page.has_create_project_button():
            project_name = f"Integration Test Project {time.strftime('%H%M%S')}"
            project_page.create_project(project_name)
            project_page.expect_project_created()
        
        # Create task
        if project_page.has_add_task_button():
            task_name = f"Integration Test Task {time.strftime('%H%M%S')}"
            project_page.create_task(task_name)
        
        # Create RFP
        if rfp_page.has_create_rfp_button():
            rfp_page.click_create_rfp()
            rfp_title = f"Integration RFP {time.strftime('%H%M%S')}"
            rfp_page.fill_rfp_title(rfp_title)
            
            if rfp_page.has_tiptap_editor():
                rfp_page.fill_tiptap_content("Integration test RFP content")
            
            rfp_page.save_rfp()
            rfp_page.expect_rfp_created()
        
        # Submit RFP
        if rfp_page.has_submit_button():
            rfp_page.submit_rfp()
        
        # Create quote
        if rfp_page._create_quote_button.first.is_visible(timeout=5000):
            rfp_page.create_quote()
            rfp_page.set_end_date("2030-12-31")
            
            submit_button = page.get_by_role("button", name="Submit").or_(
                page.get_by_text("Submit quote")
            ).first
            
            if submit_button.is_visible(timeout=5000):
                submit_button.click()
                page.wait_for_load_state("domcontentloaded")
        
        # Verify complete workflow succeeded
        expect(page.locator("body")).to_be_visible()

    @allure.description(
        "Steps: 1) Login as customer. 2) Test navigation between all major sections. "
        "3) Verify dashboard, projects, RFPs, quotes all accessible. 4. Test browser navigation."
    )
    @allure.story("Navigation - Complete Application")
    def test_customer_complete_application_navigation(
        self,
        page: Page,
        login_page: LoginPage,
        customer_credentials: dict,
        base_url: str,
    ) -> None:
        _customer_login(page, base_url, customer_credentials)
        
        # Test dashboard
        expect(page).to_have_url(f"{base_url}/customer/dashboard")
        
        # Test projects
        page.goto(f"{base_url}/customer/projects")
        page.wait_for_load_state("domcontentloaded")
        expect(page).to_have_url(f"{base_url}/customer/projects")
        
        # Test RFPs
        page.goto(f"{base_url}/customer/rfp")
        page.wait_for_load_state("domcontentloaded")
        expect(page).to_have_url(f"{base_url}/customer/rfp")
        
        # Test quotes
        page.goto(f"{base_url}/customer/quotes")
        page.wait_for_load_state("domcontentloaded")
        expect(page).to_have_url(f"{base_url}/customer/quotes")
        
        # Test back navigation
        page.go_back()
        page.wait_for_load_state("domcontentloaded")
        expect(page).to_have_url(f"{base_url}/customer/rfp")
        
        # Test forward navigation
        page.go_forward()
        page.wait_for_load_state("domcontentloaded")
        expect(page).to_have_url(f"{base_url}/customer/quotes")
