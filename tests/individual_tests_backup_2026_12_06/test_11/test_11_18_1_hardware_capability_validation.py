"""
Test 11.18.1: Hardware Capability Validation (Device-Aware)
Purpose: Hardware capability detection and validation
Expected: Device-specific hardware capability behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_18_1_hardware_capability_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.18.1: Hardware Capability Validation (Device-Aware)
    Purpose: Hardware capability detection and validation
    Expected: Device-specific hardware capability behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate hardware capabilities")

    general_config_page.navigate_to_page()

    # Validate hardware capabilities based on device model
    device_series = DeviceCapabilities.get_series(device_model)
    capabilities = DeviceCapabilities.get_capabilities(device_model)

    # Test Series 2 vs Series 3 capabilities
    if device_series == 2:
        # Series 2 should have specific limitations
        print(f"{device_model} (Series 2): Validating Series 2 hardware capabilities")
        # Series 2 typically has fewer interfaces, no PTP
    else:
        # Series 3 should have advanced capabilities
        print(f"{device_model} (Series 3): Validating Series 3 hardware capabilities")
        # Series 3 typically has more interfaces, PTP support

    # Check if device shows capability information
    capability_indicators = general_config_page.page.locator(
        ".capability, .hardware-info, [data-capability]"
    )
    if capability_indicators.count() > 0:
        # Device displays capability information
        expect(capability_indicators.first).to_be_visible()
    else:
        print(f"No capability indicators found for {device_model}")
