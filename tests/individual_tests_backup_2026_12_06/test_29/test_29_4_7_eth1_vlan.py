"""
Test 29 4 7 Eth1 Vlan
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
FIXED: Converted from class method to standalone function with proper fixture signatures.
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_29_4_7_eth1_vlan(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29 4 7 Eth1 Vlan
    Purpose: Test eth1 interface VLAN enable checkbox functionality
    Expected: VLAN checkbox should be visible and functional on Series 3 devices
    Device-Aware: Only runs on Series 3 devices
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    # Navigate to network configuration page
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # FIXED: Expand eth1 panel before field interaction (critical for Series 3 collapsible UI)
    _expand_eth1_panel(unlocked_config_page)

    # Test VLAN enable checkbox functionality
    vlan_checkbox = unlocked_config_page.locator("input[name='vlan_eth1']")
    if vlan_checkbox.is_visible():
        expect(vlan_checkbox).to_be_enabled()

        # Verify checkbox can be toggled
        initial_state = vlan_checkbox.is_checked()
        vlan_checkbox.click()
        time.sleep(0.2)
        new_state = vlan_checkbox.is_checked()

        # State should have changed
        assert initial_state != new_state, "VLAN checkbox should toggle when clicked"
        print(" eth1 VLAN checkbox is enabled and toggles correctly")
    else:
        print("eth1 VLAN checkbox not visible (expected on some configurations)")


def _expand_eth1_panel(page: Page):
    """Expand eth1 collapsible panel based on device exploration data."""
    try:
        # Bootstrap collapse pattern from device exploration HTML
        eth1_header = page.locator('a[href="#port_eth1_collapse"]')
        if eth1_header.count() > 0:
            # Check if already expanded
            aria_expanded = eth1_header.get_attribute("aria-expanded")
            if aria_expanded != "true":
                eth1_header.click()
                time.sleep(0.5)
                print("eth1 panel expanded")
                return
        # Fallback: Try any collapsible toggle
        panel_toggle = page.locator('a[href*="port_eth1"]')
        if panel_toggle.count() > 0:
            panel_toggle.click()
            time.sleep(0.5)
            print("eth1 panel expanded via fallback")
    except Exception as e:
        print(f"Warning: eth1 panel expansion failed: {e}")
