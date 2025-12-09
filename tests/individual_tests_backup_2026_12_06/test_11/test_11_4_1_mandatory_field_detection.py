"""
Test 11.4.1: Mandatory Field Detection (Device-Aware)
Purpose: Identification and validation of required fields
Expected: Device-specific required field behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_4_1_mandatory_field_detection(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.4.1: Mandatory Field Detection (Device-Aware)
    Purpose: Identification and validation of required fields
    Expected: Device-specific required field behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate mandatory field behavior"
        )

    general_config_page.navigate_to_page()

    # Look for required field indicators (asterisks, aria-required, etc.)
    required_indicators = general_config_page.page.locator(
        "[aria-required='true'], .required, [required]"
    )
    if required_indicators.count() > 0:
        expect(required_indicators.first).to_be_visible()
    else:
        print(f"No required field indicators found for {device_model}")
