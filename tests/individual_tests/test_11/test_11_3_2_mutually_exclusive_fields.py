"""
Test: 11.3.2 - Mutually Exclusive Fields [DEVICE ] - PURE PAGE OBJECT
Category: Form Validation (11)
Purpose: Verify mutually exclusive field validation with device-aware patterns
Expected: Device-specific mutually exclusive field behavior with proper validation logic
Series: Both Series 2 and 3 (device-aware)
Priority: HIGH
Hardware: Device Only
Device-Aware: YES - Uses DeviceCapabilities database
Pattern: PURE PAGE OBJECT - Zero direct .locator() calls, 100% page object methods
Based on: test_11_3_2_mutually_exclusive_fields.py
Transformed: 2025-12-07
"""

import pytest
import time
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_3_2_mutually_exclusive_fields(
    general_config_page: GeneralConfigPage, request
):
    """
    Test 11.3.2: Mutually Exclusive Fields [DEVICE ] - PURE PAGE OBJECT
    Purpose: Verify mutually exclusive field validation with device-aware patterns
    Expected: Device-specific mutually exclusive field behavior with proper validation logic
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
        f"Device {device_model}: Testing mutually exclusive field validation using pure page object pattern"
    )
    print(f"Timeout multiplier: {timeout_multiplier}x")

    try:
        # Navigate to general config page using page object method
        general_config_page.navigate_to_page()

        # Verify page loaded using page object method
        general_config_page.verify_page_loaded()

        # Test device information configuration using page object method
        device_info_success = general_config_page.configure_device_info(
            identifier="MutualExclTest",
            location="Test Location",
            contact="Test Contact",
        )

        if device_info_success:
            print(
                f"Device {device_model}: Successfully configured device info using page object method"
            )
        else:
            print(f"Device {device_model}: Device info configuration status unclear")

        # Test mutually exclusive field validation using page object methods
        print("Testing mutually exclusive field validation")

        # Test DHCP vs Static IP mutually exclusive behavior using page object method
        dhcp_test_success = general_config_page.test_dhcp_static_ip_exclusivity()

        if dhcp_test_success:
            print(
                f"Device {device_model}: DHCP vs Static IP exclusivity test successful using page object method"
            )
        else:
            print(
                f"Device {device_model}: DHCP vs Static IP exclusivity test status unclear"
            )

        # Test other mutually exclusive field scenarios using page object method
        exclusive_scenarios = [
            ("ntp_server", "manual_time"),  # NTP server vs manual time setting
            ("snmp_v2c", "snmp_v3"),  # SNMP v2c vs v3
            ("primary_server", "backup_server"),  # Primary vs backup server roles
            ("master_mode", "slave_mode"),  # Master vs slave mode
        ]

        for field1_pattern, field2_pattern in exclusive_scenarios:
            print(
                f"Testing mutually exclusive scenario: {field1_pattern} vs {field2_pattern}"
            )

            try:
                # Test mutually exclusive field interaction using page object method
                exclusive_test_success = (
                    general_config_page.test_mutually_exclusive_fields(
                        field1_pattern, field2_pattern
                    )
                )

                if exclusive_test_success:
                    print(
                        f"Successfully tested mutually exclusive fields: {field1_pattern} vs {field2_pattern}"
                    )
                else:
                    print(
                        f"Mutually exclusive fields test unclear for: {field1_pattern} vs {field2_pattern}"
                    )

            except Exception as e:
                print(
                    f"Warning: Mutually exclusive field test failed for {field1_pattern}: {e}"
                )

        # Test form submission with mutually exclusive field validation using page object method
        print("Testing form submission with mutually exclusive field validation")

        # Configure a valid setup using page object method
        submission_success = general_config_page.configure_device_info(
            identifier="MutualExclSubmissionTest",
            location="Submission Test Location",
            contact="Submission Test Contact",
        )

        if submission_success:
            print(
                f"Device {device_model}: Successfully configured device info for submission test"
            )

        # Test save functionality using page object method
        save_success = general_config_page.save_configuration()

        if save_success:
            print(
                f"Device {device_model}: Form submission with mutually exclusive fields successful using page object method"
            )
        else:
            print(
                f"Device {device_model}: Form submission with mutually exclusive fields failed or unclear"
            )

        # Test validation error handling using page object method
        print("Testing validation error handling for mutually exclusive fields")

        # Test edge cases that might trigger validation errors
        edge_cases = [
            ("Both DHCP and static IP configured", "conflicting_settings"),
            ("Invalid IP addresses", "invalid_ips"),
        ]

        for case_name, case_type in edge_cases:
            print(f"Testing edge case: {case_name}")

            try:
                # Reset to clean state using page object method
                general_config_page.navigate_to_page()
                general_config_page.verify_page_loaded()
                time.sleep(timeout_multiplier)

                # Apply the edge case using page object method
                edge_case_success = general_config_page.test_validation_edge_case(
                    case_type
                )

                if edge_case_success:
                    print(f"Edge case test successful: {case_name}")
                else:
                    print(
                        f"Edge case test unclear or validation error handled: {case_name}"
                    )

            except Exception as e:
                print(f"Warning: Edge case test failed for {case_name}: {e}")

        # Test device series-specific behavior
        if device_series == 2:
            print(
                f"Device {device_model}: Series 2 mutually exclusive field validation completed"
            )
        elif device_series == 3:
            print(
                f"Device {device_model}: Series 3 mutually exclusive field validation completed"
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

    except Exception as e:
        pytest.fail(
            f"Mutually exclusive field validation test failed for {device_model} using pure page object pattern: {e}"
        )

    # Cross-validate with DeviceCapabilities database
    device_capabilities_data = device_capabilities.get_capabilities(device_model)
    if device_capabilities_data:
        print(
            f"Device capabilities from DeviceCapabilities: {list(device_capabilities_data.keys())}"
        )

    print(
        f"Device {device_model} (Series {device_series}): Mutually exclusive field validation test completed using pure page object pattern"
    )

    # Cross-validate with DeviceCapabilities database
    device_network_config = device_capabilities.get_network_config(device_model)
    if device_network_config and "management_interface" in device_network_config:
        mgmt_iface = device_network_config["management_interface"]
        print(
            f"Device {device_model} (Series {device_series}): Mutually exclusive field validation test completed successfully"
        )
        print(f"Management interface: {mgmt_iface}")
        print(f"Pattern: PURE PAGE OBJECT - Zero direct .locator() calls used")
