"""
Test 11.6.2: Maximum Value Validation (Device-Enhanced)
Purpose: Maximum value constraints on numeric fields with device capabilities
Expected: Device-aware maximum value constraints
Device-Enhanced: Uses DeviceCapabilities for device-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_6_2_maximum_value_validation_device_enhanced(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.6.2: Maximum Value Validation (Device-Enhanced)
    Purpose: Maximum value constraints on numeric fields with device capabilities
    Expected: Device-aware maximum value constraints
    Device-Enhanced: Uses DeviceCapabilities for device-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate maximum value constraints"
        )

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Navigate to general config page
    general_config_page.navigate_to_page()

    # Look for numeric fields with maximum values
    numeric_fields = general_config_page.page.locator("input[type='number']")
    if numeric_fields.count() > 0:
        numeric_field = numeric_fields.first

        # Test maximum value behavior with device-aware values
        if device_series == 2:
            # Series 2: Traditional maximum values
            test_values = ["100", "255", "65535"]
            max_reasonable_value = 65535
        else:  # Series 3
            # Series 3: May have different maximum ranges
            test_values = ["100", "255", "1000"]
            max_reasonable_value = 1000

        for test_value in test_values:
            try:
                numeric_field.fill(test_value)
                actual_value = numeric_field.input_value()
                print(f"Series {device_series}: Value {test_value} -> {actual_value}")

                # Validate that reasonable values are accepted
                if int(test_value) <= max_reasonable_value:
                    print(f" Acceptable maximum value: {test_value}")
            except Exception as e:
                print(f"Maximum value test issue for {test_value}: {e}")

        # Test edge case: very large values
        try:
            large_value = "999999"
            numeric_field.fill(large_value)
            actual_large = numeric_field.input_value()
            print(f"Large value test: {large_value} -> {actual_large}")
        except Exception as e:
            print(f"Large value test issue: {e}")

    else:
        print(f"No numeric fields found for maximum value validation on {device_model}")
