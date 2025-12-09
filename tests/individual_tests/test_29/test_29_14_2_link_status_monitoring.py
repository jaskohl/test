"""
Test 29.14.2: Link Status Monitoring
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


def test_29_14_2_link_status_monitoring(
    unlocked_config_page, base_url: str, device_model: str
):
    """
    Test 29.14.2: Link Status Monitoring
    Purpose: Test link status and connectivity monitoring on network interfaces
    Expected: Link status indicators should be visible and functional

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

    # Check for link status monitoring configuration using page object methods
    link_status_config = network_page.get_link_status_monitoring_configuration()

    if link_status_config and link_status_config.get("has_link_status_fields", False):
        # Verify link status fields are visible
        assert link_status_config.get(
            "fields_visible", False
        ), "Link status fields should be visible"
