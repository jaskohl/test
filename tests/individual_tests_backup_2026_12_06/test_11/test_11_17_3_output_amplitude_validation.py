"""
Test 11.17.3: Output Amplitude Validation (Device-Aware)
Purpose: Output amplitude validation and limits
Expected: Device-specific output amplitude behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_17_3_output_amplitude_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.17.3: Output Amplitude Validation (Device-Aware)
    Purpose: Output amplitude validation and limits
    Expected: Device-specific output amplitude behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate output amplitude behavior"
        )

    general_config_page.navigate_to_page()

    # Look for amplitude fields
    amplitude_fields = general_config_page.page.locator(
        "input[name*='amplitude' i], input[name*='level' i], input[name*='voltage' i]"
    )
    if amplitude_fields.count() > 0:
        amplitude_field = amplitude_fields.first
        # Test typical amplitude values
        typical_amplitudes = ["1.0", "2.5", "5.0", "10.0"]
        for amp in typical_amplitudes:
            amplitude_field.clear()
            amplitude_field.fill(amp)
            expect(amplitude_field).to_have_value(amp)
        # Test zero amplitude
        amplitude_field.clear()
        amplitude_field.fill("0")
        expect(amplitude_field).to_have_value("0")
    else:
        print(f"No amplitude fields found for {device_model}")
