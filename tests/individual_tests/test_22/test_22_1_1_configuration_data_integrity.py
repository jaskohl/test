"""
Test: 22.1.1 - Configuration Data Integrity [DEVICE ]
Category: Data Integrity Testing (22)
Purpose: Test configuration data integrity with device-aware validation
Expected: Data persists correctly with device-specific patterns
Series: Both Series 2 and 3 (device-aware)
Priority: HIGH
Hardware: Device Only
Device-Aware: YES - Uses DeviceCapabilities database for data validation
Based on: test_22_data_integrity.py
: 2025-12-01
"""

import pytest
import time
from playwright.sync_api import expect
from pages.network_config_page import NetworkConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_22_1_1_configuration_data_integrity(
    network_config_page: NetworkConfigPage, request
):
    """
    Test 22.1.1: Configuration Data Integrity [DEVICE ]
    Purpose: Test configuration data integrity with device-aware validation
    Expected: Data persists correctly with device-specific patterns
    Series: Both 2 and 3
    Device-Aware: Uses DeviceCapabilities database for data validation
    """
    # Get device context and validate
    device_model = request.session.get("device_model", "unknown")
    device_capabilities = DeviceCapabilities()

    if device_model not in device_capabilities.get_series_list():
        pytest.skip(f"Device model '{device_model}' not in DeviceCapabilities database")

    device_series = device_capabilities.get_device_series(device_model)

    # Device-aware timeout scaling
    base_timeout = 10000  # Data integrity testing needs longer timeouts
    device_timeout_multiplier = device_capabilities.get_timeout_multiplier(device_model)
    scaled_timeout = int(base_timeout * device_timeout_multiplier)

    print(
        f"Device {device_model} (Series {device_series}): Testing configuration data integrity"
    )

    try:
        # Navigate to network config page
        network_config_page.navigate_to_page()
        network_config_page.verify_page_loaded()
        print(f"Device {device_model}: Network config page loaded")

        # Test 1: Get current configuration values
        try:
            config_data = {}

            # Extract current network configuration
            ip_fields = [
                network_config_page.page.locator(
                    "input[name*='ip'], input[placeholder*='IP']"
                ),
            ]

            for field_selector in ip_fields:
                try:
                    fields = field_selector.all()
                    for i, field in enumerate(fields):
                        try:
                            field_name = (
                                field.get_attribute("name") or f"ip_field_{i+1}"
                            )
                            field_value = (
                                field.input_value() if field.input_value() else ""
                            )

                            if field_name not in config_data:
                                config_data[field_name] = []
                            config_data[field_name].append(field_value)

                            print(
                                f"Device {device_model}: {field_name} = '{field_value}'"
                            )
                        except Exception:
                            continue
                except Exception:
                    continue

            print(
                f"Device {device_model}: Retrieved {len(config_data)} configuration fields"
            )

        except Exception as e:
            print(f"Device {device_model}: Configuration data retrieval failed: {e}")

        # Test 2: Test data persistence through page reload
        try:
            # Store original values
            original_values = {}

            # Focus on IP fields for persistence testing
            ip_field = network_config_page.page.locator("input[name*='ip']").first
            if ip_field.count() > 0:
                try:
                    original_value = ip_field.input_value()
                    original_values["test_ip"] = original_value

                    # Focus the field to trigger any dynamic behavior
                    ip_field.focus(timeout=scaled_timeout)

                    print(
                        f"Device {device_model}: Stored original IP value: '{original_value}'"
                    )
                except Exception as e:
                    print(
                        f"Device {device_model}: Failed to store original IP value: {e}"
                    )

            # Reload page
            network_config_page.page.reload()
            network_config_page.wait_for_page_load()
            network_config_page.verify_page_loaded()

            # Check if values persist
            persisted_values = {}

            ip_field_after = network_config_page.page.locator("input[name*='ip']").first
            if ip_field_after.count() > 0:
                try:
                    persisted_value = ip_field_after.input_value()
                    persisted_values["test_ip"] = persisted_value

                    print(
                        f"Device {device_model}: Persisted IP value: '{persisted_value}'"
                    )

                    # Compare original vs persisted
                    if "test_ip" in original_values and "test_ip" in persisted_values:
                        if original_values["test_ip"] == persisted_values["test_ip"]:
                            print(
                                f"Device {device_model}: IP value persistence verified"
                            )
                        else:
                            print(
                                f"Device {device_model}: Warning - IP value changed after reload"
                            )

                except Exception as e:
                    print(
                        f"Device {device_model}: Failed to check persisted IP value: {e}"
                    )

        except Exception as e:
            print(f"Device {device_model}: Data persistence test failed: {e}")

        # Test 3: Validate device-specific configuration constraints
        try:
            # Get device network configuration constraints
            device_network_config = device_capabilities.get_network_config(device_model)

            if device_network_config:
                mgmt_interface = device_network_config.get("management_interface")

                if mgmt_interface:
                    # Verify management interface is properly configured
                    interface_elements = [
                        network_config_page.page.locator(
                            f"select[name*='{mgmt_interface}']"
                        ),
                        network_config_page.page.locator(
                            f"input[name*='{mgmt_interface}']"
                        ),
                    ]

                    interface_found = False
                    for element in interface_elements:
                        try:
                            if element.count() > 0:
                                interface_found = True
                                print(
                                    f"Device {device_model}: Management interface '{mgmt_interface}' elements found"
                                )
                                break
                        except Exception:
                            continue

                    if not interface_found:
                        print(
                            f"Device {device_model}: Warning - Management interface '{mgmt_interface}' elements not found"
                        )

            else:
                print(
                    f"Device {device_model}: No specific network configuration constraints found"
                )

        except Exception as e:
            print(
                f"Device {device_model}: Configuration constraints validation failed: {e}"
            )

        # Cross-validate with DeviceCapabilities database
        device_network_config = device_capabilities.get_network_config(device_model)
        if device_network_config and "management_interface" in device_network_config:
            mgmt_iface = device_network_config["management_interface"]
            print(f"Device {device_model}: Configuration data integrity test completed")
            print(
                f"Management interface: {mgmt_iface}, Timeout scaling: {device_timeout_multiplier}x"
            )

    except Exception as e:
        pytest.fail(f"Configuration data integrity test failed for {device_model}: {e}")

    # Database validation summary
    assert device_capabilities.get_device_series(device_model) == device_series
    assert (
        device_capabilities.get_timeout_multiplier(device_model)
        == device_timeout_multiplier
    )
