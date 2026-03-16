"""Configuration for Construct automation tests."""
import os

BASE_URL = os.getenv("CONSTRUCT_BASE_URL", "https://dev-app.helpconstruct.com")

# Credentials - use environment variables in CI for security
VENDOR_EMAIL = os.getenv("VENDOR_EMAIL", "rahul+412@codezyng.com")
CUSTOMER_EMAIL = os.getenv("CUSTOMER_EMAIL", "rahul+411@codezyng.com")
PASSWORD = os.getenv("CONSTRUCT_PASSWORD", "Test@123")
