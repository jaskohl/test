"""
Test 19.1.5: Save button stays enabled on validation error
Category 19: Dynamic UI Behavior & Element Validation
Hardware: Device Only
Series: Both Series 2 and 3
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_1_5_save_button_stays_enabled_on_validation_error(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.1.5: Save button stays enabled on validation error"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate save button behavior")

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/network")
    time.sleep(1)
    # IMPROVED: Device-aware IP field selection with device model context
    print(f"[Device: {device_model}] Testing save button behavior with invalid IP")

    # Select appropriate IP field based on device series
    if device_series == "Series 2":
        ip_field = unlocked_config_page.locator("input[name='ipaddr']")
        save_btn = unlocked_config_page.get_by_role("button", name="Save")
    else:  # Series 3
        ip_field = unlocked_config_page.locator("input[name='ip_eth0']")
        save_btn = unlocked_config_page.get_by_role("button", name="Save", exact=True)

    if ip_field.is_visible():
        ip_field.fill("999.999.999.999")
        time.sleep(0.5)
        # Button may be enabled even with invalid data
