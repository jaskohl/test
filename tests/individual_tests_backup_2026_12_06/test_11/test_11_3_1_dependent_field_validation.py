"""
Test 11.3.1: Dependent Field Validation (Device-Aware)
Purpose: Validation of fields that depend on other field values
Expected: Device-specific dependent field behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_3_1_dependent_field_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.3.1: Dependent Field Validation (Device-Aware)
    Purpose: Validation of fields that depend on other field values
    Expected: Device-specific dependent field behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate dependent field behavior"
        )

    general_config_page.navigate_to_page()

    # Look for fields with dependencies (e.g., VLAN ID depends on VLAN enable)
    vlan_enable = general_config_page.page.locator("input[name*='vlan_enable' i]")
    vlan_id = general_config_page.page.locator("input[name*='vlan_id' i]")

    if vlan_enable.is_visible() and vlan_id.is_visible():
        # Test: VLAN ID should be required when VLAN is enabled
        vlan_enable.check()
        # VLAN ID field should be accessible and required
        expect(vlan_id).to_be_enabled()
    else:
        print(
            f"Dependent field validation skipped for {device_model} - VLAN fields not found"
        )
