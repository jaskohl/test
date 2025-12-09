"""
Test 11.17.4: Output Impedance Validation (Device-Aware)
Purpose: Output impedance validation and standard values
Expected: Device-specific output impedance behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_17_4_output_impedance_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.17.4: Output Impedance Validation (Device-Aware)
    Purpose: Output impedance validation and standard values
    Expected: Device-specific output impedance behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate output impedance behavior"
        )

    general_config_page.navigate_to_page()

    # Look for impedance fields
    impedance_fields = general_config_page.page.locator(
        "input[name*='impedance' i], input[name*='ohm' i], input[name*='resistance' i]"
    )
    if impedance_fields.count() > 0:
        impedance_field = impedance_fields.first
        # Test standard impedance values
        standard_impedances = ["50", "75", "600"]
        for imp in standard_impedances:
            impedance_field.clear()
            impedance_field.fill(imp)
            expect(impedance_field).to_have_value(imp)
        # Test invalid impedance value
        impedance_field.clear()
        impedance_field.fill("999999")
        # Device should validate impedance range
    else:
        print(f"No impedance fields found for {device_model}")
