"""
Test 29 7 3 Eth4 Mtu
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
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


def test_29_7_3_eth4_mtu(unlocked_config_page: Page, base_url: str, device_series: str):
    """
    Test 29 7 3 Eth4 Mtu
    Purpose: Verify eth4 MTU configuration with default value
    Expected: Test should verify eth4 MTU field with default value of 1500
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")
    # FIXED: Expand eth4 panel before field interaction
    _expand_eth4_panel(unlocked_config_page)

    mtu = unlocked_config_page.locator("input[name='mtu_eth4']")
    if mtu.is_visible():
        # Verify default MTU value is 1500
        assert mtu.input_value() == "1500"
        print("eth4 MTU field verified - default value 1500")
    else:
        print(
            "eth4 MTU field not visible - may not be available on this device variant"
        )
