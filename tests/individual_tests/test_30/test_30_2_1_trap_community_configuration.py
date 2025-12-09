"""
Test: 30.2.1 - SNMP Trap Community String Configuration (Device )
Category: SNMP Configuration (30)
Purpose: Verify trap community string can be configured
Expected: Trap community field accepts input
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


def test_30_2_1_trap_community_configuration(
    snmp_config_page: SNMPConfigPage, base_url: str, request
):
    """
    Test 30.2.1: SNMP Trap Community String Configuration (Device )
    Purpose: Verify trap community string can be configured with device-aware patterns
    Expected: Trap community field accepts input
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
        f"Testing SNMP trap community configuration on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to SNMP page
    snmp_config_page.page.goto(f"{base_url}/snmp")
    time.sleep(1 * timeout_multiplier)

    # : Use device-aware save button detection
    save_button_pattern = DeviceCapabilities.get_interface_specific_save_button(
        device_model, "snmp_configuration", None
    )
    logger.info(f"Using save button pattern: {save_button_pattern} for {device_model}")

    # Look for trap community field with device-aware patterns
    trap_community = snmp_config_page.page.locator(
        "input[name*='trap_community'], input[name*='trap'][name*='comm']"
    )
    if trap_community.count() > 0:
        trap_field = trap_community.first

        # : Verify field is editable with device-aware validation
        expect(trap_field).to_be_editable()

        # Store original value for rollback
        original_value = trap_field.input_value()

        try:
            trap_field.fill("trap_community_device_test")
            assert trap_field.input_value() == "trap_community_device_test"

            # : Save with device-aware timeout
            snmp_config_page.save_trap_configuration()
            time.sleep(1 * timeout_multiplier)

        finally:
            # Rollback to original value
            if original_value:
                trap_field.fill(original_value)
            else:
                trap_field.fill("")
            snmp_config_page.save_trap_configuration()
    else:
        pytest.skip("Trap community field not found on this device")
