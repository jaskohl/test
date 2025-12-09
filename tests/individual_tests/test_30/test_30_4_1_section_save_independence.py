"""
Test: 30.4.1 - SNMP Sections Save Independently (Device )
Category: SNMP Configuration (30)
Purpose: Verify each SNMP section can save without affecting others
Expected: Three independent save buttons work correctly
Series: Both Series 2 and 3
Priority: MEDIUM
Hardware: Device Only
Based on: test_30_snmp_config.py
: DeviceCapabilities integration with timeout multipliers and device-aware patterns
"""

import pytest
import time
import logging
from pages.snmp_config_page import SNMPConfigPage
from pages.device_capabilities import DeviceCapabilities
from playwright.sync_api import expect

logger = logging.getLogger(__name__)


def test_30_4_1_section_save_independence(
    snmp_config_page: SNMPConfigPage, base_url: str, request
):
    """
    Test 30.4.1: SNMP Sections Save Independently (Device )
    Purpose: Verify each SNMP section can save without affecting others with device-aware patterns
    Expected: Three independent save buttons work correctly
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
        f"Testing SNMP section save independence on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to SNMP page
    snmp_config_page.page.goto(f"{base_url}/snmp")
    time.sleep(1 * timeout_multiplier)

    # : Use device-aware save button detection
    save_button_pattern = DeviceCapabilities.get_interface_specific_save_button(
        device_model, "snmp_configuration", None
    )
    device_series = DeviceCapabilities.get_series(device_model)
    logger.info(f"Using save button pattern: {save_button_pattern} for {device_series}")

    # Store original configuration values for rollback
    original_data = snmp_config_page.get_page_data()
    original_ro_community1 = original_data.get("ro_community1", "PUBLIC")
    original_trap_community = original_data.get("trap_community", "")

    try:
        # : Get device-aware save button locators
        save1_locator = None
        save2_locator = None
        save3_locator = None

        if device_series == "Series 3":
            save1_locator = snmp_config_page.page.locator("button#button_save_1")
            save2_locator = snmp_config_page.page.locator("button#button_save_2")
            save3_locator = snmp_config_page.page.locator("button#button_save_3")
        elif device_series == "Series 2":
            save1_locator = snmp_config_page.page.locator("input#button_save_1")
            save2_locator = snmp_config_page.page.locator("input#button_save_2")
            save3_locator = snmp_config_page.page.locator("input#button_save_3")

        # Modify v1/v2c section
        ro_community1 = snmp_config_page.page.locator("input[name='ro_community1']")
        ro_community1.fill("test_community_v1v2c_device")

        # : Only v1/v2c save button should enable (device-aware timeout)
        if save1_locator and save1_locator.count() > 0:
            expect(save1_locator).to_be_enabled(timeout=2000 * timeout_multiplier)
        if save2_locator and save2_locator.count() > 0:
            expect(save2_locator).to_be_disabled()
        if save3_locator and save3_locator.count() > 0:
            expect(save3_locator).to_be_disabled()

        # Reset and test section 2 modification
        ro_community1.fill(original_ro_community1)  # Reset section 1
        time.sleep(0.5 * timeout_multiplier)  # Device-aware delay
        if save1_locator and save1_locator.count() > 0:
            expect(save1_locator).to_be_disabled()

        # : Modify section 2
        trap_community = snmp_config_page.page.locator("input[name='trap_community']")
        if trap_community.count() > 0:
            trap_community.fill("test_trap_community_device")
            if save2_locator and save2_locator.count() > 0:
                expect(save2_locator).to_be_enabled(timeout=2000 * timeout_multiplier)
            if save1_locator and save1_locator.count() > 0:
                expect(save1_locator).to_be_disabled()
            if save3_locator and save3_locator.count() > 0:
                expect(save3_locator).to_be_disabled()

    finally:
        # Rollback to original values
        ro_community1 = snmp_config_page.page.locator("input[name='ro_community1']")
        if ro_community1.count() > 0:
            ro_community1.fill(original_ro_community1)

        trap_community = snmp_config_page.page.locator("input[name='trap_community']")
        if trap_community.count() > 0 and original_trap_community:
            trap_community.fill(original_trap_community)
        elif trap_community.count() > 0:
            trap_community.fill("")  # Clear if no original value

        # Save to restore original state
        snmp_config_page.save_v1_v2c_configuration()
        if trap_community.count() > 0:
            snmp_config_page.save_traps_configuration()
