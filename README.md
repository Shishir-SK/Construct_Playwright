# Construct Automation

Playwright + Python + pytest automation for [Construct](https://dev-app.helpconstruct.com) vendor/customer dashboard.

## Setup

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (uses project-local .playwright-browsers/)
playwright install chromium
```

## Configuration

Credentials are in `config.py`. For CI, use environment variables:

- `VENDOR_EMAIL` - Vendor login (default: shishir@codezyng.com)
- `CUSTOMER_EMAIL` - Customer login (default: test@zupaloop.com)
- `CONSTRUCT_PASSWORD` - Password (default: Test1234)
- `CONSTRUCT_BASE_URL` - Base URL (default: https://dev-app.helpconstruct.com)

## Running Tests

```bash
# Run all tests (headless)
pytest

# Run with visible browser
pytest --headed

# Run with slow motion
pytest --headed --slowmo 500

# Run by flow (vendor / customer / common)
pytest tests/vendor/ -v
pytest tests/customer/ -v
pytest tests/common/ -v

# Run specific test file
pytest tests/vendor/test_login.py
pytest tests/common/test_login.py

# Run specific test
pytest tests/vendor/test_login.py::TestVendorLoginFlow::test_vendor_login_success

# Run on different browser
pytest --browser webkit
pytest --browser firefox

# Debug mode
PWDEBUG=1 pytest tests/vendor/test_login.py -s

# Allure reports (after tests run)
allure generate allure-results -o allure-report --clean
allure serve allure-results
```

## Project Structure

```
├── config.py           # Configuration & credentials
├── conftest.py         # Pytest fixtures (base_url, login_page, credentials)
├── pytest.ini          # Pytest configuration
├── requirements.txt
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── dashboard_page.py
└── tests/
    ├── common/         # Shared tests (both flows)
    │   └── test_login.py   # Page load, invalid creds, SQL injection, validation, XSS
    ├── vendor/         # Vendor flow only
    │   ├── conftest.py     # logged_in_vendor_page fixture
    │   ├── test_login.py   # Vendor login success, vendor wrong password
    │   └── test_dashboard.py  # Vendor dashboard (nav, Services, Activity)
    └── customer/       # Customer flow only
        ├── conftest.py     # logged_in_customer_page fixture
        ├── test_login.py   # Customer login success, customer wrong password
        └── test_dashboard.py  # Customer post-login (dashboard/org setup)
```

## Test Coverage

- **common/**: Login page load, invalid credentials, SQL injection, empty/invalid fields, nonexistent email, XSS
- **vendor/**: Vendor login success, vendor wrong password; dashboard nav, Services, Activity
- **customer/**: Customer login success, customer wrong password; dashboard or org setup loaded
