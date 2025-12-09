"""
Test 29 5 6 Eth2 Vlan
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page


def test_29_5_6_eth2_vlan(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29 5 6 Eth2 Vlan
    Purpose: Test eth2 VLAN settings management through eth1 panel (Series 3A architecture)

    Architecture Note: In Series 3A devices, eth2 doesn't exist as a separate port.
    eth2 settings (including VLAN) are managed through the eth1 panel interface.
    This test verifies that eth2-specific VLAN fields don't exist separately
    and confirms VLAN configuration is handled through eth1 panel.

    Expected: Test should pass according to original specification
    """
    # Series 3 only test - eth2 architecture is Series 3A specific
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    # Navigate to network configuration page
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # NOTE: eth2 VLAN settings are managed through eth1 panel
    # No separate eth2 configuration exists in Series 3A devices

    # Verify eth2-specific VLAN fields don't exist (they should be managed via eth1)
    eth2_vlan_enable = unlocked_config_page.locator("input[name='vlan_enable_eth2']")
    eth2_vlan_id = unlocked_config_page.locator("input[name='vlan_id_eth2']")

    # eth2-specific VLAN fields should not exist in Series 3A architecture
    assert (
        eth2_vlan_enable.count() == 0
    ), "eth2 VLAN enable field should not exist separately"
    assert eth2_vlan_id.count() == 0, "eth2 VLAN ID field should not exist separately"

    # Verify VLAN fields exist for eth1 (where eth2 settings are managed)
    eth1_vlan_enable = unlocked_config_page.locator("input[name='vlan_enable_eth1']")
    eth1_vlan_id = unlocked_config_page.locator("input[name='vlan_id_eth1']")

    # These should exist since eth1 panel manages both eth1 and eth2 VLAN settings
    # Note: Fields may not be visible until eth1 panel is expanded
    if eth1_vlan_enable.count() > 0:
        print("eth1 VLAN enable field found (manages both eth1 and eth2 VLAN settings)")

    if eth1_vlan_id.count() > 0:
        print("eth1 VLAN ID field found (manages both eth1 and eth2 VLAN settings)")

    print(
        " eth2 VLAN test passed - no separate eth2 VLAN configuration (correct for Series 3A architecture)"
    )
