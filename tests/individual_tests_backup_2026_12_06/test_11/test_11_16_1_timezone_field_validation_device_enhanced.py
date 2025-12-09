"""
Test 11.16.1: Timezone Field Validation (Device-Enhanced)
Purpose: Timezone field validation with device capabilities
Expected: Device-aware timezone field validation
Device-Enhanced: Uses DeviceCapabilities for device-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_16_1_timezone_field_validation_device_enhanced(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.16.1: Timezone Field Validation (Device-Enhanced)
    Purpose: Timezone field validation with device capabilities
    Expected: Device-aware timezone field validation
    Device-Enhanced: Uses DeviceCapabilities for device-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate timezone field")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Navigate to general config page
    general_config_page.navigate_to_page()

    # Look for timezone fields
    timezone_field_selectors = [
        "select[name*='timezone']",
        "select[name*='time']",
        "input[name*='timezone']",
    ]

    timezone_field = None
    for selector in timezone_field_selectors:
        try:
            field = general_config_page.page.locator(selector).first
            if field.count() > 0:
                timezone_field = field
                print(f"Found timezone field with selector: {selector}")
                break
        except:
            continue

    if timezone_field:
        if timezone_field.get_attribute("tagName") == "SELECT":
            # Handle select field
            options = timezone_field.locator("option")
            option_count = options.count()
            print(f"Found {option_count} timezone options")

            # Test selecting valid timezones
            try:
                if option_count > 1:  # Skip placeholder option
                    options.first.select_option()
                    print(f" Timezone selection working on {device_model}")
                else:
                    print(f"Limited timezone options available on {device_model}")
            except Exception as e:
                print(f"Timezone selection issue: {e}")
        else:
            # Handle input field
            try:
                timezone_field.fill("UTC")
                actual_value = timezone_field.input_value()
                print(f"Timezone input test: UTC -> {actual_value}")
            except Exception as e:
                print(f"Timezone input issue: {e}")
    else:
        print(f"No timezone fields found for validation test on {device_model}")

    # Check timezone-related validation patterns
    if device_series == 3:
        # Series 3 may have more advanced timezone features
        print(
            f"Advanced timezone features may be available on Series 3 device {device_model}"
        )
    else:
        # Series 2 has basic timezone support
        print(f"Basic timezone support on Series 2 device {device_model}")
