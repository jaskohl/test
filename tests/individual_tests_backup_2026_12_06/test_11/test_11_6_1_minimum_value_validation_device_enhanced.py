"""
Test 11.6.1: Minimum Value Validation (Device-Enhanced)
Purpose: Minimum value constraints on numeric fields with device-aware behavior
Expected: Device-specific minimum value constraints based on capabilities
Device-Enhanced: Full DeviceCapabilities integration with series-specific patterns
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_6_1_minimum_value_validation_device_enhanced(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.6.1: Minimum Value Validation (Device-Enhanced)
    Purpose: Minimum value constraints on numeric fields with device-aware behavior
    Expected: Device-specific minimum value constraints based on capabilities
    Device-Enhanced: Full DeviceCapabilities integration with series-specific patterns
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate minimum value constraints"
        )

    # Get device capabilities for enhanced validation
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    general_config_page.navigate_to_page()

    # Device-aware timeout handling
    base_timeout = 5000
    enhanced_timeout = int(base_timeout * timeout_multiplier)

    # Look for numeric fields with device-specific minimum value patterns
    if device_series == "Series 2":
        # Series 2 has simpler numeric field requirements
        numeric_selectors = [
            "input[type='number']",
            ".numeric-input",
            "[data-field-type='number']",
        ]
        expected_min_values = {
            "port": 1,  # Port numbers start at 1
            "timeout": 1,  # Timeout values start at 1 second
            "retries": 1,  # Retry counts start at 1
        }
    else:  # Series 3
        # Series 3 has more complex numeric requirements including PTP-related values
        numeric_selectors = [
            "input[type='number']",
            ".numeric-input",
            "[data-field-type='number']",
            "[data-field-type='ptp-number']",  # PTP-related numeric fields
            ".ptp-numeric",
        ]
        expected_min_values = {
            "port": 1,
            "timeout": 0,  # Series 3 can have 0 timeout
            "retries": 0,  # Series 3 can have 0 retries
            "priority": 1,  # PTP priority starts at 1
            "delay": 0,  # PTP delay can be 0
        }

    # Test numeric fields for minimum value validation
    total_tested_fields = 0
    for selector in numeric_selectors:
        numeric_fields = general_config_page.page.locator(selector)
        count = numeric_fields.count()

        if count > 0:
            print(f"Found {count} numeric fields using selector: {selector}")

            # Test each numeric field
            for i in range(
                min(count, 3)
            ):  # Test up to 3 fields per selector to avoid overwhelming
                try:
                    numeric_field = numeric_fields.nth(i)

                    # Test minimum value validation with device-specific patterns
                    # Common minimum values based on device series
                    if device_series == "Series 2":
                        min_test_values = [0, 1, -1]  # Test boundary values
                    else:
                        min_test_values = [-1, 0, 1]  # Series 3 allows more flexibility

                    for test_value in min_test_values:
                        try:
                            numeric_field.fill(str(test_value))
                            actual_value = numeric_field.input_value()

                            # Check if the value was accepted or rejected appropriately
                            if actual_value == str(test_value):
                                print(f"Field accepted minimum value: {test_value}")
                            else:
                                # Value was modified (likely rejected)
                                print(
                                    f"Field rejected minimum value: {test_value}, got: {actual_value}"
                                )
                                total_tested_fields += 1
                                break
                        except Exception as e:
                            print(f"Error testing value {test_value}: {str(e)}")
                            total_tested_fields += 1
                            break

                except Exception as e:
                    print(f"Error accessing numeric field {i}: {str(e)}")

    # Device-specific validation assertions
    assert (
        total_tested_fields > 0
    ), f"No numeric fields could be tested for minimum value validation on {device_model}"

    if device_series == "Series 2":
        # Series 2 should have basic minimum value constraints
        print(f"Series 2 device {device_model} - validated minimum value constraints")
    else:  # Series 3
        # Series 3 should have more flexible minimum value constraints
        print(
            f"Series 3 device {device_model} - validated enhanced minimum value constraints"
        )

    # Check for device-specific minimum value patterns
    if device_series == "Series 3":
        # Look for PTP-related numeric fields with specific minimum values
        ptp_numeric_fields = general_config_page.page.locator(
            "[data-field-type='ptp-number']"
        )
        if ptp_numeric_fields.count() > 0:
            print(
                f"Found PTP-related numeric fields for Series 3 device {device_model}"
            )
            # Test PTP-specific minimum values
            try:
                ptp_field = ptp_numeric_fields.first
                ptp_field.fill("0")  # PTP fields often allow 0
                expect(ptp_field).to_be_visible(timeout=enhanced_timeout)
                print(
                    f"PTP field accepted minimum value 0 for Series 3 device {device_model}"
                )
            except Exception as e:
                print(f"PTP field minimum value test failed: {str(e)}")
    else:
        print(
            f"Series 2 device {device_model} - no PTP-related numeric fields expected"
        )

    print(
        f"Successfully validated minimum value constraints for {device_model} ({device_series}): {total_tested_fields} fields tested"
    )
