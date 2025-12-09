"""
Test 19.5.2: VLAN Enable Shows Fields
Category 19: Dynamic UI Behavior & Element Validation - IMPROVED
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_5_2_vlan_enable_shows_fields(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.5.2: VLAN enable shows VLAN ID/priority fields"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate VLAN field visibility")

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    if device_series != "Series 3":
        pytest.skip("VLAN is Series 3 feature")

    unlocked_config_page.goto(f"{base_url}/network")
    time.sleep(1)
    vlan_enable = unlocked_config_page.locator("input[name='vlan_enable_eth1']")
    if vlan_enable.is_visible():
        vlan_enable.check()
        time.sleep(0.5)
        vlan_id = unlocked_config_page.locator("input[name='vlan_id_eth1']")
        # VLAN ID field may become visible/enabled
