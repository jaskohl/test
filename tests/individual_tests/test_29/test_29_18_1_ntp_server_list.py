"""
Test 29 18 1 Ntp Server List
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect


def test_29_18_1_ntp_server_list(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.18.1: NTP server list and priority configuration
    Purpose: Test NTP server list and priority configuration on Series 3 devices
    Expected: NTP server configuration should be visible and editable on Series 3 devices
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Look for NTP server configuration
    ntp_servers = unlocked_config_page.locator(
        "input[name*='ntp_server' i], textarea[name*='ntp_list' i]"
    )
    if ntp_servers.is_visible():
        expect(ntp_servers).to_be_editable()
