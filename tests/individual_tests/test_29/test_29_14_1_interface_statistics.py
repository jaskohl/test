"""
Test 29 14 1 Interface Statistics
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.

TRANSFORMATION TO PURE PAGE OBJECT PATTERN:
- Uses NetworkConfigPage for all page interactions
- No direct DeviceCapabilities calls - encapsulated in page object
- Device-aware page load and capability validation
- Pure page object pattern implementation
"""

import pytest
from pages.network_config_page import NetworkConfigPage


def test_29_14_1_interface_statistics(
    unlocked_config_page, base_url: str, device_model: str
):
    """
    Test 29.14.1: Network interface monitoring and statistics

    Test network interface monitoring and statistics functionality.
    Series 3 devices only - checks for interface statistics availability and functionality.

    Pure page object pattern implementation:
    - Uses NetworkConfigPage for device-aware page interactions
    - No direct DeviceCapabilities calls - encapsulated in page object
    - Device-aware capability validation and timeout management
    """
    # Create NetworkConfigPage instance with device model
    network_page = NetworkConfigPage(unlocked_config_page, device_model=device_model)

    # Check device series using page object method
    device_series = network_page.get_series()

    if device_series != 3:
        pytest.skip("Series 3 only")

    # Navigate to network configuration using page object
    network_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Verify page loaded using device-aware validation
    network_page.verify_page_loaded()

    # Check for interface statistics configuration using page object methods
    interface_stats_config = network_page.get_interface_statistics_configuration()

    if interface_stats_config and interface_stats_config.get(
        "has_statistics_fields", False
    ):
        # Verify statistics fields are enabled
        assert interface_stats_config.get(
            "fields_enabled", False
        ), "Interface statistics fields should be enabled"
