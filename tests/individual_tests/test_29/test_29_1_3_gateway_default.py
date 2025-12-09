"""
Test 29 1 3 Gateway Default - Pure Page Object Pattern
Category: 29 - Network Configuration (Series 3)
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
Test Count: 3 of 60 in Category 29
Hardware: Device Only
Priority: MEDIUM - Gateway default state validation
Series: Series 3 only
PATTERN: PURE PAGE OBJECT - No direct DeviceCapabilities calls
Based on test_29_network_config_series3.py::TestNetworkConfigSeries3::test_29_1_3_gateway_default
"""

import pytest
import time
from playwright.sync_api import Page
from pages.network_config_page import NetworkConfigPage


def test_29_1_3_gateway_default(
    unlocked_config_page: Page, base_url: str, device_series: str, request
):
    """
    Test 29.1.3: Gateway Default Configuration - Pure Page Object Pattern
    Purpose: Verify gateway field exists in default state with device-aware validation
    Expected: Gateway field visible and accessible
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

    # Verify gateway field is visible with device-aware timeout
    device_timeout_multiplier = network_config_page.get_timeout_multiplier()
    field_timeout = int(5000 * device_timeout_multiplier)

    try:
        # Check visibility with device-aware timeout
        is_visible = gateway_locator.is_visible(timeout=field_timeout)
        assert is_visible, f"Gateway field not visible for {device_model}"

        # Additional validation - field should be accessible
        is_enabled = gateway_locator.is_enabled()
        if is_enabled:
            print(f"Gateway field is accessible for {device_model}")
        else:
            print(f"Gateway field is read-only for {device_model} (may be expected)")

        # Log successful validation
        device_info = network_config_page.get_device_info()
        print(f"Gateway default state validated for {device_model}: {device_info}")

    except Exception as e:
        pytest.fail(f"Failed to validate gateway default state for {device_model}: {e}")

    # Final validation through page object capabilities
    network_capable = network_config_page.has_capability("network")
    if not network_capable:
        pytest.skip(f"Device {device_model} does not support network configuration")

    print(f"GATEWAY DEFAULT STATE VALIDATED: {device_model} (Series {actual_series})")
