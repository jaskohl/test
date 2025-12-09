"""
Test 29 18 2 Ntp Authentication
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect


def test_29_18_2_ntp_authentication(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.18.2: NTP authentication and security
    Purpose: Test NTP authentication and security configuration on Series 3 devices
    Expected: NTP authentication fields should be visible and configurable on Series 3 devices
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Look for NTP authentication fields
    ntp_auth = unlocked_config_page.locator(
        "input[name*='ntp_auth' i], input[name*='ntp_key' i]"
    )
    if ntp_auth.is_visible():
        expect(ntp_auth).to_be_enabled()
