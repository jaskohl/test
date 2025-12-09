"""
Test 1.1.1: Valid Password Login
Purpose: Verify successful login with correct password
Expected: Login succeeds, satellite loading occurs, dashboard visible

Category: 1 - Authentication & Session Management
Test Type: Unit Test
Priority: CRITICAL
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


def test_1_1_1_valid_password_login(page: Page, base_url: str, device_password: str):
    """
    Test 1.1.1: Valid Password Login
    Purpose: Verify successful login with correct password
    Expected: Login succeeds, satellite loading occurs, dashboard visible
    """
    page.goto(base_url, wait_until="domcontentloaded")
    login_page = LoginPage(page)
    login_page.verify_page_loaded()
    success = login_page.login(password=device_password)
    assert success, "Login should succeed with valid password"
    # Wait for satellite loading (dynamic wait with 5s timeout based on device exploration)
    login_page.wait_for_satellite_loading()
    # Verify dashboard is visible (check for Configure button presence)
    configure_button = page.locator("a[title*='locked']").filter(has_text="Configure")
    assert configure_button.is_visible(), "Should show Configure button after login"
