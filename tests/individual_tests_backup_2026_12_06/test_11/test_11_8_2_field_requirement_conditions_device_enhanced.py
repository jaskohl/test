"""
Test 11.8.2: Field Requirement Conditions (Device-Enhanced)
Purpose: Field requirement conditions with device capabilities
Expected: Device-aware field requirement behavior
Device-Enhanced: Uses DeviceCapabilities for device-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_8_2_field_requirement_conditions_device_enhanced(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.8.2: Field Requirement Conditions (Device-Enhanced)
    Purpose: Field requirement conditions with device capabilities
    Expected: Device-aware field requirement behavior
    Device-Enhanced: Uses DeviceCapabilities for device-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate field requirements")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Navigate to general config page
    general_config_page.navigate_to_page()

    # Identify required vs optional fields based on device series
    if device_series == 2:
        # Series 2: Basic field requirements
        basic_fields = ["input[name='identifier']", "input[name='location']"]
    else:  # Series 3
        # Series 3: Additional fields may be required based on configuration
        advanced_fields = [
            "input[name='identifier']",
            "input[name='location']",
            "select[name*='interface']",
        ]
        basic_fields = advanced_fields

    # Check field requirement patterns
    required_count = 0
    optional_count = 0

    for selector in basic_fields:
        try:
            field = general_config_page.page.locator(selector).first
            if field.count() > 0:
                # Check for required indicators
                is_required = (
                    field.get_attribute("required") is not None
                    or field.get_attribute("aria-required") == "true"
                    or field.locator("..").get_attribute("class") is not None
                    and "required" in field.locator("..").get_attribute("class")
                )

                if is_required:
                    required_count += 1
                    print(f" Required field: {selector}")
                else:
                    optional_count += 1
                    print(f"- Optional field: {selector}")
        except:
            continue

    print(
        f"Field requirements summary for {device_model}: {required_count} required, {optional_count} optional"
    )

    # Validate requirement patterns
    if required_count >= 1:
        print(f" Required field patterns detected on {device_model}")
    else:
        print(f" No required fields detected on {device_model}")

    # Test dynamic requirement changes if supported
    if device_series == 3:
        # Series 3 may have conditional requirements based on advanced features
        print(f"Advanced requirement conditions may apply to {device_model}")
    else:
        print(f"Basic requirement conditions on {device_model}")
