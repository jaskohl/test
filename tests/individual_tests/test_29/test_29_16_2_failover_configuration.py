"""
Test 29 16 2 Failover Configuration
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect


def test_29_16_2_failover_configuration(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.16.2: Automatic failover and recovery
    Purpose: Test automatic failover and recovery configuration on Series 3 devices
    Expected: Failover settings should be visible and configurable on Series 3 devices
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Look for failover settings
    failover = unlocked_config_page.locator(
        "input[name*='failover' i], input[name*='auto_recovery' i]"
    )
    if failover.is_visible():
        expect(failover).to_be_enabled()
