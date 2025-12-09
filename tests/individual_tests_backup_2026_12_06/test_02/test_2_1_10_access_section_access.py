"""
Test 2.1.10: Access Section Accessible - Device-Aware
Purpose: Verify access section navigation and device-specific password configuration availability

Category: 2 - Configuration Section Navigation
Test Type: Unit Test
Priority: HIGH
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_2_1_10_access_section_access(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 2.1.10: Access Section Accessible - Device-Aware"""
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate access configuration")

    unlocked_config_page.goto(f"{base_url}/access")
    assert "access" in unlocked_config_page.url, "Should navigate to access page"

    # Device-aware access field verification
    # Both series use text inputs (not password type) with specific names
    cfgpwd_field = unlocked_config_page.locator("input[name='cfgpwd']")
    uplpwd_field = unlocked_config_page.locator("input[name='uplpwd']")
    stspwd_field = unlocked_config_page.locator("input[name='stspwd']")

    assert (
        cfgpwd_field.is_visible()
    ), f"Device {device_model} should have config password field (cfgpwd)"
    assert (
        uplpwd_field.is_visible()
    ), f"Device {device_model} should have upload password field (uplpwd)"
    assert (
        stspwd_field.is_visible()
    ), f"Device {device_model} should have status password field (stspwd)"
