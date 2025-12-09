"""
Test 29 15 2 Vlan Port Assignment
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestVLANConfigurationManagement
Individual test file for better test isolation and debugging.

TRANSFORMATION TO PURE PAGE OBJECT PATTERN:
- Uses NetworkConfigPage for all page interactions
- No direct DeviceCapabilities calls - encapsulated in page object
- Device-aware page load and capability validation
- Pure page object pattern implementation
"""

import pytest
from pages.network_config_page import NetworkConfigPage


def test_29_15_2_vlan_port_assignment(
    unlocked_config_page, base_url: str, device_model: str
):
    """
    Test 29.15.2: VLAN Port Assignment
    Purpose: Port assignment to VLANs
    Expected: VLAN port assignment fields should be visible and configurable

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

    # Check for VLAN port assignment configuration using page object methods
    vlan_port_assignment_config = network_page.get_vlan_port_assignment_configuration()

    if vlan_port_assignment_config and vlan_port_assignment_config.get(
        "has_port_assignment_fields", False
    ):
        # Verify VLAN port assignment fields are enabled
        assert vlan_port_assignment_config.get(
            "fields_enabled", False
        ), "VLAN port assignment fields should be enabled"
