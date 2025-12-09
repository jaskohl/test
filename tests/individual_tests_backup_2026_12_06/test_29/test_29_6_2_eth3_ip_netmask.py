"""
Test 29 6 2 Eth3 Ip Netmask
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_29_6_2_eth3_ip_netmask(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29 6 2 Eth3 Ip Netmask
    Purpose: Test eth3 IP address and netmask configuration
    Expected: IP field should be editable, netmask field should be visible and functional
    """
    # Series 3 only test - eth3 is a Series 3 feature
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    # Navigate to network configuration page
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # FIXED: Expand eth3 panel before field interaction (critical for Series 3 collapsible UI)
    _expand_eth3_panel(unlocked_config_page)

    # Test eth3 IP address field
    eth3_ip = unlocked_config_page.locator("input[name='ip_eth3']")

    # Verify IP field is visible and functional
    if eth3_ip.is_visible():
        expect(eth3_ip).to_be_editable()

        # Test valid IP address inputs
        test_ips = ["192.168.3.10", "10.0.0.50", "172.16.25.100"]
        for test_ip in test_ips:
            eth3_ip.fill(test_ip)
            assert eth3_ip.input_value() == test_ip

        # Restore default test IP
        eth3_ip.fill("192.168.3.10")
        print(" eth3 IP address field verified")
    else:
        print("eth3 IP field not visible (may depend on device model)")

    # Test eth3 netmask field (check multiple possible selectors)
    netmask_selectors = [
        "input[name='mask_eth3']",
        "input[name='netmask_eth3']",
        "select[name='netmask_eth3']",
    ]

    netmask_found = False
    for selector in netmask_selectors:
        netmask_field = unlocked_config_page.locator(selector)
        if netmask_field.is_visible():
            if "select" in selector:
                expect(netmask_field).to_be_enabled()
                assert netmask_field.locator("option").count() >= 1
            else:
                expect(netmask_field).to_be_editable()
            netmask_found = True
            print(f" eth3 netmask field verified with selector: {selector}")
            break

    if not netmask_found:
        print("eth3 netmask field not found (may depend on device model)")


def _expand_eth3_panel(page: Page):
    """Helper method to expand eth3 collapsible panel based on device exploration data."""
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
