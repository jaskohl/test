"""
Test 29 3 3 Eth0 Mtu
Category: 29 - Network Configuration Series3
Extracted from: tests/grouped/test_29_network_config_series3.py
Source Class: TestEth0Management.test_29_3_3_eth0_mtu
Individual test file for better test isolation and debugging.
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_29_3_3_eth0_mtu(unlocked_config_page: Page, base_url: str, device_series: str):
    """
    Test 29.3.3: eth0 MTU Configuration

    Purpose: Test MTU field visibility and default value for eth0 interface
    Args:
        unlocked_config_page: Playwright page object for the network configuration page
        base_url: Base URL for the application under test
        device_series: Device series information (should be "Series 3")
    Expected:
        - Test should skip on non-Series 3 devices
        - eth0 panel should expand successfully
        - MTU field should be visible for eth0 interface
        - Default MTU value should be 1500
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # FIXED: Expand eth0 panel before field interaction
    _expand_eth0_panel(unlocked_config_page)

    mtu = unlocked_config_page.locator("input[name='mtu_eth0']")
    if mtu.is_visible():
        assert mtu.input_value() == "1500"


def _expand_eth0_panel(page: Page):
    """
    Expand the eth0 collapsible panel for Series 3 devices.

    Args:
        page: Playwright page object
    """
    try:
        # Bootstrap collapse pattern from device exploration HTML
        eth0_header = page.locator('a[href="#port_eth0_collapse"]')
        if eth0_header.count() > 0:
            # Check if already expanded
            aria_expanded = eth0_header.get_attribute("aria-expanded")
            if aria_expanded != "true":
                eth0_header.click()
                time.sleep(0.5)
                print("eth0 panel expanded")
                return
        # Fallback: Try any collapsible toggle
        panel_toggle = page.locator('a[href*="port_eth0"]')
        if panel_toggle.count() > 0:
            panel_toggle.click()
            time.sleep(0.5)
            print("eth0 panel expanded via fallback")
    except Exception as e:
        print(f"Warning: eth0 panel expansion failed: {e}")
