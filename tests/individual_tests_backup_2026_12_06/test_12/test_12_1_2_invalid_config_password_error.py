"""
Test 12.1.2: Invalid Config Password Error
Category: 12 - Error Handling Tests
Test Count: Part of 12 tests in Category 12
Hardware: Device Only
Priority: HIGH - Proper error handling critical for reliability
Series: Both Series 2 and 3

Extracted from: tests/test_12_error_handling.py
Source Class: TestAuthenticationErrors
"""

import pytest
from playwright.sync_api import Page, expect
from pages.configuration_unlock_page import ConfigurationUnlockPage


def test_12_1_2_invalid_config_password_error(logged_in_page, base_url):
    """
    Test 12.1.2: Invalid Configuration Password Error
    Purpose: Verify error handling for invalid configuration unlock password
    Expected: Configuration unlock fails and appropriate error is indicated
    """
    logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")
    configure_button = logged_in_page.locator("a[title*='locked']").filter(
        has_text="Configure"
    )
    if configure_button.is_visible(timeout=2000):
        configure_button.click()
    unlock_page = ConfigurationUnlockPage(logged_in_page)
    success = unlock_page.unlock_configuration(password="wrong_unlock_password")
    assert not success, "Configuration unlock should fail with invalid password"
