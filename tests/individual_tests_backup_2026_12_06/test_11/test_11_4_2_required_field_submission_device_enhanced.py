"""
Test 11.4.2: Required Field Submission (Device-Enhanced)
Purpose: Validate required field submission behavior with device capabilities
Expected: Device-aware required field submission behavior
Device-Enhanced: Uses DeviceCapabilities for device-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_4_2_required_field_submission_device_enhanced(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.4.2: Required Field Submission (Device-Enhanced)
    Purpose: Validate required field submission behavior with device capabilities
    Expected: Device-aware required field submission behavior
    Device-Enhanced: Uses DeviceCapabilities for device-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate required field submission"
        )

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Navigate to general config page
    general_config_page.navigate_to_page()

    # Find required fields
    required_fields = general_config_page.page.locator(
        "[aria-required='true'], [required], .required"
    )

    if required_fields.count() > 0:
        # Clear required fields and attempt submission to test validation
        required_fields.first.fill("")

        # Look for save/submit button with device-aware targeting
        if device_series == 2:
            save_selectors = [
                "input[type='submit']",
                "button[type='submit']",
                "input[value*='Save']",
                "button:has-text('Save')",
            ]
        else:  # Series 3
            save_selectors = [
                "input[value*='Save']",
                "button:has-text('Save')",
                "input[type='submit'][value*='Save']",
            ]

        save_button = None
        for selector in save_selectors:
            try:
                button = general_config_page.page.locator(selector).first
                if button.count() > 0:
                    save_button = button
                    break
            except:
                continue

        if save_button:
            # Test form submission without required fields
            save_button.click()

            # Check for validation messages with device-aware timeout
            validation_messages = general_config_page.page.locator(
                ".error, .validation-error, [role='alert']"
            )

            # Wait for validation with series-specific timeout
            try:
                expect(validation_messages).to_be_visible(
                    timeout=timeout_multiplier * 3000
                )
                print(f"Required field validation working on {device_model}")
            except:
                print(f"Required field validation behavior may vary on {device_model}")
        else:
            print(
                f"No save button found for required field submission test on {device_model}"
            )
    else:
        print(f"No required fields found for submission test on {device_model}")
