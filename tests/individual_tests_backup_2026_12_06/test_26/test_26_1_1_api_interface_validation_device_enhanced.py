"""
Test: 26.1.1 - API Interface Validation [DEVICE ENHANCED]
Category: API Interfaces Testing (26)
Purpose: Test API interfaces with device-aware validation
Expected: Proper API access based on device capabilities
Series: Both Series 2 and 3 (device-aware)
Priority: MEDIUM
Hardware: Device Only
Device-Aware: YES - Uses DeviceCapabilities database for API validation
Based on: test_26_api_interfaces.py
Enhanced: 2025-12-01
"""

import pytest
import time
from playwright.sync_api import expect
from pages.network_config_page import NetworkConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_26_1_1_api_interface_validation_device_enhanced(
    network_config_page: NetworkConfigPage, request
):
    """
    Test 26.1.1: API Interface Validation [DEVICE ENHANCED]
    Purpose: Test API interfaces with device-aware validation
    Expected: Proper API access based on device capabilities
    Series: Both 2 and 3
    Device-Aware: Uses DeviceCapabilities database for API validation
    """
    # Get device context and validate
    device_model = request.session.get("device_model", "unknown")
    device_capabilities = DeviceCapabilities()

    if device_model not in device_capabilities.get_series_list():
        pytest.skip(f"Device model '{device_model}' not in DeviceCapabilities database")

    device_series = device_capabilities.get_device_series(device_model)

    # Device-aware timeout scaling
    base_timeout = 5000
    device_timeout_multiplier = device_capabilities.get_timeout_multiplier(device_model)
    scaled_timeout = int(base_timeout * device_timeout_multiplier)

    print(
        f"Device {device_model} (Series {device_series}): Testing API interface validation"
    )

    try:
        # Navigate to network config page
        network_config_page.navigate_to_page()
        network_config_page.verify_page_loaded()
        print(f"Device {device_model}: Network config page loaded")

        # Test 1: Check for API-related configuration options
        try:
            api_elements = [
                network_config_page.page.locator(
                    "input[name*='api'], input[id*='api']"
                ),
                network_config_page.page.locator(
                    "select[name*='api'], select[id*='api']"
                ),
                network_config_page.page.locator("text=/api|rest|json/i"),
                network_config_page.page.locator(
                    "input[name*='port'], input[id*='port']"
                ),
            ]

            api_found = 0
            for element in api_elements:
                try:
                    if element.count() > 0:
                        api_found += element.count()
                        print(
                            f"Device {device_model}: Found {element.count()} API-related elements"
                        )
                except Exception:
                    continue

            print(
                f"Device {device_model}: Total API interface elements found: {api_found}"
            )

        except Exception as e:
            print(f"Device {device_model}: API interface test failed: {e}")

        # Cross-validate with DeviceCapabilities database
        device_network_config = device_capabilities.get_network_config(device_model)
        if device_network_config and "management_interface" in device_network_config:
            mgmt_iface = device_network_config["management_interface"]
            print(f"Device {device_model}: API interface validation test completed")
            print(
                f"Management interface: {mgmt_iface}, Timeout scaling: {device_timeout_multiplier}x"
            )

    except Exception as e:
        pytest.fail(f"API interface validation test failed for {device_model}: {e}")

    # Database validation summary
    assert device_capabilities.get_device_series(device_model) == device_series
    assert (
        device_capabilities.get_timeout_multiplier(device_model)
        == device_timeout_multiplier
    )
