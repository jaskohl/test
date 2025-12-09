"""
Test 18.1.2: Multiple Section Configuration Workflow
Category: 18 - Workflow Tests
Test Count: Part of 8 tests in Category 18
Hardware: Device Only
Priority: HIGH - End-to-end workflow validation
Series: Both Series 2 and 3

Extracted from: tests/test_18_workflow.py
Source Class: TestCompleteConfigurationWorkflow
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_18_1_2_multi_section_configuration_workflow(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 18.1.2: Multiple Section Configuration Workflow (Device-Aware)
    Purpose: Verify can configure multiple sections in sequence
    Expected: Changes to different sections all persist
    Device-Aware: Uses actual device model for model-specific validation
    FIXED: Improved test isolation to prevent cleanup interference
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate multi-section workflow"
        )

    device_series = DeviceCapabilities.get_series(device_model)

    # Store original state for cleanup - isolate this test's state
    unlocked_config_page.goto(f"{base_url}/general", wait_until="domcontentloaded")
    general_page = GeneralConfigPage(unlocked_config_page)
    original_data = general_page.get_page_data()
    original_identifier = original_data.get("identifier", "")
    try:
        # Configure General
        test_identifier = f"Multi Section Test {int(time.time())}"
        general_page.configure_identifier(identifier=test_identifier)
        general_page.save_configuration()

        # Configure Display
        unlocked_config_page.goto(f"{base_url}/display", wait_until="domcontentloaded")
        display_mode = unlocked_config_page.locator("select[name='mode']")
        if display_mode.is_visible(timeout=2000):
            display_mode.select_option("Time")
            save_button = unlocked_config_page.locator("button#button_save")
            if save_button.is_enabled():
                save_button.click()
                # Use device-specific timeout if available
                known_issues = DeviceCapabilities.get_capabilities(device_model).get(
                    "known_issues", {}
                )
                timeout_multiplier = known_issues.get("timeout_multiplier", 1.0)
                save_delay = max(2.0 * timeout_multiplier, 2.0)
                time.sleep(save_delay)

        # Verify both configurations persisted
        unlocked_config_page.goto(f"{base_url}/general", wait_until="domcontentloaded")
        general_data = general_page.get_page_data()

        # FIXED: Use specific assertion with better error message
        assert (
            general_data.get("identifier") == test_identifier
        ), f"Expected identifier '{test_identifier}' but got '{general_data.get('identifier')}' on {device_model}"

        unlocked_config_page.goto(f"{base_url}/display", wait_until="domcontentloaded")
        display_after = unlocked_config_page.locator("select[name='mode']")
        if display_after.is_visible():
            expect(display_after).to_have_value("Time")
    finally:
        # FIXED: Isolated cleanup that doesn't interfere with other tests
        try:
            unlocked_config_page.goto(
                f"{base_url}/general", wait_until="domcontentloaded"
            )
            general_page = GeneralConfigPage(unlocked_config_page)
            if original_identifier:
                general_page.configure_identifier(identifier=original_identifier)
                general_page.save_configuration()
                time.sleep(2)
        except Exception as e:
            print(f"Warning: Cleanup failed but test passed for {device_model}: {e}")
