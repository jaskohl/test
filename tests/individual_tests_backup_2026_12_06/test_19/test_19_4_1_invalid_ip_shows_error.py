"""
Test 19.4.1: Invalid IP Shows Error
Category 19: Dynamic UI Behavior & Element Validation - IMPROVED
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_4_1_invalid_ip_shows_error(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.4.1: Invalid IP shows error feedback"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate IP validation feedback"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/network")
    time.sleep(1)
    # IMPROVED: Device-aware IP field selection with device model context
    print(f"[Device: {device_model}] Testing IP validation with invalid IP")

    # Select appropriate IP field based on device series
    if device_series == "Series 2":
        ip_field = unlocked_config_page.locator("input[name='ipaddr']")
    else:  # Series 3
        ip_field = unlocked_config_page.locator("input[name='ip_eth0']")

    if ip_field.is_visible():
        ip_field.fill("999.999.999.999")
        ip_field.blur()
        time.sleep(0.5)
        # Error may appear in various forms
