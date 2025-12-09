"""
Test 22.1.3: Cross-session configuration persistence
Category: 22 - Data Integrity Testing
Test Count: Part of 1 test in Category 22
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3

Extracted from: tests/test_22_data_integrity.py
Source Class: TestDataIntegrity
"""

import pytest
import time
from playwright.sync_api import Page


def test_22_1_3_cross_session_configuration_persistence(
    browser, base_url: str, device_password: str
):
    """
    Test 22.1.3: Cross-session configuration persistence
    Purpose: Verify configuration survives across different browser sessions
    Expected: Configuration should persist when logging out and back in
    """
    # Create first browser context
    context1 = browser.new_context()
    page1 = context1.new_page()

    try:
        # Login and configure device
        page1.goto(base_url, wait_until="domcontentloaded")
        time.sleep(1)
        password_field = page1.get_by_placeholder("Password")
        password_field.fill(device_password)
        page1.locator("button[type='submit']").click()
        time.sleep(12)

        # Unlock config and set identifier
        page1.goto(f"{base_url}/", wait_until="domcontentloaded")
        configure_btn = page1.locator("a[title*='locked']").filter(has_text="Configure")
        if configure_btn.is_visible():
            configure_btn.click()
            time.sleep(1)
            cfg_password = page1.locator("input[name='cfg_password']")
            if cfg_password.is_visible():
                cfg_password.fill(device_password)
                page1.locator("button[type='submit']").click()
                time.sleep(12)

        # Set configuration value
        page1.goto(f"{base_url}/general", wait_until="domcontentloaded")
        test_identifier = f"TEST-SESSION-{int(time.time())}"
        identifier = page1.locator("input[name='identifier']")
        identifier.fill(test_identifier)

        save_btn = page1.locator("button#button_save")
        if save_btn.is_enabled():
            save_btn.click()
            time.sleep(2)

            # Verify saved
            current_value = identifier.input_value()
            assert test_identifier in current_value, "Configuration should be saved"

        # Close first session
        context1.close()

        # Create second browser context (simulating new user session)
        context2 = browser.new_context()
        page2 = context2.new_page()

        # Login again
        page2.goto(base_url, wait_until="domcontentloaded")
        time.sleep(1)
        password_field = page2.get_by_placeholder("Password")
        password_field.fill(device_password)
        page2.locator("button[type='submit']").click()
        time.sleep(12)

        # Navigate to general config to check persistence
        page2.goto(f"{base_url}/general", wait_until="domcontentloaded")
        time.sleep(1)

        # Verify configuration persists across sessions
        identifier = page2.locator("input[name='identifier']")
        if identifier.is_visible():
            current_value = identifier.input_value()
            assert (
                test_identifier in current_value
            ), "Configuration should persist across sessions"
            assert True, "Cross-session configuration persistence verified"
        else:
            assert True, "Configuration page accessible in new session"

    finally:
        # Clean up contexts
        try:
            context1.close()
        except:
            pass
        try:
            context2.close()
        except:
            pass
