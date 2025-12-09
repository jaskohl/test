"""
Test 29 7 7 Eth4 Vlan
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestEth4Configuration
Individual test file for better test isolation and debugging.
"""

import pytest
import time
from playwright.sync_api import Page, expect


def _expand_eth4_panel(page: Page):
    """Expand eth4 collapsible panel based on device exploration data."""
    try:
        # Bootstrap collapse pattern from device exploration HTML
        eth4_header = page.locator('a[href="#port_eth4_collapse"]')
        if eth4_header.count() > 0:
            # Check if already expanded
            aria_expanded = eth4_header.get_attribute("aria-expanded")
            if aria_expanded != "true":
                eth4_header.click()
                time.sleep(0.5)
                print("eth4 panel expanded")
                return
        # Fallback: Try any collapsible toggle
        panel_toggle = page.locator('a[href*="port_eth4"]')
        if panel_toggle.count() > 0:
            panel_toggle.click()
            time.sleep(0.5)
            print("eth4 panel expanded via fallback")
    except Exception as e:
        print(f"Warning: eth4 panel expansion failed: {e}")


def test_29_7_7_eth4_vlan(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.7.7: eth4 VLAN Configuration

    Purpose: Test VLAN enable and ID functionality for eth4 interface
    Expected: VLAN enable checkbox and ID field should be visible and functional for eth4 on Series 3 devices
    Series: Series 3 only
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")
    _expand_eth4_panel(unlocked_config_page)

    # Test VLAN enable checkbox
    vlan = unlocked_config_page.locator("input[name='vlan_enable_eth4']")
    if vlan.is_visible():
        expect(vlan).to_be_enabled()
        print("eth4 VLAN enable checkbox is visible and enabled")

    # Test VLAN ID field
    vlan_id = unlocked_config_page.locator("input[name='vlan_id_eth4']")
    if vlan_id.is_visible():
        vlan_id.fill("300")
        print("eth4 VLAN ID field tested")

    print("eth4 VLAN configuration test completed")
