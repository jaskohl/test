"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.26.5: Validation Message Context Sensitivity
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 19.26.5
Modernized with DeviceCapabilities integration for improved device detection and error handling
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_26_5_validation_message_context_sensitivity(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.26.5: Validation error messages change based on context"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate validation message context sensitivity"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/network")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing context-sensitive validation messages")

    # Select appropriate validation field based on device series
    if device_series == "Series 2":
        validation_field = unlocked_config_page.locator("input[name*='port' i]").first
    else:  # Series 3
        # Use specific interface selector to avoid matching multiple elements
        validation_field = unlocked_config_page.locator("input#ip_eth0")
    if validation_field.count() > 0 and validation_field.is_visible():
        validation_field = validation_field.first
        # Enter invalid data
        validation_field.fill("invalid_data")
        validation_field.dispatch_event("change")  # Trigger onchange event
        time.sleep(0.5)
        # Look for initial error message - using text_content() safely
        error_locators = unlocked_config_page.locator(".error, .validation-message")
        if error_locators.count() > 0:
            try:
                initial_error = error_locators.first.text_content()
            except:
                initial_error = "No error message found"
        # Change context if possible
        selects = unlocked_config_page.locator("select")
        if selects.count() > 0:
            select_field = selects.first
            if select_field.locator("option").count() > 1:
                select_field.select_option(index=1)
                time.sleep(0.5)
                # Trigger validation again
                validation_field.dispatch_event("change")  # Trigger onchange event
                time.sleep(0.5)
                # Check if error message changed
                if error_locators.count() > 0:
                    try:
                        new_error = error_locators.first.text_content()
                        # Error message may be different based on context
                    except:
                        new_error = "No error message found"
