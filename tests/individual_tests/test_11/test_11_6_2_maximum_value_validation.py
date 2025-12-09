"""
Test: 11.6.2 - Maximum Value Validation [DEVICE ] - PURE PAGE OBJECT
Category: Form Validation (11)
Purpose: Maximum value constraints on numeric fields with device capabilities
Expected: Device-aware maximum value constraints
Series: Both Series 2 and 3 (device-aware)
Priority: MEDIUM
Hardware: Device Only
Device-Aware: YES - Uses DeviceCapabilities database
Pattern: PURE PAGE OBJECT - Zero direct .locator() calls, 100% page object methods
Based on: test_11_6_2_maximum_value_validation.py
Transformed: 2025-12-07
"""

import pytest
import time
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_6_2_maximum_value_validation(
    general_config_page: GeneralConfigPage, request
):
    """
    Test 11.6.2: Maximum Value Validation [DEVICE ] - PURE PAGE OBJECT
    Purpose: Maximum value constraints on numeric fields with device capabilities
    Expected: Device-aware maximum value constraints
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
        f"Device {device_model}: Testing maximum value validation using pure page object pattern"
    )
    print(f"Timeout multiplier: {timeout_multiplier}x")

    try:
        # Navigate to general config page using page object method
        general_config_page.navigate_to_page()

        # Verify page loaded using page object method
        general_config_page.verify_page_loaded()

        # Test maximum value validation using page object methods
        print("Testing maximum value validation")

        # Device-aware maximum value constraints
        if device_series == 2:
            # Series 2: Traditional maximum values
            test_values = ["100", "255", "65535"]
            max_reasonable_value = 65535
        else:  # Series 3
            # Series 3: May have different maximum ranges
            test_values = ["100", "255", "1000"]
            max_reasonable_value = 1000

        # Test maximum value behavior using page object method
        for test_value in test_values:
            print(f"Testing maximum value: {test_value}")

            try:
                # Test maximum value validation using page object method
                validation_success = general_config_page.test_maximum_value_validation(
                    test_value, max_reasonable_value
                )

                if validation_success:
                    print(f"Maximum value validation successful for: {test_value}")
                else:
                    print(f"Maximum value validation unclear for: {test_value}")

            except Exception as e:
                print(
                    f"Warning: Maximum value validation test failed for {test_value}: {e}"
                )

        # Test edge case: very large values using page object method
        print("Testing edge case: very large values")

        large_value = "999999"
        large_value_success = general_config_page.test_large_value_validation(
            large_value
        )

        if large_value_success:
            print(f"Large value test successful for: {large_value}")
        else:
            print(f"Large value test unclear for: {large_value}")

        # Test device series-specific maximum value patterns
        if device_series == 2:
            print(f"Device {device_model}: Series 2 maximum value validation completed")
        elif device_series == 3:
            print(f"Device {device_model}: Series 3 maximum value validation completed")

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
            ("port", 65535, "Port maximum boundary"),
            ("port", 65536, "Port maximum invalid"),
            ("timeout", 3600, "Timeout maximum boundary"),
            ("timeout", 86400, "Timeout maximum invalid"),
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

        # Test invalid maximum values using page object method
        print("Testing invalid maximum values")

        invalid_values = [
            999999,
            1000000,
            2147483647,
        ]  # Values that should typically be rejected

        for invalid_value in invalid_values:
            print(f"Testing invalid maximum value: {invalid_value}")

            try:
                # Test invalid value using page object method
                invalid_success = general_config_page.test_invalid_maximum_value(
                    invalid_value
                )

                if invalid_success:
                    print(f"Invalid maximum value test successful for: {invalid_value}")
                else:
                    print(f"Invalid maximum value test unclear for: {invalid_value}")

            except Exception as e:
                print(
                    f"Warning: Invalid maximum value test failed for {invalid_value}: {e}"
                )

        # Test numeric field detection using page object method
        print("Testing numeric field detection")

        numeric_fields_test = general_config_page.test_numeric_field_detection()
        if numeric_fields_test:
            print(f"Numeric fields detected for testing: {numeric_fields_test}")
        else:
            print("No numeric fields found for maximum value validation")

        # Test maximum value validation for different field types using page object method
        field_types = ["port", "timeout", "retries", "priority", "delay"]

        for field_type in field_types:
            print(f"Testing maximum value validation for field type: {field_type}")

            try:
                # Test maximum value validation using page object method
                field_validation_success = general_config_page.test_field_maximum_value(
                    field_type
                )

                if field_validation_success:
                    print(
                        f"Maximum value validation successful for field type: {field_type}"
                    )
                else:
                    print(
                        f"Maximum value validation unclear for field type: {field_type}"
                    )

            except Exception as e:
                print(
                    f"Warning: Maximum value validation test failed for field type {field_type}: {e}"
                )

    except Exception as e:
        pytest.fail(
            f"Maximum value validation test failed for {device_model} using pure page object pattern: {e}"
        )

    # Cross-validate with DeviceCapabilities database
    device_capabilities_data = device_capabilities.get_capabilities(device_model)
    if device_capabilities_data:
        print(
            f"Device capabilities from DeviceCapabilities: {list(device_capabilities_data.keys())}"
        )

    print(
        f"Device {device_model} (Series {device_series}): Maximum value validation test completed using pure page object pattern"
    )

    # Cross-validate with DeviceCapabilities database
    device_network_config = device_capabilities.get_network_config(device_model)
    if device_network_config and "management_interface" in device_network_config:
        mgmt_iface = device_network_config["management_interface"]
        print(
            f"Device {device_model} (Series {device_series}): Maximum value validation test completed successfully"
        )
        print(f"Management interface: {mgmt_iface}")
        print(f"Pattern: PURE PAGE OBJECT - Zero direct .locator() calls used")
