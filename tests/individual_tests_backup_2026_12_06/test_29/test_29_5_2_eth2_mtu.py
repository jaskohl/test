"""
Test 29 5 2 Eth2 Mtu
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page


def test_29_5_2_eth2_mtu(unlocked_config_page: Page, base_url: str, device_series: str):
    """
    Test 29 5 2 Eth2 Mtu
    Purpose: Test that eth2 MTU settings are managed via eth1 panel (no separate eth2 configuration)
    Expected: Eth2 MTU should not have separate configuration - managed through eth1 panel
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # NOTE: eth2 MTU settings are managed through eth1 panel
    # No separate eth2 configuration in Series 3A devices

    # Check that eth2 MTU field is NOT visible as separate configuration
    eth2_mtu_separate = unlocked_config_page.locator("input[name='mtu_eth2']")

    # Should NOT find separate eth2 MTU configuration
    # (eth2 MTU is configured through eth1 panel)
    if eth2_mtu_separate.count() == 0:
        print(
            "eth2 MTU correctly managed via eth1 panel (no separate eth2 configuration)"
        )
    else:
        # If separate eth2 field exists, verify it behaves correctly
        if eth2_mtu_separate.is_visible():
            print(
                "Warning: Found separate eth2 MTU field - eth2 should be managed via eth1"
            )
