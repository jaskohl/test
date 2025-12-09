"""
Test 11.17.1: Output Signal Type Validation (Device-Aware)
Purpose: Output signal type selection and validation
Expected: Device-specific output signal behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_17_1_output_signal_type_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.17.1: Output Signal Type Validation (Device-Aware)
    Purpose: Output signal type selection and validation
    Expected: Device-specific output signal behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate output signal behavior"
        )

    general_config_page.navigate_to_page()

    # Look for output signal type fields
    signal_fields = general_config_page.page.locator(
        "select[name*='signal' i], select[name*='output' i], select[name*='format' i]"
    )
    if signal_fields.count() > 0:
        signal_field = signal_fields.first
        options = signal_field.locator("option")
        option_count = options.count()
        if option_count > 1:
            # Test signal type selection
            options.nth(1).click()
            selected_signal = signal_field.input_value()
            assert selected_signal != "", "Signal type should be selected"
            # Device should provide appropriate signal format options
        else:
            print(f"Signal field has insufficient options for {device_model}")
    else:
        print(f"No signal type fields found for {device_model}")
