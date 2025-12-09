"""
Test 15.4.1: Series 2 Network Modes Available
Category: 15 - Device Capability Detection Tests
Test Count: Part of 12 tests in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Series 2 Only

Extracted from: tests/test_15_capability_detection.py
Source Class: TestNetworkModeDetection
"""

import pytest
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage


def test_15_4_1_series2_network_modes(
    network_config_page: NetworkConfigPage, device_series: str
):
    """
    Test 15.4.1: Series 2 Network Modes Available
    Purpose: Verify Series 2 has 6 network modes
    Expected: DHCP, SINGLE, DUAL, BALANCE-RR, ACTIVE-BACKUP, BROADCAST
    Series: Series 2 Only
    """
    if device_series != "Series 2":
        pytest.skip("Test specific to Series 2")
    mode_select = network_config_page.page.locator("select[name='mode']")
    expect(mode_select).to_be_visible(timeout=2000)
    options = mode_select.locator("option")
    option_count = options.count()
    assert (
        option_count == 6
    ), f"Series 2 should have 6 network modes, found {option_count}"
    # Verify expected modes present
    expected_modes = [
        "DHCP",
        "SINGLE",
        "DUAL",
        "BALANCE-RR",
        "ACTIVE-BACKUP",
        "BROADCAST",
    ]
    for mode in expected_modes:
        option = mode_select.locator(f"option[value='{mode}']")
        assert option.count() > 0, f"Mode {mode} should be available"
