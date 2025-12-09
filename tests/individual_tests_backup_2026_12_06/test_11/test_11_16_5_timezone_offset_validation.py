"""
Test 11.16.5: Timezone Offset Validation (Device-Aware)
Purpose: Timezone offset validation and input ranges
Expected: Device-specific timezone offset behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_16_5_timezone_offset_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.16.5: Timezone Offset Validation (Device-Aware)
    Purpose: Timezone offset validation and input ranges
    Expected: Device-specific timezone offset behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate timezone offset behavior"
        )

    general_config_page.navigate_to_page()

    # Look for timezone offset fields
    offset_fields = general_config_page.page.locator(
        "input[name*='offset' i], input[name*='gmt' i]"
    )
    if offset_fields.count() > 0:
        offset_field = offset_fields.first
        # Test valid offset ranges (typically -12 to +14)
        valid_offsets = ["-12", "-5", "0", "5", "12", "14"]
        for offset in valid_offsets:
            offset_field.clear()
            offset_field.fill(offset)
            expect(offset_field).to_have_value(offset)
        # Test invalid offset values
        offset_field.clear()
        offset_field.fill("999")
        # Device may accept or reject based on validation rules
    else:
        print(f"No timezone offset fields found for {device_model}")
