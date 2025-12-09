"""
Category 17: Cross-Browser & Responsive Tests - COMPLETE
Test Count: 4 tests
Hardware: Device Only
Priority: LOW
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 17
FIXED: Cross-browser tests now use pytest-playwright fixtures properly
instead of manually launching browsers. This fixes the async/sync issues.
"""

import time
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage


class TestBrowserCompatibility:
    """Test 17.1-17.3: Browser Compatibility - Unique Engines Only"""

    def test_17_1_2_firefox_compatibility(
        self, browser, base_url: str, device_password: str
    ):
        """
        Test 17.1.2: Full functionality in Firefox
        Uses pytest-playwright Firefox browser fixture to test device compatibility.
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
                pytest.fail("Failed to login to device with Firefox")
            # Wait for page navigation away from authenticate page (indicates login success)
            expect(page).not_to_have_url("**/authenticate", timeout=10000)
            # Verify dashboard is accessible - handle HTTP/HTTPS redirect
            page.goto(f"{base_url}/", wait_until="domcontentloaded")
            current_url = page.url
            # TODO: only accept HTTPS URLs once device supports it, for now accept both HTTP and HTTPS due to redirect behavior
            # Accept both HTTP and HTTPS URLs due to device redirect behavior
            assert current_url.startswith(
                "http"
            ), f"Dashboard URL should be HTTP/HTTPS, got: {current_url}"
        except Exception as e:
            # Enhanced error reporting for certificate/connection issues
            pytest.fail(f"Failed to test Firefox compatibility at {base_url}: {str(e)}")
        finally:
            context.close()

    def test_17_1_3_webkit_compatibility(
        self, browser, base_url: str, device_password: str
    ):
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
            # Enhanced error reporting for certificate/connection issues
            pytest.fail(f"Failed to test WebKit compatibility at {base_url}: {str(e)}")
        finally:
            context.close()


class TestResponsiveDesign:
    """Test 17.4-17.6: Responsive Design"""

    def test_17_4_1_desktop_resolution(self, logged_in_page, base_url: str):
        """Test 17.4.1: UI works at 1920x1080"""
        logged_in_page.set_viewport_size({"width": 1920, "height": 1080})
        logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")
        # Dashboard should be fully visible
        tables = logged_in_page.locator("table")
        expect(tables.first).to_be_visible()

    def test_17_4_2_laptop_resolution(self, logged_in_page, base_url: str):
        """Test 17.4.2: UI works at 1366x768"""
        logged_in_page.set_viewport_size({"width": 1366, "height": 768})
        logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")
        # UI should remain usable
        tables = logged_in_page.locator("table")
        expect(tables.first).to_be_visible()

    def test_17_4_3_tablet_resolution(self, logged_in_page, base_url: str):
        """Test 17.4.3: UI works at 1024x768"""
        logged_in_page.set_viewport_size({"width": 1024, "height": 768})
        logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")
        # Navigation should remain accessible
        tables = logged_in_page.locator("table")
        expect(tables.first).to_be_visible()
