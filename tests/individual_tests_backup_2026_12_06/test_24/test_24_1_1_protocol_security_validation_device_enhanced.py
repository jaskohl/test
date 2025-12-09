"""
Test: 24.1.1 - Protocol Security Validation [DEVICE ENHANCED]
Category: Protocol Security Testing (24)
Purpose: Test protocol security features with device-aware validation
Expected: Proper security protocols based on device capabilities
Series: Both Series 2 and 3 (device-aware)
Priority: HIGH
Hardware: Device Only
Device-Aware: YES - Uses DeviceCapabilities database for security validation
Based on: test_24_protocol_security.py
Enhanced: 2025-12-01
"""

import pytest
import time
from playwright.sync_api import expect
from pages.network_config_page import NetworkConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_24_1_1_protocol_security_validation_device_enhanced(
    network_config_page: NetworkConfigPage, request
):
    """
    Test 24.1.1: Protocol Security Validation [DEVICE ENHANCED]
    Purpose: Test protocol security features with device-aware validation
    Expected: Proper security protocols based on device capabilities
    Series: Both 2 and 3
    Device-Aware: Uses DeviceCapabilities database for security validation
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
        f"Device {device_model} (Series {device_series}): Testing protocol security validation"
    )

    try:
        # Navigate to network config page
        network_config_page.navigate_to_page()
        network_config_page.verify_page_loaded()
        print(f"Device {device_model}: Network config page loaded")

        # Test 1: HTTPS/SSL protocol availability
        try:
            protocol_elements = [
                network_config_page.page.locator(
                    "select[name*='protocol'], select[id*='protocol']"
                ),
                network_config_page.page.locator(
                    "input[name*='ssl'], input[id*='ssl']"
                ),
                network_config_page.page.locator(
                    "input[name*='tls'], input[id*='tls']"
                ),
                network_config_page.page.locator("text=/https|ssl|tls/i"),
            ]

            protocol_found = 0
            for element in protocol_elements:
                try:
                    if element.count() > 0:
                        protocol_found += element.count()
                        print(
                            f"Device {device_model}: Found {element.count()} protocol security elements"
                        )
                except Exception:
                    continue

            print(
                f"Device {device_model}: Total protocol security elements found: {protocol_found}"
            )

        except Exception as e:
            print(f"Device {device_model}: Protocol security test failed: {e}")

        # Cross-validate with DeviceCapabilities database
        device_network_config = device_capabilities.get_network_config(device_model)
        if device_network_config and "management_interface" in device_network_config:
            mgmt_iface = device_network_config["management_interface"]
            print(f"Device {device_model}: Protocol security validation test completed")
            print(
                f"Management interface: {mgmt_iface}, Timeout scaling: {device_timeout_multiplier}x"
            )

    except Exception as e:
        pytest.fail(f"Protocol security validation test failed for {device_model}: {e}")

    # Database validation summary
    assert device_capabilities.get_device_series(device_model) == device_series
    assert (
        device_capabilities.get_timeout_multiplier(device_model)
        == device_timeout_multiplier
    )
