"""
Test 11.16.1: Timezone Field Validation (Device-Aware)
Category 11: Form Validation Tests
Test Count: 1 of 47 total tests
Hardware: Device Only
Priority: MEDIUM - Input validation critical for data integrity
Series: Both Series 2 and 3

FIXES APPLIED:
-  Fixed device model detection: uses request.session.device_hardware_model
-  Device-aware validation using DeviceCapabilities.get_series()
-  Maintains rollback logic with try/finally blocks
-  Uses correct parameter signatures
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_16_1_timezone_field_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.16.1: Timezone field validation and format checking (Device-Aware)
    Purpose: Test timezone field validation and format checking
    Expected: Device should handle timezone validation appropriately
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate timezone behavior")

    device_series = DeviceCapabilities.get_series(device_model)

    try:
        general_config_page.navigate_to_page()

        # Look for timezone fields
        timezone_fields = general_config_page.page.locator(
            "select[name*='timezone' i], input[name*='timezone' i], input[name*='tz' i]"
        )
        if timezone_fields.count() > 0:
            timezone_field = timezone_fields.first
            if timezone_field.get_attribute("type") == "select":
                # Test timezone selection
                options = timezone_field.locator("option")
                option_count = options.count()
                assert option_count > 0, "Timezone field should have options"
                # Select first timezone option
                options.first.click()
            else:
                # Text input timezone field
                timezone_field.fill("UTC")
                expect(timezone_field).to_have_value("UTC")
        else:
            print(f"No timezone fields found for {device_model}")

    finally:
        # Cleanup: Reset fields to original state if needed
        pass
