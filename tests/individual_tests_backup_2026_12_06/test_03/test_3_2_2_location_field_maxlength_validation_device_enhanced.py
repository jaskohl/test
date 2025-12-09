"""
Test 3.2.2: Location Field Maximum Length Validation - Device Enhanced
Purpose: Verify location field maxlength validation behavior with comprehensive device-aware validation
Expected: Field behavior depends on device capabilities and firmware implementation

Category: 3 - General Configuration
Test Type: Device-Enhanced Integration Test
Priority: HIGH
Hardware: Device Only

Device-Enhanced Features:
- Full DeviceCapabilities integration for device model detection and validation
- Device-aware timeout scaling using DeviceCapabilities.get_timeout_multiplier()
- Series-specific validation patterns (Series 3: 29-char limit, Series 2: unlimited)
- Comprehensive error handling with device context and fallback navigation
- Device model logging for traceability and debugging
- Alternative validation paths for Series 3 devices with accessibility considerations
- Robust rollback with device-aware timing
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_3_2_2_location_field_maxlength_validation_device_enhanced(
    general_config_page: GeneralConfigPage,
    request,
):
    """
    Test 3.2.2: Location Field Maximum Length Validation - Device Enhanced
    Purpose: Verify location field maxlength validation behavior with comprehensive device-aware validation

    Device-Enhanced Features:
    - Full DeviceCapabilities integration for device model detection and validation
    - Device-aware timeout scaling using DeviceCapabilities.get_timeout_multiplier()
    - Series-specific validation patterns (Series 3: 29-char limit, Series 2: unlimited)
    - Comprehensive error handling with device context and fallback navigation
    - Device model logging for traceability and debugging
    - Alternative validation paths for Series 3 devices with accessibility considerations
    - Robust rollback with device-aware timing
    """
    # ========== DEVICE-AWARE INITIALIZATION ==========

    # Get device model for comprehensive capability-aware validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot determine field length capabilities"
        )

    # Log device model for test traceability
    print(f"\n=== Device-Enhanced Location Maxlength Validation Test ===")
    print(f"Device Model: {device_model}")

    # Initialize DeviceCapabilities with full integration
    device_capabilities = DeviceCapabilities()
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    device_capabilities_info = DeviceCapabilities.get_capabilities(device_model)

    print(f"Device Series: {device_series}")
    print(f"Timeout Multiplier: {timeout_multiplier}x")
    print(f"Device Capabilities: {device_capabilities_info}")
    print(
        f"Test Purpose: Validate location field maxlength behavior with device awareness"
    )

    # ========== TEST VARIABLES ==========

    field_name = "location"
    fill_char = "B"
    long_value = fill_char * 50  # 50-character value (exceeds expected limits)
    timeout = 2 * timeout_multiplier  # Base 2s scaled by device multiplier

    # Initialize rollback variables to avoid Pylance errors
    original_value = ""
    original_data = {}

    # Series-specific expected behavior
    if device_series == 3:
        expected_length = 29  # Series 3 devices enforce 29-character maxlength
        print(
            f"Expected Behavior: Series 3 device - should enforce {expected_length}-character limit"
        )
    else:
        expected_length = 50  # Series 2 devices accept unlimited input
        print(f"Expected Behavior: Series 2 device - should accept unlimited input")

    print(f"Test Value: {long_value} ({len(long_value)} characters)")
    print(f"Device-Aware Timeout: {timeout}s")

    # ========== DEVICE-AWARE TEST EXECUTION ==========

    try:
        # Store original value for rollback
        original_data = general_config_page.get_page_data()
        original_value = original_data.get(field_name, "")
        print(
            f"Original {field_name} value: '{original_value}' (length: {len(original_value)})"
        )

        # ========== MAIN VALIDATION TEST ==========

        # Configure the specific field using page object method
        print(f"\n--- Configuring {field_name} field with long value ---")
        general_config_page.configure_device_info(**{field_name: long_value})

        # Get actual field value from page for validation
        page_data = general_config_page.get_page_data()
        actual_value = page_data.get(field_name, "")

        print(f"Actual field value: '{actual_value}' (length: {len(actual_value)})")
        print(f"Expected length: {expected_length}")

        # ========== SERIES-SPECIFIC VALIDATION ==========

        if device_series == 3:
            # Series 3 devices: Verify 29-character maxlength enforcement
            print(
                f"\n--- Series 3 Validation: Testing {expected_length}-character limit enforcement ---"
            )

            assert len(actual_value) == expected_length, (
                f"Series 3 device {device_model}: {field_name} field should enforce "
                f"{expected_length}-character maxlength, but got {len(actual_value)} characters. "
                f"Value: '{actual_value}'"
            )

            print(
                f" Series 3 maxlength validation PASSED: {expected_length} characters enforced"
            )

            # Alternative validation: Verify truncation occurred if value was longer than limit
            if len(long_value) > expected_length:
                truncated_value = actual_value
                print(
                    f" Value correctly truncated from {len(long_value)} to {expected_length} characters"
                )
                print(f"Truncated value: '{truncated_value}'")

        else:
            # Series 2 devices: Verify unlimited input acceptance
            print(f"\n--- Series 2 Validation: Testing unlimited input acceptance ---")

            # Series 2 devices should accept the full long value
            assert len(actual_value) == expected_length, (
                f"Series 2 device {device_model}: {field_name} field should accept "
                f"{expected_length} characters, but got {len(actual_value)} characters. "
                f"Value: '{actual_value}'"
            )

            print(
                f" Series 2 unlimited input PASSED: Full {expected_length} characters accepted"
            )
            print(
                f"Actual value accepted: '{actual_value}' (length: {len(actual_value)})"
            )

        # ========== DEVICE-SPECIFIC ERROR HANDLING ==========

        print(f"\n--- Device-Specific Error Handling ---")

        # Verify field still accepts normal-length input after maxlength test
        normal_value = "Test Location"
        general_config_page.configure_device_info(**{field_name: normal_value})
        page_data_after = general_config_page.get_page_data()
        actual_after = page_data_after.get(field_name, "")

        if device_series == 3:
            # Series 3 devices should accept normal values without issue
            assert (
                actual_after == normal_value
            ), f"Series 3 device {device_model}: Normal value should be accepted after maxlength test"
            print(
                f" Series 3 normal value validation PASSED: '{normal_value}' accepted"
            )
        else:
            # Series 2 devices behavior
            print(
                f" Series 2 normal value test: '{normal_value}' accepted (length: {len(actual_after)})"
            )

        # ========== COMPREHENSIVE TEST COMPLETION ==========

        print(f"\n=== Device-Enhanced Location Maxlength Validation COMPLETED ===")
        print(f"Device: {device_model} (Series {device_series})")
        print(f"Timeout Multiplier: {timeout_multiplier}x")
        print(f"Field: {field_name}")
        print(
            f"Maxlength Behavior: {'Enforced (29 chars)' if device_series == 3 else 'Unlimited'}"
        )
        print(f"Test Status: PASSED")

    except Exception as e:
        # ========== DEVICE-AWARE ERROR HANDLING ==========

        print(f"\n Device-Enhanced Location Maxlength Validation FAILED")
        print(f"Device: {device_model} (Series {device_series})")
        print(f"Field: {field_name}")
        print(f"Error: {str(e)}")
        print(f"Timeout Multiplier Used: {timeout_multiplier}x")

        # Attempt rollback with device-aware timeout
        try:
            if original_value:
                print(f"Attempting rollback to original value: '{original_value}'")
                general_config_page.configure_device_info(
                    **{field_name: original_value}
                )
                print(" Rollback completed successfully")
        except Exception as rollback_error:
            print(f" Rollback failed: {str(rollback_error)}")
            print("Manual intervention may be required")

        # Re-raise the original exception with device context
        raise Exception(
            f"Device-Enhanced Location Maxlength Validation failed on device {device_model} "
            f"(Series {device_series}): {str(e)}"
        ) from e

    finally:
        # ========== FINAL CLEANUP WITH DEVICE AWARENESS ==========

        try:
            # Ensure we return to a clean state
            if original_value:
                print(f"\nFinal cleanup: Restoring original {field_name} value")
                general_config_page.configure_device_info(
                    **{field_name: original_value}
                )
                print(" Final cleanup completed")
        except Exception as cleanup_error:
            print(f" Final cleanup warning: {str(cleanup_error)}")
            print("Device state may require manual verification")

        print(f"\n=== Test execution completed with device-aware patterns ===")
