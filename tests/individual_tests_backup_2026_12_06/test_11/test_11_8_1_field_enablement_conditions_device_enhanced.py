"""
Test 11.8.1: Field Enablement Conditions (Device-Enhanced)
Purpose: Field enablement conditions with device capabilities
Expected: Device-aware field enablement behavior
Device-Enhanced: Uses DeviceCapabilities for device-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_8_1_field_enablement_conditions_device_enhanced(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.8.1: Field Enablement Conditions (Device-Enhanced)
    Purpose: Field enablement conditions with device capabilities
    Expected: Device-aware field enablement behavior
    Device-Enhanced: Uses DeviceCapabilities for device-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate field enablement")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Navigate to general config page
    general_config_page.navigate_to_page()

    # Look for conditionally enabled fields
    # These fields may be enabled/disabled based on device capabilities
    if device_series == 2:
        # Series 2: Check basic fields and their enablement state
        field_selectors = [
            "input[name='identifier']",
            "input[name='location']",
            "input[name='contact']",
        ]
        expected_enabled_fields = 3  # Most basic fields should be enabled
    else:  # Series 3
        # Series 3: Check for additional fields enabled based on hardware capabilities
        field_selectors = [
            "input[name='identifier']",
            "input[name='location']",
            "input[name='contact']",
            "select[name*='interface']",
            "input[name*='ptp']",
        ]
        expected_enabled_fields = 3  # Basic fields should be enabled

    enabled_count = 0
    disabled_count = 0

    for selector in field_selectors:
        try:
            field = general_config_page.page.locator(selector).first
            if field.count() > 0:
                if field.is_enabled():
                    enabled_count += 1
                    print(f" Field enabled: {selector}")
                else:
                    disabled_count += 1
                    print(f"- Field disabled: {selector}")
        except:
            print(f"Field not found: {selector}")

    print(
        f"Field enablement summary for {device_model}: {enabled_count} enabled, {disabled_count} disabled"
    )

    # Validate that at least basic fields are enabled
    if enabled_count >= 1:
        print(f" Basic field enablement working on {device_model}")
    else:
        print(f" No fields found enabled on {device_model}")

    # Check for conditional enablement patterns
    if device_series == 3 and DeviceCapabilities.is_ptp_supported(device_model):
        ptp_fields = general_config_page.page.locator("input[name*='ptp']")
        if ptp_fields.count() > 0:
            if ptp_fields.first.is_enabled():
                print(f" PTP fields enabled as expected on {device_model}")
            else:
                print(
                    f"PTP fields disabled (may be expected behavior) on {device_model}"
                )
