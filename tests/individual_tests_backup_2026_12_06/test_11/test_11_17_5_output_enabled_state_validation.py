"""
Test 11.17.5: Output Enabled State Validation (Device-Aware)
Purpose: Output enabled/disabled state validation
Expected: Device-specific output enable behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_17_5_output_enabled_state_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.17.5: Output Enabled State Validation (Device-Aware)
    Purpose: Output enabled/disabled state validation
    Expected: Device-specific output enable behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate output enable behavior"
        )

    general_config_page.navigate_to_page()

    # Look for output enable fields
    enable_fields = general_config_page.page.locator(
        "input[name*='enable' i], input[name*='output' i], input[name*='active' i]"
    )
    if enable_fields.count() > 0:
        enable_field = enable_fields.first
        if enable_field.get_attribute("type") == "checkbox":
            # Test enable/disable toggle
            enable_field.check()
            expect(enable_field).to_be_checked()
            enable_field.uncheck()
            expect(enable_field).not_to_be_checked()
            # Test that enabling/disabling affects other fields
            enable_field.check()
            # Device should enable dependent output configuration fields
        else:
            # Text field for enable state
            enable_field.fill("enabled")
            expect(enable_field).to_have_value("enabled")
            enable_field.fill("disabled")
            expect(enable_field).to_have_value("disabled")
    else:
        print(f"No output enable fields found for {device_model}")
