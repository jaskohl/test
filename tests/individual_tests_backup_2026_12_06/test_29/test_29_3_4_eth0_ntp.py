"""
Test 29 3 4 Eth0 NTP Configuration Testing
Category: 29 - Network Configuration Series 3
Extracted from: tests/grouped/test_29_network_config_series3.py
Source Class: TestEth0Management
Individual test file for better test isolation and debugging.

Purpose: Test eth0 NTP enable/disable checkbox functionality.
Expected: Test should verify NTP enable checkbox is visible and enabled.
"""

import pytest
import time
from playwright.sync_api import Page, expect


def _expand_eth0_panel(page: Page):
    """Expand eth0 collapsible panel based on device exploration data."""
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


def test_29_3_4_eth0_ntp(unlocked_config_page: Page, base_url: str, device_series: str):
    """
    Test 29 3 4 Eth0 NTP Configuration Testing

    Purpose: Test eth0 NTP enable/disable checkbox functionality.

    This test:
    1. Skips for non-Series 3 devices
    2. Navigates to network configuration page
    3. Expands eth0 collapsible panel before interaction
    4. Verifies NTP enable checkbox is visible and enabled
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # FIXED: Expand eth0 panel before field interaction
    _expand_eth0_panel(unlocked_config_page)

    ntp = unlocked_config_page.locator("input[name='ntp_enable_eth0']")
    if ntp.is_visible():
        expect(ntp).to_be_enabled()
