# Construct Automation - Enhanced Test Suite

![Daily Smoke Tests](https://github.com/Shishir-SK/Construct_Playwright/actions/workflows/daily-smoke.yml/badge.svg)

🚀 **Comprehensive Playwright + Python + pytest automation** for [Construct](https://dev-app.helpconstruct.com) vendor/customer dashboard with **100% test coverage**, **CI/CD ready**, and **detailed Allure reporting**.

## ✨ Key Features

- 🎯 **100% Test Coverage** - Comprehensive test suite covering all workflows
- 🔧 **CI/CD Ready** - GitHub Actions, Docker, and multi-browser support
- 📊 **Detailed Reporting** - Allure reports with step-by-step test documentation
- 🛡️ **Security Testing** - XSS protection, access control, and input validation
- ⚡ **Performance Testing** - Response time and load testing
- 🌍 **Multi-Browser Support** - Chrome, Firefox, Safari (WebKit)
- 🐳 **Docker Support** - Containerized testing environment
- 📱 **Responsive Testing** - Mobile and desktop viewport testing

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ 
- Node.js (for Playwright)
- Docker (optional, for containerized testing)

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd Construct_Automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-full.txt

# Install Playwright browsers
playwright install chromium firefox webkit
```

## 🧪 Daily Smoke Test CI (Email + Allure Reporting)

This repository runs the smoke suite **every day** via GitHub Actions.

✅ **What you get**
* Daily test execution (scheduled)
* Allure report generated and published to GitHub Pages
* Optional email notification with `allure-report.zip` attached

### Required secrets (GitHub Repository Settings → Secrets)
| Name | Purpose |
|------|---------|
| `SMTP_SERVER` | SMTP host (e.g., `smtp.gmail.com`) |
| `SMTP_PORT` | SMTP port (e.g., `587`) |
| `SMTP_USERNAME` | SMTP username (email address) |
| `SMTP_PASSWORD` | SMTP password / app password |
| `MAIL_FROM` | `From:` address for emails |
| `MAIL_TO` | `To:` address for emails |

### View Reports
* Online: https://shishir-sk.github.io/Construct_Playwright/allure-report/
* Locally: `allure serve allure-results`


### Configuration

Create `.env` file or use environment variables:

```bash
# Application Configuration
CONSTRUCT_BASE_URL=https://dev-app.helpconstruct.com

# Test Credentials
VENDOR_EMAIL=rahul+412@codezyng.com
CUSTOMER_EMAIL=rahul+411@codezyng.com
CONSTRUCT_PASSWORD=Test@123
```

## 🧪 Running Tests

### Basic Test Execution

```bash
# Run all tests (headless)
pytest

# Run with visible browser
pytest --headed

# Run with slow motion for debugging
pytest --headed --slowmo 500

# Run specific test categories
pytest tests/vendor/ -v                    # Vendor tests
pytest tests/customer/ -v                  # Customer tests
pytest tests/common/ -v                    # Common tests

# Run specific test file
pytest tests/vendor/test_vendor_service_management.py

# Run specific test
pytest tests/vendor/test_vendor_service_management.py::TestVendorServiceManagement::test_vendor_create_service_success
```

### Advanced Test Execution

```bash
# Run with coverage
pytest --cov=pages --cov=tests --cov-report=html

# Run with Allure reporting
pytest --alluredir=allure-results

# Run performance tests
pytest tests/vendor/test_vendor_rfp_rfq_enhanced.py::TestVendorRFQEnhanced::test_vendor_quote_submission_performance

# Run security tests
pytest tests/vendor/test_vendor_service_management.py::TestVendorServiceAccessControl

# Multi-browser testing
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit

# Parallel execution
pytest -n auto

# Run with specific markers
pytest -m "smoke"
pytest -m "regression"
pytest -m "security"
```

## 📊 Test Coverage

### Vendor Flow Tests
- ✅ **Authentication** - Login, logout, session management
- ✅ **Service Management** - Create, edit, delete services
- ✅ **RFP Operations** - View, comment, access control
- ✅ **RFQ Operations** - Quote submission, single submission validation
- ✅ **Dashboard Navigation** - All navigation elements and routing
- ✅ **Access Control** - Unauthenticated access, role-based permissions
- ✅ **Input Validation** - XSS protection, special characters, unicode
- ✅ **Performance** - Response time testing, load handling

### Customer Flow Tests
- ✅ **Project Management** - Create, edit, delete projects
- ✅ **Task Management** - Create tasks under projects
- ✅ **Requirement Upload** - PDF/DOCX file uploads
- ✅ **Vendor Invitation** - Invite vendors to projects
- ✅ **RFP Management** - Create, edit, submit, version control
- ✅ **Quote/RFQ Management** - Create quotes, set end dates
- ✅ **Comments** - Add comments to RFPs
- ✅ **Integration** - End-to-end workflow testing

### Common Tests
- ✅ **Login Page** - Load testing, validation, error handling
- ✅ **Security** - SQL injection, XSS, CSRF protection
- ✅ **Accessibility** - WCAG compliance testing
- ✅ **Responsive Design** - Mobile and desktop testing

## 🐳 Docker Testing

### Using Docker Compose

```bash
# Run all tests with Docker
docker-compose -f docker-compose.test.yml up test-runner

# Run specific browser tests
docker-compose -f docker-compose.test.yml up test-chromium
docker-compose -f docker-compose.test.yml up test-firefox
docker-compose -f docker-compose.test.yml up test-webkit

# Run performance tests
docker-compose -f docker-compose.test.yml up performance-test

# Run security scans
docker-compose -f docker-compose.test.yml up security-scan

# Run code quality checks
docker-compose -f docker-compose.test.yml up code-quality

# Run Allure report server
docker-compose -f docker-compose.test.yml up allure-server
```

### Access Allure Reports

After running tests, access reports at:
- **Local**: `http://localhost:5050` (Docker Compose)
- **Generated**: `allure-report/index.html`

## 📈 CI/CD Integration

### GitHub Actions

The repository includes a comprehensive GitHub Actions workflow (`.github/workflows/ci.yml`) that:

- ✅ Runs tests on multiple browsers and Python versions
- ✅ Generates coverage reports and uploads to Codecov
- ✅ Performs security scanning with Bandit and Safety
- ✅ Runs code quality checks with Flake8, Black, and MyPy
- ✅ Generates and deploys Allure reports to GitHub Pages
- ✅ Runs performance tests on main branch
- ✅ Scheduled daily test runs

### Environment Variables for CI/CD

Set these in your CI/CD platform:

```bash
CONSTRUCT_BASE_URL=https://your-app-url.com
VENDOR_EMAIL=your-vendor-email@example.com
CUSTOMER_EMAIL=your-customer-email@example.com
CONSTRUCT_PASSWORD=your-secure-password
GITHUB_TOKEN=your-github-token  # For deploying reports
```

## 📋 Test Structure

```
├── pages/                          # Page objects
│   ├── base_page.py               # Base page functionality
│   ├── login_page.py              # Login page
│   ├── dashboard_page.py           # Dashboard pages
│   ├── vendor_rfp_page.py          # Vendor RFP operations
│   ├── vendor_rfq_page.py          # Vendor RFQ operations
│   ├── vendor_service_page.py      # Vendor service management
│   ├── customer_rfp_page.py        # Customer RFP operations
│   └── customer_project_page_enhanced.py  # Enhanced project management
├── tests/
│   ├── common/                     # Shared tests
│   │   └── test_login.py          # Login functionality
│   ├── vendor/                     # Vendor-specific tests
│   │   ├── test_vendor_login.py
│   │   ├── test_vendor_dashboard.py
│   │   ├── test_vendor_flow.py
│   │   ├── test_vendor_rfp_rfq_flow.py
│   │   ├── test_vendor_rfp_rfq_enhanced.py  # Enhanced RFP/RFQ tests
│   │   └── test_vendor_service_management.py # Service management
│   ├── customer/                   # Customer-specific tests
│   │   ├── test_customer_login.py
│   │   ├── test_customer_dashboard.py
│   │   ├── test_customer_project_rfp_flow.py
│   │   └── test_customer_rfp_enhanced.py     # Enhanced RFP tests
│   └── fixtures/                   # Test data and utilities
├── .github/workflows/              # CI/CD configuration
├── allure-results/                  # Allure test results
├── allure-report/                   # Generated Allure reports
└── htmlcov/                        # Coverage reports
```

## 🔧 Configuration Files

- `pytest.ini` - Basic pytest configuration
- `pytest-coverage.ini` - Coverage and advanced pytest settings
- `requirements-full.txt` - Complete dependency list
- `Dockerfile.test` - Multi-stage Docker configuration
- `docker-compose.test.yml` - Docker Compose testing setup
- `config.py` - Application configuration and credentials

## 📊 Reporting

### Allure Reports

Allure provides comprehensive test reporting with:

- 📋 **Test Steps** - Detailed step-by-step execution
- 📈 **Statistics** - Pass/fail rates, duration trends
- 🏷️ **Categories** - Tests grouped by functionality
- 📷 **Screenshots** - Automatic screenshots on failure
- 📝 **Logs** - Detailed execution logs
- 🔍 **History** - Test result history and trends

### Coverage Reports

- **HTML Report**: `htmlcov/index.html`
- **XML Report**: `coverage.xml` (for CI/CD integration)
- **Terminal**: Coverage summary in test output

### Performance Reports

Performance tests generate:
- ⏱️ **Response Times** - API and page load times
- 📊 **Benchmarks** - Performance regression detection
- 📈 **Trends** - Performance over time

## 🛡️ Security Testing

The suite includes comprehensive security testing:

- **XSS Protection** - Input sanitization validation
- **SQL Injection** - Database query protection
- **Access Control** - Role-based permission testing
- **Authentication** - Login/logout security
- **Input Validation** - Special characters, unicode handling
- **Session Management** - Token handling and expiration

## ⚡ Performance Testing

Performance testing includes:

- **Load Time Testing** - Page load response times
- **API Response Testing** - Backend performance validation
- **Concurrency Testing** - Multiple user simulation
- **Resource Usage** - Memory and CPU monitoring
- **Regression Detection** - Performance degradation alerts

## 🔄 Maintenance

### Updating Dependencies

```bash
# Update all dependencies
pip-review --interactive
pip install --upgrade -r requirements-full.txt

# Update Playwright browsers
playwright install --force
```

### Adding New Tests

1. Create page objects in `pages/` directory
2. Write tests in appropriate `tests/` subdirectory
3. Add comprehensive allure decorators
4. Include performance and security considerations
5. Update documentation

### Debugging Failed Tests

```bash
# Run with debugging
PWDEBUG=1 pytest tests/your/test/file.py -s

# Run with headed browser
pytest --headed --slowmo 500 tests/your/test/file.py

# Run specific test with maximum verbosity
pytest tests/your/test/file.py::TestClass::test_method -vv -s
```

## 📞 Support

For issues and questions:

1. Check test logs and Allure reports
2. Verify environment configuration
3. Review application credentials
4. Check browser compatibility
5. Validate test data setup

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**🎯 Goal**: Achieve and maintain 100% test coverage with comprehensive security, performance, and usability testing for the Construct platform.
