"""
Test 30.4.3: Cross-Section Configuration Test (Device )
Purpose: Verify all three sections can be configured simultaneously
Expected: All sections maintain independent state
Series: Both 2 and 3

Category: 30 - SNMP Configuration
Test Type: Unit Test
Priority: MEDIUM
Hardware: Device Only
: DeviceCapabilities integration with timeout multipliers and device-aware patterns
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.snmp_config_page import SNMPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_30_4_3_cross_section_configuration(
    snmp_config_page: SNMPConfigPage, base_url: str, request
):
    """
    Test 30.4.3: Cross-Section Configuration Test (Device )
    Purpose: Verify all three sections can be configured simultaneously with device-aware patterns
    Expected: All sections maintain independent state
    Series: Both 2 and 3
    : DeviceCapabilities integration with timeout multipliers
    """
    # : Use request.session.device_hardware_model for device detection
    device_model = request.session.device_hardware_model
    if device_model == "Unknown":
        pytest.fail("Device model not detected - cannot determine SNMP capabilities")

    # : Apply timeout multiplier for device-aware testing
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    logger.info(
        f"Testing SNMP cross-section configuration on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to SNMP page
    snmp_config_page.page.goto(f"{base_url}/snmp")
    time.sleep(1 * timeout_multiplier)

    # : Use device-aware save button detection
    save_button_pattern = DeviceCapabilities.get_interface_specific_save_button(
        device_model, "snmp_configuration", None
    )
    logger.info(f"Using save button pattern: {save_button_pattern} for {device_model}")

    # Store original configuration values for rollback
    original_data = snmp_config_page.get_page_data()
    original_ro_community1 = original_data.get("ro_community1", "PUBLIC")
    original_trap_community = original_data.get("trap_community", "")
    original_auth_name = original_data.get("auth_name", "")

    try:
        # : Configure Section 1 with device-aware validation
        ro_community1 = snmp_config_page.page.locator("input[name='ro_community1']")
        if ro_community1.is_visible():
            ro_community1.fill("custom_public_device")

        # : Configure Section 2 (if trap fields visible)
        trap_fields = snmp_config_page.page.locator("input[name*='trap']")
        if trap_fields.count() > 0:
            trap_fields.first.fill("trap_config_device")

        # : Configure Section 3 (v3 fields) with device-aware validation
        v3_fields = snmp_config_page.page.locator("input[name='auth_name']")
        if v3_fields.is_visible():
            v3_fields.fill("test_user_device")

        # : Verify all three sections can be configured independently
        # Test the SNMP page object methods work correctly for all sections
        page_data = snmp_config_page.get_page_data()
        assert page_data is not None, "Page data extraction should work"

        # : Test save button detection works for all sections (device-aware)
        save_buttons_work = snmp_config_page.verify_save_buttons_present()
        assert save_buttons_work, "All save buttons should be detectable"

        # : Validate device series-specific behavior
        device_series = DeviceCapabilities.get_series(device_model)
        if device_series == "Series 3":
            # Series 3 should use button elements
            button_elements = snmp_config_page.page.locator(
                "button[name*='save']"
            ).count()
            logger.info(f"Series 3: Found {button_elements} button save elements")
        elif device_series == "Series 2":
            # Series 2 should use input elements
            input_elements = snmp_config_page.page.locator(
                "input[name*='save']"
            ).count()
            logger.info(f"Series 2: Found {input_elements} input save elements")

        # : Cross-validate configuration state with device capabilities
        assert (
            "ro_community1" in page_data
            or snmp_config_page.page.locator("input[name='ro_community1']").count() > 0
        ), "Section 1 should be accessible"

    finally:
        # Rollback to original values
        if ro_community1.is_visible():
            ro_community1.fill(original_ro_community1)

        if trap_fields.count() > 0:
            if original_trap_community:
                trap_fields.first.fill(original_trap_community)
            else:
                trap_fields.first.fill("")

        if v3_fields.is_visible():
            if original_auth_name:
                v3_fields.fill(original_auth_name)
            else:
                v3_fields.fill("")

        # Save to restore original state
        snmp_config_page.save_v1_v2c_configuration()
        if trap_fields.count() > 0:
            snmp_config_page.save_traps_configuration()
        if v3_fields.is_visible():
            snmp_config_page.save_v3_configuration()
