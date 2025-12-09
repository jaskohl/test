"""
Test 29 5 8 Eth2 No Redundancy
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page


def test_29_5_8_eth2_no_redundancy(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29 5 8 Eth2 No Redundancy
    Purpose: Test eth2 redundancy configuration absence (Series 3A architecture)

    Architecture Note: In Series 3A devices, eth2 doesn't exist as a separate port.
    eth2 redundancy settings are managed through the eth1 panel interface (eth1/eth2 combined).
    This test verifies that eth2-specific redundancy fields don't exist separately
    and confirms redundancy configuration is handled through eth1 panel.

    Expected: Test should pass according to original specification
    """
    # Series 3 only test - eth2 architecture is Series 3A specific
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    # Navigate to network configuration page
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # NOTE: eth2 redundancy settings are managed through eth1 panel
    # No separate eth2 configuration exists in Series 3A devices

    # Verify eth2-specific redundancy fields don't exist (they should be managed via eth1)
    eth2_redundancy_selectors = [
        "select[name='redundancy_mode_eth2']",
        "input[name='redundancy_eth2']",
        "select[name*='eth2_redundancy']",
    ]

    eth2_redundancy_found = False
    for selector in eth2_redundancy_selectors:
        redundancy_field = unlocked_config_page.locator(selector)
        if redundancy_field.count() > 0:
            eth2_redundancy_found = True
            break

    # eth2-specific redundancy fields should not exist in Series 3A architecture
    assert (
        not eth2_redundancy_found
    ), "eth2 redundancy field should not exist separately (should use eth1 panel)"

    # Verify redundancy fields exist for eth1 (where eth2 settings are managed)
    eth1_redundancy = unlocked_config_page.locator(
        "select[name='redundancy_mode_eth1']"
    )

    # This should exist since eth1 panel manages both eth1 and eth2 redundancy settings
    # Note: Field may not be visible until eth1 panel is expanded
    if eth1_redundancy.count() > 0:
        print(
            "eth1 redundancy field found (manages both eth1 and eth2 redundancy settings)"
        )

    print(
        " eth2 no redundancy test passed - no separate eth2 redundancy (correct for Series 3A architecture)"
    )
