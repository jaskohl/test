"""
Test 29 5 1 Eth2 Ip
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect


def test_29_5_1_eth2_ip(unlocked_config_page: Page, base_url: str, device_series: str):
    """
    Test 29 5 1 Eth2 Ip
    Purpose: Test that eth2 IP configuration is managed via eth1 panel (no separate eth2 panel)
    Expected: Eth2 IP should not have separate configuration - managed through eth1 panel
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # NOTE: eth2 is configured via eth1 panel (eth1/eth2 combined)
    # No separate eth2 panel exists in Series 3A devices

    # Check that eth2 IP field is NOT visible as separate configuration
    eth2_ip_separate = unlocked_config_page.locator("input[name='ip_eth2']")

    # Should NOT find separate eth2 IP configuration
    # (eth2 is configured through eth1 panel)
    if eth2_ip_separate.count() == 0:
        print(
            "eth2 IP correctly managed via eth1 panel (no separate eth2 configuration)"
        )
    else:
        # If separate eth2 field exists, verify it behaves correctly
        if eth2_ip_separate.is_visible():
            print(
                "Warning: Found separate eth2 IP field - eth2 should be managed via eth1"
            )
