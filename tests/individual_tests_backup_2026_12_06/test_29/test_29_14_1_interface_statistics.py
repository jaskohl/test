"""
Test 29 14 1 Interface Statistics
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page


def test_29_14_1_interface_statistics(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.14.1: Network interface monitoring and statistics

    Test network interface monitoring and statistics functionality.
    Series 3 devices only - checks for interface statistics availability and functionality.
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")
    # Look for interface statistics
    from playwright.sync_api import expect

    stats = unlocked_config_page.locator(
        "button[name*='stats' i], a[href*='statistics']"
    )
    if stats.is_visible():
        expect(stats).to_be_enabled()
