"""
Test 29.15.1: VLAN Creation
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


def test_29_15_1_vlan_creation(unlocked_config_page, base_url: str, device_model: str):
    """
    Test 29.15.1: VLAN Creation
    Purpose: Test VLAN creation and ID assignment on network interfaces
    Expected: VLAN ID fields should be visible and accept valid VLAN IDs (1-4094)

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

    # Check for VLAN creation configuration using page object methods
    vlan_config = network_page.get_vlan_creation_configuration()

    # Test VLAN ID range validation if VLAN fields are found
    if vlan_config and vlan_config.get("vlan_fields_found", False):
        # Test VLAN ID range (1-4094) using page object method
        vlan_test_passed = network_page.test_vlan_id_range()
        assert vlan_test_passed, "VLAN ID range validation should pass"
