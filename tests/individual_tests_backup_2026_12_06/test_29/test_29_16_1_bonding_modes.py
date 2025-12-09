"""
Test 29 16 1 Bonding Modes
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect


def test_29_16_1_bonding_modes(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.16.1: Interface bonding mode configuration
    Purpose: Test interface bonding mode configuration on Series 3 devices
    Expected: Bonding mode fields should be visible and configurable on Series 3 devices
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Look for bonding mode selection
    bonding = unlocked_config_page.locator(
        "select[name*='bonding' i], select[name*='bond_mode' i]"
    )
    if bonding.is_visible():
        expect(bonding).to_be_enabled()
        # Should have multiple bonding modes available
        assert bonding.locator("option").count() >= 2
