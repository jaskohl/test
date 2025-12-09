"""
Test 29 1 2 Gateway Validation - Pure Page Object Pattern
Category: 29 - Network Configuration (Series 3)
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
Test Count: 2 of 60 in Category 29
Hardware: Device Only
Priority: MEDIUM - Gateway validation
Series: Series 3 only
PATTERN: PURE PAGE OBJECT - No direct DeviceCapabilities calls
Based on test_29_network_config_series3.py::TestNetworkConfigSeries3::test_29_1_2_gateway_validation
"""

import pytest
import time
from playwright.sync_api import Page
from pages.network_config_page import NetworkConfigPage


def test_29_1_2_gateway_validation(
    unlocked_config_page: Page, base_url: str, device_series: str, request
):
    """
    Test 29.1.2: Gateway IP Validation - Pure Page Object Pattern
    Purpose: Verify gateway accepts valid IP addresses with device-aware validation
    Expected: Multiple valid IP formats accepted
    Series: Series 3 only
    Pattern: PURE PAGE OBJECT - No direct DeviceCapabilities calls
    """
    # Get device model and validate Series 3 requirement
    device_model = (
        request.session.device_hardware_model
        if hasattr(request.session, "device_hardware_model")
        else "unknown"
    )

    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    # Initialize page object with device-aware patterns
    network_config_page = NetworkConfigPage(
        unlocked_config_page, device_model=device_model
    )

    # Navigate to network configuration page using page object
    network_config_page.navigate_to_page()

    # Validate device series through page object
    actual_series = network_config_page.get_series()
    if actual_series != 3:
        pytest.skip(f"Series 3 only, detected Series {actual_series}")

    # Expand gateway panel before field interaction using page object method
    try:
        gateway_panel_expanded = network_config_page.expand_gateway_panel()
        if gateway_panel_expanded:
            time.sleep(0.5)  # Brief pause for panel expansion
        else:
            # Panel may already be expanded or not required for this device
            pass
    except Exception as e:
        # Panel expansion is optional - continue with test
        pass

    # Get gateway field locator through page object
    gateway_locator = network_config_page.get_gateway_field_locator()

    # Test valid IP addresses with device-aware timeout
    test_ips = ["172.16.0.1", "192.168.1.1", "10.0.0.1"]
    device_timeout_multiplier = network_config_page.get_timeout_multiplier()

    for ip in test_ips:
        try:
            # Fill gateway field with device-aware timeout
            gateway_locator.fill(ip, timeout=int(5000 * device_timeout_multiplier))

            # Verify the IP was accepted
            actual_value = gateway_locator.input_value()
            assert actual_value == ip, f"Expected IP {ip}, got {actual_value}"

            # Log successful validation
            print(f"Gateway IP validation successful: {ip}")

        except Exception as e:
            pytest.fail(f"Failed to validate gateway IP {ip}: {e}")

    # Log test completion through page object
    device_info = network_config_page.get_device_info()
    print(f"Gateway validation test completed for {device_model}: {device_info}")

    # Additional validation through page object capabilities
    capabilities = network_config_page.get_capabilities()
    network_capable = network_config_page.has_capability("network")

    if network_capable:
        print(f"Network capabilities validated for {device_model}")
    else:
        pytest.skip(f"Device {device_model} does not support network configuration")
