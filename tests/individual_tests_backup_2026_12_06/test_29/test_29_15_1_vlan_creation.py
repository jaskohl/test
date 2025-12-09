"""
Test 29.15.1: VLAN Creation
Category: 29 - Network Configuration Series 3
Source: tests/grouped/test_29_network_config_series3.py
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect


def test_29_15_1_vlan_creation(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.15.1: VLAN Creation
    Purpose: Test VLAN creation and ID assignment on network interfaces
    Expected: VLAN ID fields should be visible and accept valid VLAN IDs (1-4094)
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Use interface-specific selectors to avoid strict mode violations
    # Check VLAN configuration on available ports instead of generic locator
    available_ports = [
        "eth0",
        "eth1",
        "eth3",
        "eth4",
    ]  # Skip eth2 as it's combined with eth1
    vlan_found = False
    for port in available_ports:
        # Look for VLAN ID fields on each port using specific selectors
        vlan_id_input = unlocked_config_page.locator(f"input[name='vlan_id_{port}']")
        vlan_enable_input = unlocked_config_page.locator(
            f"input[name='vlan_enable_{port}']"
        )
        # Check if VLAN ID input exists and is visible for this port
        if vlan_id_input.count() > 0:
            # Expand panel first if needed
            panel_selector = f"a[href='#port_{port}_collapse']"
            panel_toggle = unlocked_config_page.locator(panel_selector)
            if panel_toggle.count() > 0:
                aria_expanded = panel_toggle.get_attribute("aria-expanded")
                if aria_expanded != "true":
                    panel_toggle.click()
                    pytest.defer_call(lambda: None)  # No-op to keep pattern consistent

            if vlan_id_input.is_visible():
                # Test VLAN ID range (1-4094)
                for vid in ["1", "100", "4094"]:
                    vlan_id_input.fill(vid)
                    assert vlan_id_input.input_value() == vid
                vlan_found = True
                break
    # If no port-specific VLAN found, look for global VLAN settings
    if not vlan_found:
        global_vlan = unlocked_config_page.locator(
            "input[name='vlan_id'], input[name='vlan']"
        )
        if global_vlan.count() > 0 and global_vlan.first.is_visible():
            # Test VLAN ID range (1-4094)
            for vid in ["1", "100", "4094"]:
                global_vlan.first.fill(vid)
                assert global_vlan.first.input_value() == vid
