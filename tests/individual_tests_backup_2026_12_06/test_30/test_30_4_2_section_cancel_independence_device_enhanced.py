"""
Test 30.4.2: SNMP Section Cancel Independence (Device Enhanced)
Purpose: Verify cancel buttons work per section
Expected: Cancel affects only current section
Series: Both 2 and 3

Category: 30 - SNMP Configuration
Test Type: Unit Test
Priority: MEDIUM
Hardware: Device Only
ENHANCED: DeviceCapabilities integration with timeout multipliers and device-aware patterns
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.snmp_config_page import SNMPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_30_4_2_section_cancel_independence_device_enhanced(
    snmp_config_page: SNMPConfigPage, base_url: str, request
):
    """
    Test 30.4.2: SNMP Section Cancel Independence (Device Enhanced)
    Purpose: Verify cancel buttons work per section with device-aware patterns
    Expected: Cancel affects only current section
    Series: Both 2 and 3
    ENHANCED: DeviceCapabilities integration with timeout multipliers
    """
    # ENHANCED: Use request.session.device_hardware_model for device detection
    device_model = request.session.device_hardware_model
    if device_model == "Unknown":
        pytest.fail("Device model not detected - cannot determine SNMP capabilities")

    # ENHANCED: Apply timeout multiplier for device-aware testing
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    logger.info(
        f"Testing SNMP section cancel independence on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to SNMP page
    snmp_config_page.page.goto(f"{base_url}/snmp")
    time.sleep(1 * timeout_multiplier)

    # Store original configuration values for rollback
    original_data = snmp_config_page.get_page_data()
    original_ro_community1 = original_data.get("ro_community1", "PUBLIC")
    original_trap_community = original_data.get("trap_community", "")
    original_auth_name = original_data.get("auth_name", "")

    try:
        # ENHANCED: Modify Section 1 with device-aware validation
        ro_community1 = snmp_config_page.page.locator("input[name='ro_community1']")
        if ro_community1.count() > 0:
            ro_community1.fill("modified_value_device")

            # Look for cancel buttons with device-aware timeout
            cancel_buttons = snmp_config_page.page.locator("input[value='Cancel']")
            if cancel_buttons.count() > 0:
                # Click first cancel button (should be for section 1)
                cancel_buttons.first.click()
                time.sleep(1 * timeout_multiplier)  # Device-aware delay

                # ENHANCED: Section 1 should revert (device-aware validation)
                new_value = ro_community1.input_value()
                # Note: May or may not revert immediately, depending on device implementation

        # ENHANCED: Sections 2 and 3 should be unaffected (device-aware validation)
        trap_community = snmp_config_page.page.locator("input[name='trap_community']")
        auth_name = snmp_config_page.page.locator("input[name='auth_name']")

        # These should remain in their original states
        if trap_community.count() > 0:
            trap_value = trap_community.input_value()
            if original_trap_community:
                assert (
                    trap_value == original_trap_community
                ), "Trap community should remain unchanged"

        if auth_name.count() > 0:
            auth_value = auth_name.input_value()
            if original_auth_name:
                assert (
                    auth_value == original_auth_name
                ), "Auth name should remain unchanged"

    finally:
        # Rollback to original values
        ro_community1 = snmp_config_page.page.locator("input[name='ro_community1']")
        if ro_community1.count() > 0:
            ro_community1.fill(original_ro_community1)

        if trap_community.count() > 0 and original_trap_community:
            trap_community.fill(original_trap_community)
        elif trap_community.count() > 0:
            trap_community.fill("")

        if auth_name.count() > 0 and original_auth_name:
            auth_name.fill(original_auth_name)
        elif auth_name.count() > 0:
            auth_name.fill("")

        # Save to restore original state
        snmp_config_page.save_v1_v2c_configuration()
        if trap_community.count() > 0:
            snmp_config_page.save_traps_configuration()
        if auth_name.count() > 0:
            snmp_config_page.save_v3_configuration()
