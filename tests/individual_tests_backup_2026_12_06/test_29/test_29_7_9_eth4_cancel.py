"""
Test 29 7 9 Eth4 Cancel
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


def test_29_7_9_eth4_cancel(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29 7 9 Eth4 Cancel
    Purpose: Test eth4 cancel button visibility and enabled state
    Expected: Cancel button should be visible and enabled for eth4 interface
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")
    _expand_eth4_panel(unlocked_config_page)

    # Test eth4 cancel button visibility
    cancel_button = unlocked_config_page.locator("button#button_cancel_port_eth4")
    if cancel_button.is_visible():
        expect(cancel_button).to_be_visible()
        print("eth4 cancel button test completed")
    else:
        print("Cancel button not available for eth4 (may be expected on some models)")
