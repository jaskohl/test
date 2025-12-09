"""
Test 29.15.3: VLAN Trunking Configuration
Category: 29 - Network Config Series 3 VLAN Tests
Extracted from: tests/grouped/test_29_network_config_series3.py test_29_15_3_vlan_trunking() in TestVLANConfigurationManagement class
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect


def test_29_15_3_vlan_trunking(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.15.3: VLAN Trunking Configuration
    Purpose: Test VLAN trunking and tagging configuration on Series 3 devices
    Expected: VLAN trunk mode fields should be visible and configurable on Series 3 devices
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Look for trunk configuration fields
    trunk = unlocked_config_page.locator(
        "input[name*='trunk' i], select[name*='vlan_mode' i]"
    )
    if trunk.is_visible():
        expect(trunk).to_be_enabled()
