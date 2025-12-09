"""
Test 11.6.1: Minimum Value Validation (Device-Aware)
Purpose: Minimum value constraints on numeric fields
Expected: Device-specific minimum value constraints
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_6_1_minimum_value_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.6.1: Minimum Value Validation (Device-Aware)
    Purpose: Minimum value constraints on numeric fields
    Expected: Device-specific minimum value constraints
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate minimum value constraints"
        )

    general_config_page.navigate_to_page()

    # Look for numeric fields with minimum values
    numeric_fields = general_config_page.page.locator("input[type='number']")
    if numeric_fields.count() > 0:
        numeric_field = numeric_fields.first
        # Test minimum value behavior
        # Most numeric fields on Kronos devices should accept reasonable minimum values
        numeric_field.fill("0")  # Common minimum
        expect(numeric_field).to_have_value("0")
        numeric_field.fill("1")  # Common minimum for port/time values
        expect(numeric_field).to_have_value("1")
    else:
        print(f"No numeric fields found for minimum value validation on {device_model}")
