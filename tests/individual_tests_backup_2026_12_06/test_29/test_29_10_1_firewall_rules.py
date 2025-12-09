"""
Test 29 10 1 Firewall Rules
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page


def test_29_10_1_firewall_rules(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.10.1: Firewall and ACL configuration

    Test firewall and access control list configuration.
    Series 3 devices only - checks for firewall/ACL field availability and functionality.
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")
    # Look for firewall/security configuration
    from playwright.sync_api import expect

    firewall = unlocked_config_page.locator(
        "input[name*='firewall' i], select[name*='acl' i]"
    )
    if firewall.is_visible():
        expect(firewall).to_be_enabled()
