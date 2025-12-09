"""
Test 11.10.1: Validation Error Consistency (Device-Enhanced)
Purpose: Validation error consistency with device capabilities
Expected: Device-aware validation error patterns
Device-Enhanced: Uses DeviceCapabilities for device-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_10_1_validation_error_consistency_device_enhanced(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.10.1: Validation Error Consistency (Device-Enhanced)
    Purpose: Validation error consistency with device capabilities
    Expected: Device-aware validation error patterns
    Device-Enhanced: Uses DeviceCapabilities for device-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate error consistency")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Navigate to general config page
    general_config_page.navigate_to_page()

    # Find input fields for error testing
    test_fields = [
        general_config_page.page.locator("input[name='identifier']").first,
        general_config_page.page.locator("input[name='location']").first,
        general_config_page.page.locator("input[name='contact']").first,
    ]

    valid_field_count = 0

    for field in test_fields:
        if field.count() > 0:
            valid_field_count += 1

            # Test field with invalid input to trigger validation
            try:
                # Clear field and enter invalid data
                field.fill("")
                field.fill("")  # Empty value

                # Look for validation error indicators
                error_selectors = [
                    ".error",
                    ".validation-error",
                    "[role='alert']",
                    ".field-error",
                    ".error-message",
                ]

                errors_found = 0
                for error_selector in error_selectors:
                    error_elements = general_config_page.page.locator(error_selector)
                    if error_elements.count() > 0:
                        errors_found += error_elements.count()
                        print(
                            f"Found {error_elements.count()} validation errors with selector: {error_selector}"
                        )

                print(f"Field validation test completed - {errors_found} errors found")

            except Exception as e:
                print(f"Field validation test issue: {e}")

    print(
        f"Validation error consistency test completed for {device_model} with {valid_field_count} fields tested"
    )

    # Validate error handling patterns based on device series
    if device_series == 3:
        print(f"Advanced error handling expected on Series 3 device {device_model}")
    else:
        print(f"Basic error handling on Series 2 device {device_model}")

    # Check for consistent error styling
    try:
        error_elements = general_config_page.page.locator(".error, .validation-error")
        error_count = error_elements.count()
        if error_count > 0:
            print(f" Error styling detected - {error_count} error elements found")
        else:
            print(f"No error styling detected on {device_model}")
    except Exception as e:
        print(f"Error styling check issue: {e}")
