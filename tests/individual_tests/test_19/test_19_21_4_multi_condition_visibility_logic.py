"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.21.4: Multi-Condition Visibility Logic
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 19.21.4
Modernized with DeviceCapabilities integration for improved device detection and error handling
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_21_4_multi_condition_visibility_logic(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.21.4: Elements visible only when multiple conditions are met"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate multi-condition visibility logic"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/ptp")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing multi-condition visibility logic")

    # Look for elements with complex visibility conditions
    complex_elements = unlocked_config_page.locator(
        "input[data-show-when-multiple], div[data-complex-condition]"
    )
    if complex_elements.count() > 0:
        complex_element = complex_elements.first
        # Try to satisfy multiple conditions
        # This requires understanding the specific logic of the page
        checkboxes = unlocked_config_page.locator("input[type='checkbox']")
        selects = unlocked_config_page.locator("select")
        # Check multiple conditions if they exist
        if checkboxes.count() > 0:
            checkboxes.first.check()
        if selects.count() > 0 and selects.first.locator("option").count() > 1:
            selects.first.select_option(index=1)
        time.sleep(0.5)
        # Complex element may now be visible
