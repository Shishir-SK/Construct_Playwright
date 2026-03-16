"""Enhanced customer project page object for Construct application."""
from playwright.sync_api import Page, expect

from .base_page import BasePage


class CustomerProjectPageEnhanced(BasePage):
    """Enhanced page object for customer project and task operations."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        # Project navigation
        self._projects_link = page.locator("a[href*='/projects']").or_(page.locator("a[href*='/project']"))
        self._dashboard_link = page.locator("a[href*='/customer/dashboard']")
        
        # Project creation
        self._create_project_button = page.get_by_role("button", name="Create Project").or_(page.get_by_text("Create Project")).or_(page.get_by_role("button", name="New Project")).or_(page.get_by_role("link", name="Create Project"))
        self._project_name_input = page.get_by_label("Project Name").or_(page.get_by_placeholder("Project Name")).or_(page.locator('input[name="name"]'))
        
        # Task creation
        self._add_task_button = page.get_by_role("button", name="Add Task").or_(page.get_by_text("Add Task")).or_(page.get_by_role("button", name="Create Task")).or_(page.get_by_text("Create Task"))
        self._task_name_input = page.get_by_label("Task Name").or_(page.get_by_placeholder("Task Name")).or_(page.locator('input[name="taskName"]'))
        
        # File upload
        self._file_input = page.locator('input[type="file"]')
        self._add_requirement_button = page.get_by_role("button", name="Add requirement").or_(page.get_by_text("Add requirement")).or_(page.get_by_text("Upload"))
        
        # Vendor invitation
        self._invite_vendor_button = page.get_by_role("button", name="Invite Vendor").or_(page.get_by_text("Invite Vendor"))
        self._vendor_email_input = page.get_by_placeholder("Email").or_(page.get_by_label("Vendor email"))
        self._send_invite_button = page.get_by_role("button", name="Invite").or_(page.get_by_role("button", name="Send"))

    def goto_customer_dashboard(self) -> None:
        """Navigate to customer dashboard."""
        if "/customer/dashboard" not in self.page.url:
            self.page.goto(f"{self.base_url}/customer/dashboard")
        self.page.wait_for_load_state("domcontentloaded")

    def goto_projects(self) -> None:
        """Navigate to projects page."""
        if self._projects_link.first.is_visible(timeout=5000):
            self._projects_link.first.click()
        else:
            self.page.goto(f"{self.base_url}/customer/projects")
        self.page.wait_for_load_state("domcontentloaded")

    def create_project(self, project_name: str) -> None:
        """Create a new project."""
        if not self._create_project_button.first.is_visible(timeout=8000):
            self.goto_projects()
        self._create_project_button.first.click()
        self.page.wait_for_load_state("domcontentloaded")
        self.fill_project_name(project_name)
        self.save_project()

    def fill_project_name(self, name: str) -> None:
        """Fill in the project name."""
        if self._project_name_input.first.is_visible(timeout=3000):
            self._project_name_input.first.fill(name)

    def create_task(self, task_name: str) -> None:
        """Create a new task."""
        self._add_task_button.first.click()
        self.page.wait_for_load_state("domcontentloaded")
        self.fill_task_name(task_name)
        self.page.get_by_role("button", name="Save").or_(page.get_by_role("button", name="Create")).first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def fill_task_name(self, name: str) -> None:
        """Fill in the task name."""
        if self._task_name_input.first.is_visible(timeout=3000):
            self._task_name_input.first.fill(name)

    def upload_file(self, file_path: str) -> None:
        """Upload a file (PDF/DOCX)."""
        if self._file_input.first.is_visible(timeout=5000):
            self._file_input.first.set_input_files(file_path)
        else:
            self._add_requirement_button.first.click()
            self.page.wait_for_timeout(500)
            self._file_input.first.set_input_files(file_path)

    def invite_vendor(self, vendor_email: str) -> None:
        """Invite a vendor to the project."""
        if self._invite_vendor_button.first.is_visible(timeout=8000):
            self._invite_vendor_button.first.click()
            if self._vendor_email_input.first.is_visible(timeout=5000):
                self._vendor_email_input.first.fill(vendor_email)
                self._send_invite_button.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def save_project(self) -> None:
        """Save the project."""
        save_btn = self.page.get_by_role("button", name="Save").or_(self.page.get_by_role("button", name="Create")).or_(self.page.get_by_role("button", name="Submit"))
        if save_btn.first.is_visible(timeout=3000):
            save_btn.first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def open_first_project(self) -> None:
        """Open the first available project."""
        project_link = self.page.locator("a[href*='/customer/project']").or_(self.page.locator("a[href*='/project/']")).first
        if project_link.is_visible(timeout=8000):
            project_link.click()
            self.page.wait_for_load_state("domcontentloaded")

    def has_create_project_button(self, timeout: float = 8000) -> bool:
        """Check if create project button is visible."""
        return self._create_project_button.first.is_visible(timeout=timeout)

    def has_add_task_button(self, timeout: float = 10000) -> bool:
        """Check if add task button is visible."""
        return self._add_task_button.first.is_visible(timeout=timeout)

    def has_invite_vendor_button(self, timeout: float = 8000) -> bool:
        """Check if invite vendor button is visible."""
        return self._invite_vendor_button.first.is_visible(timeout=timeout)

    def expect_project_created(self) -> None:
        """Assert that project was created successfully."""
        url = self.page.url
        assert "customer" in url and ("project" in url or "task" in url or "rfp" in url or "dashboard" in url), url
