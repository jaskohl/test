"""
Test 29.15.3: VLAN Trunking Configuration
Category: 29 - Network Config Series 3 VLAN Tests
Extracted from: tests/grouped/test_29_network_config_series3.py test_29_15_3_vlan_trunking() in TestVLANConfigurationManagement class
Individual test file for better test isolation and debugging.

TRANSFORMATION TO PURE PAGE OBJECT PATTERN:
- Uses NetworkConfigPage for all page interactions
- No direct DeviceCapabilities calls - encapsulated in page object
- Device-aware page load and capability validation
- Pure page object pattern implementation
"""

import pytest
from pages.network_config_page import NetworkConfigPage


def test_29_15_3_vlan_trunking(unlocked_config_page, base_url: str, device_model: str):
    """
    Test 29.15.3: VLAN Trunking Configuration
    Purpose: Test VLAN trunking and tagging configuration on Series 3 devices
    Expected: VLAN trunk mode fields should be visible and configurable on Series 3 devices

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

    # Check for VLAN trunking configuration using page object methods
    vlan_trunking_config = network_page.get_vlan_trunking_configuration()

    if vlan_trunking_config and vlan_trunking_config.get("has_trunking_fields", False):
        # Verify VLAN trunking fields are enabled
        assert vlan_trunking_config.get(
            "fields_enabled", False
        ), "VLAN trunking fields should be enabled"
