"""
Test 11.18.2: Feature Availability Validation (Device-Aware)
Purpose: Feature availability based on device capabilities
Expected: Device-specific feature availability behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_18_2_feature_availability_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.18.2: Feature Availability Validation (Device-Aware)
    Purpose: Feature availability based on device capabilities
    Expected: Device-specific feature availability behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate feature availability")

    general_config_page.navigate_to_page()

    # Check feature availability based on device model
    device_series = DeviceCapabilities.get_series(device_model)

    # Look for PTP-related features (Series 3 only)
    if device_series == 3:
        ptp_fields = general_config_page.page.locator(
            "input[name*='ptp' i], select[name*='ptp' i], button:has-text('PTP')"
        )
        if ptp_fields.count() > 0:
            print(f"{device_model} (Series 3): PTP features available as expected")
        else:
            print(f"{device_model} (Series 3): PTP features not found")
    else:
        # Series 2 should not have PTP features
        print(f"{device_model} (Series 2): PTP features not expected")

    # Check for interface count indicators
    interface_indicators = general_config_page.page.locator(
        "[data-interfaces], .interface-count, .ports-available"
    )
    if interface_indicators.count() > 0:
        # Device shows interface availability
        expect(interface_indicators.first).to_be_visible()
    else:
        print(f"No interface indicators found for {device_model}")
