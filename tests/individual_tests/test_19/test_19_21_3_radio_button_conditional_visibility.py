"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.21.3: Radio Button Conditional Visibility
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 19.21.3
Modernized with DeviceCapabilities integration for improved device detection and error handling
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_21_3_radio_button_conditional_visibility(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.21.3: UI elements controlled by radio button selections"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate radio button conditional visibility"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/network")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing radio button conditional visibility")

    # Look for radio button controlled elements
    radios = unlocked_config_page.locator("input[type='radio']")
    conditional_elements = unlocked_config_page.locator(
        "input[data-radio-value], div[data-radio-show]"
    )
    if radios.count() > 1 and conditional_elements.count() > 0:
        # Test different radio button selections
        for i in range(min(2, radios.count())):
            radio = radios.nth(i)
            radio.check()
            time.sleep(0.5)
            # Conditional elements may show/hide based on radio value
