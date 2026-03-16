"""Customer project, task, RFP, RFQ/quote page objects.

Locators are generic; refine with browser MCP (snapshot/inspect) if the app structure differs.
"""
from pathlib import Path

from playwright.sync_api import Page, expect

from .base_page import BasePage


class CustomerProjectPage(BasePage):
    """Customer: projects, tasks, RFP, RFQ/quote flows."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self._page = page
        # Customer dashboard / projects
        self._create_project_btn = page.get_by_role("button", name="Create Project").or_(
            page.get_by_text("Create Project")
        ).first
        self._projects_link = page.locator("a[href*='/customer/project']").or_(
            page.get_by_role("link", name="Projects")
        ).first
        # Project detail: add task, task list
        self._add_task_btn = page.get_by_role("button", name="Add Task").or_(
            page.get_by_text("Add Task")
        ).or_(page.get_by_role("button", name="Create Task")).first
        self._task_title_input = page.get_by_placeholder("Task name").or_(
            page.get_by_label("Task name")
        ).or_(page.get_by_role("textbox", name="Task name")).first
        # Requirement / file upload (requirement doc)
        self._requirement_upload = page.locator('input[type="file"]').first
        self._add_requirement_btn = page.get_by_role("button", name="Add requirement").or_(
            page.get_by_text("Add requirement")
        ).or_(page.get_by_text("Upload")).first
        # Invite vendor
        self._invite_vendor_btn = page.get_by_role("button", name="Invite Vendor").or_(
            page.get_by_text("Invite Vendor")
        ).first
        self._vendor_email_input = page.get_by_placeholder("Email").or_(
            page.get_by_label("Vendor email")
        ).first
        # RFP
        self._create_rfp_btn = page.get_by_role("button", name="Create RFP").or_(
            page.get_by_text("Create RFP")
        ).first
        self._rfp_title_input = page.get_by_placeholder("RFP title").or_(
            page.get_by_label("Title")
        ).first
        # TipTap / rich text (ProseMirror is common for TipTap)
        self._tiptap_editor = page.locator(".ProseMirror").or_(
            page.locator("[contenteditable='true']")
        ).or_(page.get_by_role("textbox").filter(has=page.locator(".."))).first
        self._edit_rfp_btn = page.get_by_role("button", name="Edit").or_(
            page.get_by_text("Edit")
        ).first
        self._submit_rfp_btn = page.get_by_role("button", name="Submit RFP").or_(
            page.get_by_text("Submit RFP")
        ).first
        self._save_rfp_btn = page.get_by_role("button", name="Save").or_(
            page.get_by_text("Save")
        ).first
        # Version
        self._version_text = page.get_by_text("Version").or_(page.locator("[data-version]")).first
        # Comments
        self._comment_input = page.get_by_placeholder("Add a comment").or_(
            page.get_by_role("textbox", name="Comment")
        ).first
        self._post_comment_btn = page.get_by_role("button", name="Post").or_(
            page.get_by_text("Post comment")
        ).or_(page.get_by_role("button", name="Comment")).first
        # RFQ / Quote (customer creates quote, sets end date)
        self._create_quote_btn = page.get_by_role("button", name="Create Quote").or_(
            page.get_by_text("Create Quote")
        ).or_(page.get_by_role("button", name="Create RFQ")).first
        self._quote_end_date_input = page.get_by_label("End date").or_(
            page.locator('input[type="date"]')
        ).first
        self._submit_quote_btn = page.get_by_role("button", name="Submit").or_(
            page.get_by_text("Submit quote")
        ).first

    def goto_customer_dashboard(self) -> None:
        """Navigate to customer dashboard."""
        self.navigate("/customer/dashboard")

    def goto_projects(self) -> None:
        """Go to projects list (from dashboard or nav)."""
        if "/customer/project" not in self._page.url and "/project" not in self._page.url:
            self._projects_link.click()
        self._page.wait_for_load_state("domcontentloaded")

    def click_create_project(self, timeout: float = 15000) -> None:
        """Click Create Project."""
        self._create_project_btn.wait_for(state="visible", timeout=timeout)
        self._create_project_btn.click()

    def fill_project_name(self, name: str) -> None:
        """Fill project name in create form."""
        inp = self._page.get_by_placeholder("Project name").or_(
            self._page.get_by_label("Project name")
        ).first
        inp.fill(name)

    def save_project(self) -> None:
        """Save/create project."""
        self._page.get_by_role("button", name="Save").or_(
            self._page.get_by_role("button", name="Create")
        ).first.click()

    def click_add_task(self, timeout: float = 15000) -> None:
        """Click Add Task / Create Task."""
        self._add_task_btn.wait_for(state="visible", timeout=timeout)
        self._add_task_btn.click()

    def fill_task_name(self, name: str) -> None:
        """Fill task name."""
        self._task_title_input.wait_for(state="visible", timeout=10000)
        self._task_title_input.fill(name)

    def upload_requirement_file(self, file_path: str) -> None:
        """Set file for requirement upload (use after clicking Add requirement if needed)."""
        path = Path(file_path).resolve()
        self._requirement_upload.set_input_files(str(path))

    def click_invite_vendor(self, timeout: float = 10000) -> None:
        """Click Invite Vendor."""
        self._invite_vendor_btn.wait_for(state="visible", timeout=timeout)
        self._invite_vendor_btn.click()

    def fill_vendor_email(self, email: str) -> None:
        """Fill vendor email in invite form."""
        self._vendor_email_input.fill(email)

    def click_create_rfp(self, timeout: float = 10000) -> None:
        """Click Create RFP."""
        self._create_rfp_btn.wait_for(state="visible", timeout=timeout)
        self._create_rfp_btn.click()

    def fill_rfp_title(self, title: str) -> None:
        """Fill RFP title."""
        self._rfp_title_input.fill(title)

    def fill_tiptap_content(self, text: str) -> None:
        """Type in TipTap/ProseMirror editor."""
        self._tiptap_editor.click()
        self._tiptap_editor.fill(text)

    def click_edit_rfp(self, timeout: float = 10000) -> None:
        """Click Edit on RFP."""
        self._edit_rfp_btn.wait_for(state="visible", timeout=timeout)
        self._edit_rfp_btn.click()

    def click_submit_rfp(self, timeout: float = 10000) -> None:
        """Click Submit RFP."""
        self._submit_rfp_btn.wait_for(state="visible", timeout=timeout)
        self._submit_rfp_btn.click()

    def add_comment(self, text: str) -> None:
        """Add a comment (after RFP submission)."""
        self._comment_input.fill(text)
        self._post_comment_btn.click()

    def expect_comment_visible(self, text: str) -> None:
        """Assert comment with given text is visible."""
        expect(self._page.get_by_text(text)).to_be_visible()

    def expect_edit_disabled_or_hidden(self) -> None:
        """Assert Edit is disabled or not visible (e.g. after end date or for invited vendor)."""
        edit_btn = self._page.get_by_role("button", name="Edit").or_(self._page.get_by_text("Edit")).first
        # Either disabled or not present
        try:
            expect(edit_btn).to_be_disabled()
        except Exception:
            expect(edit_btn).to_be_hidden()

    def click_create_quote(self, timeout: float = 10000) -> None:
        """Click Create Quote / Create RFQ."""
        self._create_quote_btn.wait_for(state="visible", timeout=timeout)
        self._create_quote_btn.click()

    def set_quote_end_date(self, date_str: str) -> None:
        """Set end date for quote/RFQ (e.g. YYYY-MM-DD)."""
        self._quote_end_date_input.fill(date_str)

    def click_submit_quote(self) -> None:
        """Submit quote (customer)."""
        self._submit_quote_btn.click()

    def expect_on_customer_dashboard(self) -> None:
        """Assert current URL is customer dashboard."""
        expect(self._page).to_have_url(lambda u: "/customer/dashboard" in u)

    def expect_on_project_or_task_page(self) -> None:
        """Assert we are on a project or task page."""
        url = self.get_current_url()
        assert "customer" in url and ("project" in url or "task" in url or "rfp" in url), url
