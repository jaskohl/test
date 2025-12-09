"""
Test 11.4.1: Mandatory Field Detection (Device-Enhanced)
Purpose: Identification and validation of required fields with device-aware behavior
Expected: Device-specific required field behavior based on capabilities
Device-Enhanced: Full DeviceCapabilities integration with series-specific patterns
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_4_1_mandatory_field_detection_device_enhanced(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.4.1: Mandatory Field Detection (Device-Enhanced)
    Purpose: Identification and validation of required fields with device-aware behavior
    Expected: Device-specific required field behavior based on capabilities
    Device-Enhanced: Full DeviceCapabilities integration with series-specific patterns
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate mandatory field behavior"
        )

    # Get device capabilities for enhanced validation
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    general_config_page.navigate_to_page()

    # Device-aware timeout handling
    base_timeout = 5000
    enhanced_timeout = int(base_timeout * timeout_multiplier)

    # Look for required field indicators with device-specific patterns
    if device_series == "Series 2":
        # Series 2 has simpler field requirements
        required_selectors = [
            "[aria-required='true']",
            ".required",
            "[required]",
            ".mandatory",
        ]
    else:  # Series 3
        # Series 3 has more complex field requirements including PTP-related fields
        required_selectors = [
            "[aria-required='true']",
            ".required",
            "[required]",
            ".mandatory",
            "[data-field-type='ptp']",  # PTP-related required fields
        ]

    # Check for required field indicators across all selectors
    total_required_fields = 0
    for selector in required_selectors:
        required_indicators = general_config_page.page.locator(selector)
        count = required_indicators.count()
        if count > 0:
            expect(required_indicators.first).to_be_visible(timeout=enhanced_timeout)
            total_required_fields += count
            print(f"Found {count} required fields using selector: {selector}")

    # Device-specific validation
    if device_series == "Series 2":
        # Series 2 should have basic required fields (identifier, location)
        expected_min_required = 2
        assert (
            total_required_fields >= expected_min_required
        ), f"Series 2 device {device_model} should have at least {expected_min_required} required fields, found {total_required_fields}"
    else:  # Series 3
        # Series 3 should have more required fields due to advanced features
        expected_min_required = 4
        assert (
            total_required_fields >= expected_min_required
        ), f"Series 3 device {device_model} should have at least {expected_min_required} required fields, found {total_required_fields}"

    # Check for device-specific required field patterns
    if device_series == "Series 3":
        # Check for PTP-related required fields
        ptp_required = general_config_page.page.locator(
            "[data-field-type='ptp'][required], .ptp-required"
        )
        if ptp_required.count() > 0:
            expect(ptp_required.first).to_be_visible(timeout=enhanced_timeout)
            print(
                f"Found PTP-related required fields for Series 3 device {device_model}"
            )
    else:
        print(
            f"Series 2 device {device_model} - no PTP-related required fields expected"
        )

    print(
        f"Successfully validated mandatory field detection for {device_model} ({device_series}): {total_required_fields} required fields found"
    )
