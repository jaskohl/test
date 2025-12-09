"""
Test 29 1 6 Gateway Persistence - Pure Page Object Pattern
Category: 29 - Network Configuration (Series 3)
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
Test Count: 6 of 60 in Category 29
Hardware: Device Only
Priority: HIGH - Gateway persistence validation
Series: Series 3 only
PATTERN: PURE PAGE OBJECT - No direct DeviceCapabilities calls
Based on test_29_network_config_series3.py::TestNetworkConfigSeries3::test_29_1_6_gateway_persistence
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage


def test_29_1_6_gateway_persistence(
    unlocked_config_page: Page, base_url: str, device_series: str, request
):
    """
    Test 29.1.6: Gateway Persistence - Pure Page Object Pattern
    Purpose: Test that gateway configuration persists across page navigation with device-aware validation
    Expected: Gateway value should be maintained after page reload/navigation
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

    # Get current gateway value with device-aware timeout
    device_timeout_multiplier = network_config_page.get_timeout_multiplier()
    field_timeout = int(5000 * device_timeout_multiplier)

    try:
        current_gateway_value = gateway_locator.input_value(timeout=field_timeout)
        print(f"Current gateway value: {current_gateway_value}")
    except Exception as e:
        current_gateway_value = ""  # Default if unable to get value
        print(f"Unable to get current gateway value: {e}")

    # Navigate away to another page and back using page object navigation
    try:
        # Navigate to general config page
        network_config_page.navigate_to_general_config()
        time.sleep(0.5)  # Brief pause for navigation

        # Navigate back to network configuration page
        network_config_page.navigate_to_page()
        time.sleep(0.5)  # Brief pause for navigation

        print(f"Navigation test completed for {device_model}")

    except Exception as e:
        pytest.fail(f"Navigation test failed for {device_model}: {e}")

    # Expand gateway panel again after navigation using page object method
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

    # Verify gateway value persisted with device-aware timeout
    try:
        persisted_gateway_value = gateway_locator.input_value(timeout=field_timeout)

        # Assert that gateway value persisted
        assert (
            persisted_gateway_value == current_gateway_value
        ), f"Gateway value should persist after navigation (was {current_gateway_value}, got {persisted_gateway_value})"

        print(f"Gateway persistence verified: {persisted_gateway_value}")

        # Log successful validation
        device_info = network_config_page.get_device_info()
        print(f"Gateway persistence test completed for {device_model}: {device_info}")

    except Exception as e:
        pytest.fail(f"Failed to verify gateway persistence for {device_model}: {e}")

    # Final validation through page object capabilities
    network_capable = network_config_page.has_capability("network")
    if not network_capable:
        pytest.skip(f"Device {device_model} does not support network configuration")

    print(f"GATEWAY PERSISTENCE VALIDATED: {device_model} (Series {actual_series})")

    # Additional persistence validation through page object
    try:
        # Verify page data includes gateway configuration
        page_data = network_config_page.get_page_data()
        gateway_in_data = any("gateway" in key.lower() for key in page_data.keys())

        if gateway_in_data:
            print(f"Gateway configuration found in page data for {device_model}")
        else:
            print(
                f"Gateway configuration not found in page data for {device_model} - may be device-specific"
            )

    except Exception as e:
        print(f"Page data validation failed for {device_model}: {e}")
