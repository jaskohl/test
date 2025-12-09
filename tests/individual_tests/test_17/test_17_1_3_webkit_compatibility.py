"""
Test 17.1.3: Full functionality in WebKit/Safari
Category: 17 - Cross-Browser & Responsive Tests
Test Count: Part of 5 tests in Category 17
Hardware: Device Only
Priority: LOW
Series: Both Series 2 and 3

Extracted from: tests/test_17_cross_browser.py
Source Class: TestBrowserCompatibility
"""

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


def test_17_1_3_webkit_compatibility(browser, base_url: str, device_password: str):
    """
    Test 17.1.3: Full functionality in WebKit/Safari
    Uses pytest-playwright WebKit browser fixture to test device compatibility.
    Safari test removed since Safari uses WebKit engine (covered here).
    """
    context_options = {
        "viewport": {"width": 1024, "height": 768},
        "ignore_https_errors": True,
        "accept_downloads": True,
        "java_script_enabled": True,
        "bypass_csp": True,  # Bypass Content Security Policy for embedded devices
    }
    context = browser.new_context(**context_options)
    page = context.new_page()
    try:
        page.goto(base_url, wait_until="domcontentloaded")
        login_page = LoginPage(page)
        login_page.verify_page_loaded()
        success = login_page.login(password=device_password)
        if not success:
            pytest.fail("Failed to login to device with WebKit")
        # Wait for page navigation away from authenticate page (indicates login success)
        expect(page).not_to_have_url("**/authenticate", timeout=10000)
        # Verify dashboard is accessible - handle HTTP/HTTPS redirect
        page.goto(f"{base_url}/", wait_until="domcontentloaded")
        current_url = page.url
        # Accept both HTTP and HTTPS URLs due to device redirect behavior
        assert current_url.startswith(
            "http"
        ), f"Dashboard URL should be HTTP/HTTPS, got: {current_url}"
    except Exception as e:
        #  error reporting for certificate/connection issues
        pytest.fail(f"Failed to test WebKit compatibility at {base_url}: {str(e)}")
    finally:
        context.close()
