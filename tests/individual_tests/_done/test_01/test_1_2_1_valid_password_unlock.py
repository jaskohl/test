"""
Test 1.2.1: Valid Password Configuration Unlock
Purpose: Verify successful configuration unlock
Expected: Configuration sections become visible after unlock

Category: 1 - Authentication & Session Management
Test Type: Unit Test
Priority: CRITICAL
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.configuration_unlock_page import ConfigurationUnlockPage


def test_1_2_1_valid_password_unlock(
    logged_in_page: Page, base_url: str, device_password: str
):
    """
    Test 1.2.1: Valid Password Configuration Unlock
    Purpose: Verify successful configuration unlock
    Expected: Configuration sections become visible after unlock
    """
    unlock_page = ConfigurationUnlockPage(logged_in_page)
    # Navigate to configure
    logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")
    configure_button = logged_in_page.locator("a[title*='locked']").filter(
        has_text="Configure"
    )
    if configure_button.is_visible():
        configure_button.click()
        time.sleep(1)
    success = unlock_page.unlock_configuration(password=device_password)
    assert success, "Configuration unlock should succeed with valid password"
    # Wait for satellite loading (dynamic wait with 5s timeout based on device exploration)
    unlock_page.wait_for_satellite_loading()
    # Verify configuration sections visible
    config_sections = ["General", "Network", "Time", "Outputs"]
    for section in config_sections:
        link = logged_in_page.get_by_role("link", name=section)
        expect(link).to_be_visible(timeout=5000)
