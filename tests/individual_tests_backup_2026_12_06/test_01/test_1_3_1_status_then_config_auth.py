"""
Test 1.3.1: Complete Dual Authentication Flow
Purpose: Verify both authentication cycles work in sequence
Expected: Login succeeds, then unlock succeeds, full access granted

Category: 1 - Authentication & Session Management
Test Type: Unit Test
Priority: CRITICAL
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.configuration_unlock_page import ConfigurationUnlockPage


def test_1_3_1_status_then_config_auth(page: Page, base_url: str, device_password: str):
    """
    Test 1.3.1: Complete Dual Authentication Flow
    Purpose: Verify both authentication cycles work in sequence
    Expected: Login succeeds, then unlock succeeds, full access granted
    """
    # First authentication: Status monitoring
    page.goto(base_url, wait_until="domcontentloaded")
    login_page = LoginPage(page)
    login_success = login_page.login(password=device_password)
    assert login_success, "First authentication (login) should succeed"
    # Wait for satellite loading (dynamic wait with 5s timeout based on device exploration)
    login_page.wait_for_satellite_loading()
    # Second authentication: Configuration access
    unlock_page = ConfigurationUnlockPage(page)
    page.goto(f"{base_url}/", wait_until="domcontentloaded")
    configure_button = page.locator("a[title*='locked']").filter(has_text="Configure")
    if configure_button.is_visible():
        configure_button.click()
    unlock_success = unlock_page.unlock_configuration(password=device_password)
    assert unlock_success, "Second authentication (unlock) should succeed"
    # Wait for satellite loading (dynamic wait with 5s timeout based on device exploration)
    unlock_page.wait_for_satellite_loading()
    # Verify full access
    access_info = unlock_page.get_configuration_access_level()
    assert not access_info["locked"], "Configuration should be fully unlocked"
    assert (
        len(access_info["sections_available"]) >= 5
    ), "Should have access to multiple sections"
