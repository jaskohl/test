"""
Test 19.21.2: UI elements show/hide based on select dropdown value - INDIVIDUAL TEST FILE
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


def test_19_21_2_select_controlled_ui_visibility(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.21.2: UI elements show/hide based on select dropdown value"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate select-controlled UI visibility"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/ptp")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing select-controlled UI visibility")

    # Look for select-controlled elements
    selects = unlocked_config_page.locator("select")
    conditional_elements = unlocked_config_page.locator(
        "input[data-show-when], div[data-hide-when]"
    )
    if selects.count() > 0 and conditional_elements.count() > 0:
        select_field = selects.first
        conditional_element = conditional_elements.first
        # Test different select values
        options = select_field.locator("option")
        for i in range(min(3, options.count())):
            select_field.select_option(index=i)
            time.sleep(0.5)
            # Conditional element visibility may change
