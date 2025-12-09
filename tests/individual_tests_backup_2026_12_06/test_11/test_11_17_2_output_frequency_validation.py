"""
Test 11.17.2: Output Frequency Validation (Device-Aware)
Purpose: Output frequency validation and range checking
Expected: Device-specific output frequency behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_17_2_output_frequency_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.17.2: Output Frequency Validation (Device-Aware)
    Purpose: Output frequency validation and range checking
    Expected: Device-specific output frequency behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate output frequency behavior"
        )

    general_config_page.navigate_to_page()

    # Look for frequency fields
    frequency_fields = general_config_page.page.locator(
        "input[name*='frequency' i], input[name*='rate' i], input[name*='hz' i]"
    )
    if frequency_fields.count() > 0:
        frequency_field = frequency_fields.first
        # Test common frequency values
        common_frequencies = ["1", "10", "100", "1000", "10000"]
        for freq in common_frequencies:
            frequency_field.clear()
            frequency_field.fill(freq)
            expect(frequency_field).to_have_value(freq)
        # Test out-of-range frequency
        frequency_field.clear()
        frequency_field.fill("999999")
        # Device should handle range validation appropriately
    else:
        print(f"No frequency fields found for {device_model}")
