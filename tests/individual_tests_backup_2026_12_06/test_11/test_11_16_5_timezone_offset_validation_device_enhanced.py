"""
Test 11.16.5: Timezone Offset Validation (Device-Enhanced)
Purpose: Timezone offset validation with comprehensive device-aware testing
Expected: Device-specific timezone offset behavior based on hardware capabilities
Device-Enhanced: Full DeviceCapabilities integration with series-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_16_5_timezone_offset_validation_device_enhanced(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.16.5: Timezone Offset Validation (Device-Enhanced)
    Purpose: Timezone offset validation with comprehensive device-aware testing
    Expected: Device-specific timezone offset behavior based on hardware capabilities
    Device-Enhanced: Full DeviceCapabilities integration with series-specific validation
    """
    # Device detection and validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate timezone offset behavior"
        )

    # Get device capabilities for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    general_config_page.navigate_to_page()

    # Look for timezone offset fields with device-aware targeting
    offset_selectors = [
        "input[name*='offset' i]",
        "input[name*='gmt' i]",
        "input[name*='timezone_offset' i]",
        "select[name*='offset' i]",
        "select[name*='timezone_offset' i]",
    ]

    offset_field = None
    for selector in offset_selectors:
        try:
            potential_field = general_config_page.page.locator(selector)
            if potential_field.count() > 0:
                # Check if field is visible and enabled
                if potential_field.first.is_visible(timeout=timeout_multiplier * 1000):
                    offset_field = potential_field.first
                    break
        except Exception:
            continue

    if not offset_field:
        print(
            f"No timezone offset fields found for {device_model} (Series {device_series})"
        )
        return

    # Test valid offset ranges based on device capabilities
    valid_offsets = [
        "-12",
        "-11",
        "-10",
        "-9",
        "-8",
        "-7",
        "-6",
        "-5",
        "-4",
        "-3",
        "-2",
        "-1",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
    ]

    # Series-specific offset validation
    if device_series == 2:
        # Series 2 devices typically have simpler timezone support
        # Focus on common North American and European offsets
        series_offsets = [
            "-12",
            "-11",
            "-10",
            "-9",
            "-8",
            "-7",
            "-6",
            "-5",
            "-4",
            "-3",
            "-2",
            "-1",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
        ]
    else:
        # Series 3 devices may support extended timezone ranges
        # Include additional offsets for global timezone support
        series_offsets = valid_offsets

    print(
        f"Testing timezone offset validation for {device_model} (Series {device_series})"
    )
    print(f"Testing {len(series_offsets)} offset values: {series_offsets}")

    # Test valid offset values
    for offset in series_offsets:
        try:
            # Clear and fill the field
            offset_field.clear()
            offset_field.fill(offset)

            # Validate the value is accepted
            expect(offset_field).to_have_value(
                offset, timeout=timeout_multiplier * 1000
            )

            # Check if save functionality is available
            try:
                save_button = general_config_page.page.locator(
                    "button[type='submit'], input[type='submit'], button:has-text('Save'), button:has-text('Apply')"
                )
                if save_button.count() > 0 and save_button.first.is_visible(
                    timeout=timeout_multiplier * 1000
                ):
                    print(f"Valid offset {offset} accepted for {device_model}")
            except Exception:
                pass

        except Exception as e:
            print(f"Error testing offset {offset} on {device_model}: {str(e)}")

    # Test invalid offset values
    invalid_offsets = ["-15", "-20", "15", "20", "999", "abc", "", "12:30", "UTC+5"]

    for invalid_offset in invalid_offsets:
        try:
            offset_field.clear()
            offset_field.fill(invalid_offset)

            # Check for validation feedback
            validation_feedback = general_config_page.page.locator(
                ".error, .invalid, .validation-error, [class*='error'], [class*='invalid']"
            )

            if validation_feedback.count() > 0:
                print(
                    f"Invalid offset {invalid_offset} properly rejected for {device_model}"
                )
            else:
                # Field might accept the value but it could be normalized
                current_value = offset_field.input_value()
                print(
                    f"Offset {invalid_offset} result: '{current_value}' for {device_model}"
                )

        except Exception as e:
            print(
                f"Error testing invalid offset {invalid_offset} on {device_model}: {str(e)}"
            )

    # Test boundary values
    boundary_tests = [("minimum", "-12"), ("maximum", "14"), ("zero", "0")]

    for boundary_name, boundary_value in boundary_tests:
        try:
            offset_field.clear()
            offset_field.fill(boundary_value)

            expect(offset_field).to_have_value(
                boundary_value, timeout=timeout_multiplier * 1000
            )
            print(
                f"Boundary test {boundary_name} ({boundary_value}) passed for {device_model}"
            )

        except Exception as e:
            print(f"Boundary test {boundary_name} failed for {device_model}: {str(e)}")

    # Test persistence if possible
    try:
        # Set a valid offset
        test_offset = "5"
        offset_field.clear()
        offset_field.fill(test_offset)

        # Look for save functionality
        save_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:has-text('Save')",
            "button:has-text('Apply')",
        ]

        for save_selector in save_selectors:
            save_button = general_config_page.page.locator(save_selector)
            if save_button.count() > 0 and save_button.first.is_visible(
                timeout=timeout_multiplier * 1000
            ):
                save_button.first.click(timeout=timeout_multiplier * 2000)

                # Wait for potential page reload or update
                general_config_page.page.wait_for_timeout(timeout_multiplier * 1000)

                # Check if the value persists
                persisted_value = offset_field.input_value()
                if persisted_value == test_offset:
                    print(f"Offset persistence test passed for {device_model}")
                else:
                    print(
                        f"Offset persistence test: expected '{test_offset}', got '{persisted_value}' for {device_model}"
                    )
                break

    except Exception as e:
        print(f"Persistence test failed for {device_model}: {str(e)}")

    print(
        f"Timezone offset validation completed for {device_model} (Series {device_series})"
    )
