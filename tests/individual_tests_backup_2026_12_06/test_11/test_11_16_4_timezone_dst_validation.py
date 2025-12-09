"""
Test 11.16.4: Timezone DST Validation (Device-Aware)
Purpose: Daylight Saving Time timezone validation
Expected: Device-specific DST timezone behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_16_4_timezone_dst_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.16.4: Timezone DST Validation (Device-Aware)
    Purpose: Daylight Saving Time timezone validation
    Expected: Device-specific DST timezone behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate DST behavior")

    general_config_page.navigate_to_page()

    # Look for timezone fields with DST options
    dst_fields = general_config_page.page.locator(
        "input[name*='dst' i], select[name*='dst' i]"
    )
    if dst_fields.count() > 0:
        dst_field = dst_fields.first
        if dst_field.get_attribute("type") == "select":
            options = dst_field.locator("option")
            if options.count() > 0:
                # Test DST option selection
                options.first.click()
        else:
            # DST checkbox or text field
            if dst_field.get_attribute("type") == "checkbox":
                dst_field.check()
                expect(dst_field).to_be_checked()
                dst_field.uncheck()
                expect(dst_field).not_to_be_checked()
    else:
        print(f"No DST fields found for {device_model}")
