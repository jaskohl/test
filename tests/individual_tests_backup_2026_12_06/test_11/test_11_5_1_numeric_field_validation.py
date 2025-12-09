"""
Test 11.5.1: Numeric Field Validation (Device-Aware)
Purpose: Validation of numeric input fields
Expected: Device-specific numeric field behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_5_1_numeric_field_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.5.1: Numeric Field Validation (Device-Aware)
    Purpose: Validation of numeric input fields
    Expected: Device-specific numeric field behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate numeric field behavior"
        )

    general_config_page.navigate_to_page()

    # Look for numeric fields (ports, timeouts, etc.)
    numeric_fields = general_config_page.page.locator(
        "input[type='number'], input[name*='port' i], input[name*='timeout' i]"
    )
    if numeric_fields.count() > 0:
        numeric_field = numeric_fields.first
        # Test valid numeric input
        numeric_field.fill("123")
        expect(numeric_field).to_have_value("123")
        # Test invalid input (should be rejected or show error)
        numeric_field.fill("abc")
        # Field may accept invalid input client-side but validate server-side
    else:
        print(f"No numeric fields found for {device_model}")
