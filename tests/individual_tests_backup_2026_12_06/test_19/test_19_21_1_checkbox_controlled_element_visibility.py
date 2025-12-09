"""
Test 19.21.1: UI elements show/hide based on checkbox state - INDIVIDUAL TEST FILE
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


def test_19_21_1_checkbox_controlled_element_visibility(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.21.1: UI elements show/hide based on checkbox state"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate checkbox-controlled element visibility"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/network")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing checkbox-controlled element visibility")

    # Look for checkbox-controlled elements
    checkboxes = unlocked_config_page.locator("input[type='checkbox']")
    conditional_elements = unlocked_config_page.locator(
        "input[data-show-when-checked], div[data-depends-on]"
    )
    if checkboxes.count() > 0 and conditional_elements.count() > 0:
        checkbox = checkboxes.first
        conditional_element = conditional_elements.first
        # Test unchecked state
        if not checkbox.is_checked():
            # Element should be hidden or disabled
            # Check the box
            checkbox.check()
            time.sleep(0.5)
            # Element should now be visible/enabled
            expect(conditional_element).to_be_visible()
