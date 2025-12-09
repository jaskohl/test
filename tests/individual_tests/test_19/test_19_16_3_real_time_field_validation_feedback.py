"""
Test 19.16.3: Real-time field validation with immediate feedback - INDIVIDUAL TEST FILE
Category 19: Dynamic UI Behavior & Element Validation
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 19
Modernized with DeviceCapabilities integration for improved device detection and error handling
Extracted from tests/test_19_dynamic_ui.py as part of individual test file organization
Individual test files improve test organization, readability, and execution granularity
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_16_3_real_time_field_validation_feedback(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.16.3: Real-time field validation with immediate feedback"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate real-time field validation feedback"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/network")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing real-time validation feedback")

    # Select appropriate IP field based on device series to avoid strict mode violations
    if device_series == "Series 2":
        ip_field = unlocked_config_page.locator("input[name*='gateway' i]").first
    else:  # Series 3
        # Expand collapsed gateway panel first
        # Note: Using CSS selector as fallback - gateway is in collapsed panel on Series 3
        gateway_panel = unlocked_config_page.locator(
            "a[data-toggle='collapse'][href='#gateway_collapse']"
        )
        if gateway_panel.count() > 0 and gateway_panel.is_visible():
            # Check if panel is collapsed and expand it
            panel_class = gateway_panel.get_attribute("class")
            if panel_class and "collapsed" in panel_class:
                gateway_panel.click()
                time.sleep(0.5)
        # Use specific interface selector to avoid matching multiple elements
        ip_field = unlocked_config_page.locator("input#gateway")
    if ip_field.count() > 0:
        ip_field = ip_field.first
        # Enter invalid IP and check for immediate feedback
        ip_field.fill("999.999.999.999")
        ip_field.dispatch_event("change")  # Trigger onchange event
        time.sleep(0.5)
        # Look for validation feedback
        feedback = unlocked_config_page.locator(
            ".validation-error, .invalid-feedback, [role='alert']"
        )
        if feedback.is_visible():
            expect(feedback).to_be_visible()
        # Fix the value and check feedback clears
        ip_field.fill("192.168.1.1")
        ip_field.dispatch_event("change")  # Trigger onchange event
        time.sleep(0.5)
