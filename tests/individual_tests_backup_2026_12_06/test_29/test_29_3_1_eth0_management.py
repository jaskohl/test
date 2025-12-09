"""
Test 29 3 1 Eth0 Management Interface Testing
Category: 29 - Network Configuration Series 3
Extracted from: tests/grouped/test_29_network_config_series3.py
Source Class: TestEth0Management
Individual test file for better test isolation and debugging.

Purpose: Test eth0 management interface properties and PTP absence verification.
Expected: Test should verify eth0 IP visibility, editability, and confirm PTP is not available.
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


def test_29_3_1_eth0_management(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29 3 1 Eth0 Management Interface Testing

    Purpose: Test eth0 management interface properties and PTP absence verification.

    This test:
    1. Skips for non-Series 3 devices
    2. Navigates to network configuration page
    3. Expands eth0 collapsible panel before interaction
    4. Verifies eth0 IP address field is visible and editable
    5. Confirms PTP enable field is NOT visible (eth0 is management interface)
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # FIXED: Expand eth0 panel before field interaction
    _expand_eth0_panel(unlocked_config_page)

    eth0_ip = unlocked_config_page.locator("input[name='ip_eth0']")
    expect(eth0_ip).to_be_visible()
    expect(eth0_ip).to_be_editable()

    # eth0 is management interface - PTP should NOT be available
    assert not unlocked_config_page.locator(
        "input[name='ptp_enable_eth0']"
    ).is_visible()
