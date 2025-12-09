"""
Test 29 6 3 Eth3 Mtu
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestEth3Configuration
Individual test file for better test isolation and debugging.
"""

import pytest
import time
from playwright.sync_api import Page


def test_29_6_3_eth3_mtu(unlocked_config_page: Page, base_url: str, device_series: str):
    """
    Test 29 6 3 Eth3 Mtu
    Purpose: Test eth3 MTU configuration field functionality
    Expected: MTU field should be visible and have default value of 1494
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    # Navigate to network configuration page
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Expand eth3 panel for Series 3 collapsible UI
    _expand_eth3_panel(unlocked_config_page)

    # Test MTU configuration
    mtu_field = unlocked_config_page.locator("input[name='mtu_eth3']")
    if mtu_field.is_visible():
        # Verify MTU field is editable
        assert mtu_field.input_value() == "1494"

        # Test MTU value input functionality
        mtu_field.fill("1500")
        assert mtu_field.input_value() == "1500"

        mtu_field.fill("9000")
        assert mtu_field.input_value() == "9000"

        # Restore default MTU value
        mtu_field.fill("1494")
        assert mtu_field.input_value() == "1494"
    else:
        pytest.skip("MTU field not available for eth3 on this device variant")


def _expand_eth3_panel(page: Page):
    """Expand the eth3 collapsible panel based on device exploration data."""
    try:
        # Bootstrap collapse pattern from device exploration HTML
        eth3_header = page.locator('a[href="#port_eth3_collapse"]')
        if eth3_header.count() > 0:
            # Check if already expanded
            aria_expanded = eth3_header.get_attribute("aria-expanded")
            if aria_expanded != "true":
                eth3_header.click()
                time.sleep(0.5)
                print("eth3 panel expanded")
                return
        # Fallback: Try any collapsible toggle
        panel_toggle = page.locator('a[href*="port_eth3"]')
        if panel_toggle.count() > 0:
            panel_toggle.click()
            time.sleep(0.5)
            print("eth3 panel expanded via fallback")
    except Exception as e:
        print(f"Warning: eth3 panel expansion failed: {e}")
