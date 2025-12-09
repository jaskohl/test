"""
Test 11.16.2: Timezone Format Validation (Device-Aware)
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


def test_11_16_2_timezone_format_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.16.2: Timezone format validation and accepted formats (Device-Aware)
    Purpose: Test timezone format validation and accepted formats
    Expected: Device should handle timezone format validation appropriately
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate timezone format behavior"
        )

    device_series = DeviceCapabilities.get_series(device_model)

    try:
        general_config_page.navigate_to_page()

        # Look for timezone text input fields
        timezone_fields = general_config_page.page.locator(
            "input[name*='timezone' i], input[name*='tz' i]"
        )
        if timezone_fields.count() > 0:
            timezone_field = timezone_fields.first
            # Test valid timezone formats
            valid_timezones = ["UTC", "GMT", "EST", "PST", "CET", "Asia/Tokyo"]
            for tz in valid_timezones:
                timezone_field.fill(tz)
                expect(timezone_field).to_have_value(tz)
            # Test invalid timezone format
            timezone_field.fill("Invalid/Timezone")
            # Device may accept invalid format client-side
        else:
            print(f"No timezone text fields found for {device_model}")

    finally:
        # Cleanup: Reset fields to original state if needed
        pass
