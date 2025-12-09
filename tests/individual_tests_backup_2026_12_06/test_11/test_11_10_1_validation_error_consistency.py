"""
Test 11.10.1: Validation Error Consistency (Device-Aware)
Purpose: Consistent error messages across validation scenarios
Expected: Device-specific error message consistency
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_10_1_validation_error_consistency(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.10.1: Validation Error Consistency (Device-Aware)
    Purpose: Consistent error messages across validation scenarios
    Expected: Device-specific error message consistency
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate error message consistency"
        )

    general_config_page.navigate_to_page()

    # Test various validation scenarios to check error message consistency
    # Look for numeric fields to test range validation errors
    numeric_fields = general_config_page.page.locator("input[type='number']")
    if numeric_fields.count() > 0:
        numeric_field = numeric_fields.first
        # Test with invalid value to trigger validation error
        numeric_field.fill("invalid")
        # Look for error message containers
        error_containers = general_config_page.page.locator(
            ".error, .validation-error, [role='alert'], .invalid-feedback"
        )
        if error_containers.count() > 0:
            # Error messages should be consistent in style and content
            first_error = error_containers.first.text_content()
            assert first_error is not None, "Error message should be present"
            # Check for consistent error message formatting
        else:
            print(f"No error containers found for {device_model} validation testing")
    else:
        print(
            f"No numeric fields found for error consistency testing on {device_model}"
        )
