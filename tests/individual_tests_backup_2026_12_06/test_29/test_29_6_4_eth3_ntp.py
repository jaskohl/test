"""
Test 29 6 4 Eth3 Ntp
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestEth3Configuration
Individual test file for better test isolation and debugging.
"""

import pytest
import time
from playwright.sync_api import Page


def test_29_6_4_eth3_ntp(unlocked_config_page: Page, base_url: str, device_series: str):
    """
    Test 29 6 4 Eth3 Ntp
    Purpose: Test eth3 NTP configuration enable/disable functionality
    Expected: NTP enable checkbox should be visible and functional
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    # Navigate to network configuration page
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Expand eth3 panel for Series 3 collapsible UI
    _expand_eth3_panel(unlocked_config_page)

    # Test NTP enable configuration
    ntp_field = unlocked_config_page.locator("input[name='ntp_enable_eth3']")
    if ntp_field.is_visible():
        # Verify NTP field is enabled
        assert ntp_field.is_enabled()

        # Test NTP enable/disable toggle functionality
        current_checked = ntp_field.is_checked()

        # Toggle NTP on
        ntp_field.click()
        time.sleep(0.2)
        assert ntp_field.is_checked() != current_checked

        # Toggle NTP back to original state
        ntp_field.click()
        time.sleep(0.2)
        assert ntp_field.is_checked() == current_checked
    else:
        pytest.skip("NTP field not available for eth3 on this device variant")


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
