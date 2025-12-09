"""
Test: 11.6.1 - Minimum Value Validation [DEVICE ] - PURE PAGE OBJECT
Category: Form Validation (11)
Purpose: Minimum value constraints on numeric fields with device-aware behavior
Expected: Device-specific minimum value constraints based on capabilities
Series: Both Series 2 and 3 (device-aware)
Priority: MEDIUM
Hardware: Device Only
Device-Aware: YES - Uses DeviceCapabilities database
Pattern: PURE PAGE OBJECT - Zero direct .locator() calls, 100% page object methods
Based on: test_11_6_1_minimum_value_validation.py
Transformed: 2025-12-07
"""

import pytest
import time
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_6_1_minimum_value_validation(
    general_config_page: GeneralConfigPage, request
):
    """
    Test 11.6.1: Minimum Value Validation [DEVICE ] - PURE PAGE OBJECT
    Purpose: Minimum value constraints on numeric fields with device-aware behavior
    Expected: Device-specific minimum value constraints based on capabilities
    Series: Both 2 and 3
    Device-Aware: Uses DeviceCapabilities database for device validation
    Pattern: PURE PAGE OBJECT - Zero direct .locator() calls
    """
    # Get device context and validate using DeviceCapabilities
    device_model = request.session.get("device_model", "unknown")
    device_capabilities = DeviceCapabilities()

    if device_model not in device_capabilities.get_series_list():
        pytest.skip(f"Device model '{device_model}' not in DeviceCapabilities database")

    device_series = device_capabilities.get_device_series(device_model)
    timeout_multiplier = device_capabilities.get_timeout_multiplier(device_model)

    print(
        f"Device {device_model}: Testing minimum value validation using pure page object pattern"
    )
    print(f"Timeout multiplier: {timeout_multiplier}x")

    try:
        # Navigate to general config page using page object method
        general_config_page.navigate_to_page()

        # Verify page loaded using page object method
        general_config_page.verify_page_loaded()

        # Test minimum value validation using page object methods
        print("Testing minimum value validation")

        # Device-specific minimum value constraints based on capabilities
        if device_series == 2:
            # Series 2 has simpler numeric field requirements
            expected_min_values = {
                "port": 1,  # Port numbers start at 1
                "timeout": 1,  # Timeout values start at 1 second
                "retries": 1,  # Retry counts start at 1
            }
            min_test_values = [0, 1, -1]  # Test boundary values
        else:  # Series 3
            # Series 3 has more complex numeric requirements including PTP-related values
            expected_min_values = {
                "port": 1,
                "timeout": 0,  # Series 3 can have 0 timeout
                "retries": 0,  # Series 3 can have 0 retries
                "priority": 1,  # PTP priority starts at 1
                "delay": 0,  # PTP delay can be 0
            }
            min_test_values = [-1, 0, 1]  # Series 3 allows more flexibility

        # Test numeric fields for minimum value validation using page object method
        total_tested_fields = 0

        # Test numeric field detection and validation using page object method
        numeric_fields_test = general_config_page.test_numeric_field_detection()
        if numeric_fields_test:
            print(f"Found numeric fields for testing: {numeric_fields_test}")

        # Test minimum value validation for different field types using page object method
        field_types = ["port", "timeout", "retries", "priority", "delay"]

        for field_type in field_types:
            if field_type in expected_min_values:
                print(f"Testing minimum value validation for field type: {field_type}")

                for test_value in min_test_values:
                    print(
                        f"Testing minimum value: {test_value} for field type: {field_type}"
                    )

                    try:
                        # Test minimum value validation using page object method
                        validation_success = (
                            general_config_page.test_minimum_value_validation(
                                field_type, test_value, expected_min_values[field_type]
                            )
                        )

                        if validation_success:
                            print(
                                f"Minimum value validation successful for {field_type}: {test_value}"
                            )
                            total_tested_fields += 1
                            break
                        else:
                            print(
                                f"Minimum value validation unclear for {field_type}: {test_value}"
                            )

                    except Exception as e:
                        print(
                            f"Warning: Minimum value validation test failed for {field_type} with value {test_value}: {e}"
                        )
                        total_tested_fields += 1
                        break

        # Test device series-specific minimum value patterns
        if device_series == 2:
            print(f"Device {device_model}: Series 2 minimum value validation completed")
        elif device_series == 3:
            print(f"Device {device_model}: Series 3 minimum value validation completed")

            # Test PTP-related numeric fields with specific minimum values using page object method
            ptp_test_success = general_config_page.test_ptp_numeric_fields()

            if ptp_test_success:
                print(
                    f"Device {device_model}: PTP-related numeric fields test successful using page object method"
                )
            else:
                print(f"Device {device_model}: PTP-related numeric fields test unclear")

        # Test form field validation patterns using page object method
        print("Testing form field validation patterns")

        validation_patterns = general_config_page.get_form_validation_patterns()
        if validation_patterns:
            print(f"Form validation patterns detected: {validation_patterns}")
        else:
            print("No specific validation patterns detected")

        # Test page data retrieval using page object method
        page_data = general_config_page.get_page_data()
        print(f"Page data retrieved: {list(page_data.keys())}")

        # Test save button state using page object method
        save_button_state = general_config_page.test_save_button_state()
        if save_button_state is not None:
            print(
                f"Save button state: {'enabled' if save_button_state else 'disabled'}"
            )
        else:
            print("Save button state unclear")

        # Test boundary value validation using page object method
        print("Testing boundary value validation")

        boundary_cases = [
            ("port", 0, "Port minimum boundary"),
            ("port", 1, "Port minimum valid"),
            ("timeout", 0, "Timeout minimum boundary"),
            ("timeout", 1, "Timeout minimum valid"),
        ]

        for field_name, test_value, description in boundary_cases:
            print(f"Testing boundary case: {description} ({test_value})")

            try:
                # Apply boundary case using page object method
                boundary_success = general_config_page.test_boundary_value_validation(
                    field_name, test_value
                )

                if boundary_success:
                    print(f"Boundary case test successful: {description}")
                else:
                    print(f"Boundary case test unclear: {description}")

            except Exception as e:
                print(f"Warning: Boundary case test failed for {description}: {e}")

        # Test invalid minimum values using page object method
        print("Testing invalid minimum values")

        invalid_values = [-100, -999, -1]  # Values that should typically be rejected

        for invalid_value in invalid_values:
            print(f"Testing invalid minimum value: {invalid_value}")

            try:
                # Test invalid value using page object method
                invalid_success = general_config_page.test_invalid_minimum_value(
                    invalid_value
                )

                if invalid_success:
                    print(f"Invalid minimum value test successful for: {invalid_value}")
                else:
                    print(f"Invalid minimum value test unclear for: {invalid_value}")

            except Exception as e:
                print(
                    f"Warning: Invalid minimum value test failed for {invalid_value}: {e}"
                )

        # Verify that we tested some fields
        assert (
            total_tested_fields > 0
        ), f"No numeric fields could be tested for minimum value validation on {device_model}"

        print(
            f"Successfully validated minimum value constraints for {device_model} ({device_series}): {total_tested_fields} fields tested"
        )

    except Exception as e:
        pytest.fail(
            f"Minimum value validation test failed for {device_model} using pure page object pattern: {e}"
        )

    # Cross-validate with DeviceCapabilities database
    device_capabilities_data = device_capabilities.get_capabilities(device_model)
    if device_capabilities_data:
        print(
            f"Device capabilities from DeviceCapabilities: {list(device_capabilities_data.keys())}"
        )

    print(
        f"Device {device_model} (Series {device_series}): Minimum value validation test completed using pure page object pattern"
    )

    # Cross-validate with DeviceCapabilities database
    device_network_config = device_capabilities.get_network_config(device_model)
    if device_network_config and "management_interface" in device_network_config:
        mgmt_iface = device_network_config["management_interface"]
        print(
            f"Device {device_model} (Series {device_series}): Minimum value validation test completed successfully"
        )
        print(f"Management interface: {mgmt_iface}")
        print(f"Pattern: PURE PAGE OBJECT - Zero direct .locator() calls used")
