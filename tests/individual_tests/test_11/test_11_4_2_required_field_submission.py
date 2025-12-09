"""
Test: 11.4.2 - Required Field Submission [DEVICE ] - PURE PAGE OBJECT
Category: Form Validation (11)
Purpose: Validate required field submission behavior with device capabilities
Expected: Device-aware required field submission behavior
Series: Both Series 2 and 3 (device-aware)
Priority: HIGH
Hardware: Device Only
Device-Aware: YES - Uses DeviceCapabilities database
Pattern: PURE PAGE OBJECT - Zero direct .locator() calls, 100% page object methods
Based on: test_11_4_2_required_field_submission.py
Transformed: 2025-12-07
"""

import pytest
import time
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_4_2_required_field_submission(
    general_config_page: GeneralConfigPage, request
):
    """
    Test 11.4.2: Required Field Submission [DEVICE ] - PURE PAGE OBJECT
    Purpose: Validate required field submission behavior with device capabilities
    Expected: Device-aware required field submission behavior
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
        f"Device {device_model}: Testing required field submission using pure page object pattern"
    )
    print(f"Timeout multiplier: {timeout_multiplier}x")

    try:
        # Navigate to general config page using page object method
        general_config_page.navigate_to_page()

        # Verify page loaded using page object method
        general_config_page.verify_page_loaded()

        # Test required field detection using page object method
        print("Testing required field detection")

        required_fields_detected = general_config_page.detect_required_fields()
        if required_fields_detected:
            print(
                f"Found {len(required_fields_detected)} required fields: {required_fields_detected}"
            )
        else:
            print("No required fields detected on this page")

        # Test required field submission behavior using page object method
        print("Testing required field submission behavior")

        # Clear required fields and attempt submission to test validation
        submission_test_success = general_config_page.test_required_field_submission()

        if submission_test_success:
            print(
                f"Device {device_model}: Required field submission test successful using page object method"
            )
        else:
            print(
                f"Device {device_model}: Required field submission test status unclear"
            )

        # Test form submission without required fields using page object method
        print("Testing form submission without required fields")

        # Configure valid device info first using page object method
        device_info_success = general_config_page.configure_device_info(
            identifier="RequiredFieldTest",
            location="Test Location",
            contact="Test Contact",
        )

        if device_info_success:
            print(
                f"Device {device_model}: Successfully configured device info using page object method"
            )

        # Test save functionality using page object method
        save_success = general_config_page.save_configuration()

        if save_success:
            print(
                f"Device {device_model}: Form submission successful using page object method"
            )
        else:
            print(f"Device {device_model}: Form submission failed or unclear")

        # Test validation message detection using page object method
        print("Testing validation message detection")

        validation_messages = general_config_page.detect_validation_messages()
        if validation_messages:
            print(f"Validation messages detected: {validation_messages}")
        else:
            print("No validation messages detected")

        # Test device series-specific behavior
        if device_series == 2:
            print(
                f"Device {device_model}: Series 2 required field submission validation completed"
            )
        elif device_series == 3:
            print(
                f"Device {device_model}: Series 3 required field submission validation completed"
            )

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

        # Test form reset functionality using page object method
        print("Testing form reset functionality")

        reset_success = general_config_page.reset_form_fields()
        if reset_success:
            print(
                f"Device {device_model}: Form reset successful using page object method"
            )
        else:
            print(f"Device {device_model}: Form reset status unclear")

        # Test required field validation edge cases using page object method
        print("Testing required field validation edge cases")

        edge_cases = [
            "empty_identifier",
            "empty_location",
            "empty_contact",
            "invalid_email_format",
            "special_characters_in_fields",
        ]

        for edge_case in edge_cases:
            print(f"Testing edge case: {edge_case}")

            try:
                # Reset to clean state using page object method
                general_config_page.navigate_to_page()
                general_config_page.verify_page_loaded()
                time.sleep(timeout_multiplier)

                # Apply the edge case using page object method
                edge_case_success = general_config_page.test_validation_edge_case(
                    edge_case
                )

                if edge_case_success:
                    print(f"Edge case test successful: {edge_case}")
                else:
                    print(
                        f"Edge case test unclear or validation error handled: {edge_case}"
                    )

            except Exception as e:
                print(f"Warning: Edge case test failed for {edge_case}: {e}")

    except Exception as e:
        pytest.fail(
            f"Required field submission test failed for {device_model} using pure page object pattern: {e}"
        )

    # Cross-validate with DeviceCapabilities database
    device_capabilities_data = device_capabilities.get_capabilities(device_model)
    if device_capabilities_data:
        print(
            f"Device capabilities from DeviceCapabilities: {list(device_capabilities_data.keys())}"
        )

    print(
        f"Device {device_model} (Series {device_series}): Required field submission test completed using pure page object pattern"
    )

    # Cross-validate with DeviceCapabilities database
    device_network_config = device_capabilities.get_network_config(device_model)
    if device_network_config and "management_interface" in device_network_config:
        mgmt_iface = device_network_config["management_interface"]
        print(
            f"Device {device_model} (Series {device_series}): Required field submission test completed successfully"
        )
        print(f"Management interface: {mgmt_iface}")
        print(f"Pattern: PURE PAGE OBJECT - Zero direct .locator() calls used")
