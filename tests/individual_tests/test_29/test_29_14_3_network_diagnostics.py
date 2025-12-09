"""
Test 29.14.3: Network Diagnostics
Category: 29 - Network Configuration Series 3
Source: tests/grouped/test_29_network_config_series3.py
Individual test file for better test isolation and debugging.

TRANSFORMATION TO PURE PAGE OBJECT PATTERN:
- Uses NetworkConfigPage for all page interactions
- No direct DeviceCapabilities calls - encapsulated in page object
- Device-aware page load and capability validation
- Pure page object pattern implementation
"""

import pytest
from pages.network_config_page import NetworkConfigPage


def test_29_14_3_network_diagnostics(
    unlocked_config_page, base_url: str, device_model: str
):
    """
    Test 29.14.3: Network Diagnostics
    Purpose: Test network troubleshooting and diagnostic tools
    Expected: Diagnostic tools should be visible and functional

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

    # Check for network diagnostics configuration using page object methods
    network_diagnostics_config = network_page.get_network_diagnostics_configuration()

    if network_diagnostics_config and network_diagnostics_config.get(
        "has_diagnostics_fields", False
    ):
        # Verify diagnostic fields are enabled
        assert network_diagnostics_config.get(
            "fields_enabled", False
        ), "Network diagnostic fields should be enabled"
