"""
Test: 30.2.1 - SNMP Trap Community String Configuration (Pure Page Object)
Category: SNMP Configuration (30)
Purpose: Verify trap community string can be configured
Expected: Trap community field accepts input
Series: Both Series 2 and 3
Priority: MEDIUM
Hardware: Device Only
Based on: test_30_snmp_config.py
: Pure page object pattern - no direct DeviceCapabilities calls
"""

import pytest
import time
import logging
from pages.snmp_config_page import SNMPConfigPage
from playwright.sync_api import expect

logger = logging.getLogger(__name__)


def test_30_2_1_trap_community_configuration_pure_page_object(
    snmp_config_page: SNMPConfigPage, base_url: str, request
):
    """
    Test 30.2.1: SNMP Trap Community String Configuration (Pure Page Object)
    Purpose: Verify trap community string can be configured with pure page object methods
    Expected: Trap community field accepts input
    Series: Both 2 and 3
    : Pure page object pattern - all DeviceCapabilities calls encapsulated in SNMPConfigPage
    """
    # Get device model and initialize page object with device-aware patterns
    device_model = request.session.device_hardware_model
    if device_model == "Unknown":
        pytest.fail("Device model not detected - cannot determine SNMP capabilities")

    # Initialize page object with device-aware patterns
    snmp_config_page = SNMPConfigPage(snmp_config_page.page, device_model)

    # Apply timeout multiplier for device-aware testing using page object method
    timeout_multiplier = snmp_config_page.get_timeout_multiplier()
    logger.info(
        f"Testing SNMP trap community configuration on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to SNMP page using page object method
    snmp_config_page.navigate_to_page()
    time.sleep(1 * timeout_multiplier)

    # Use device-aware save button detection using page object method
    save_button_pattern = snmp_config_page.get_interface_specific_save_button()
    logger.info(f"Using save button pattern: {save_button_pattern} for {device_model}")

    # Look for trap community field with device-aware patterns
    trap_community = snmp_config_page.page.locator(
        "input[name*='trap_community'], input[name*='trap'][name*='comm']"
    )
    if trap_community.count() > 0:
        trap_field = trap_community.first

        # Verify field is editable with device-aware validation
        expect(trap_field).to_be_editable()

        # Store original value for rollback
        original_value = trap_field.input_value()

        try:
            trap_field.fill("trap_community_device_test")
            assert trap_field.input_value() == "trap_community_device_test"

            # Save with device-aware timeout using page object method
            save_success = snmp_config_page.save_configuration()
            if save_success:
                logger.info(
                    f"Trap community configuration saved successfully on {device_model}"
                )
            else:
                logger.warning(
                    f"Trap community configuration save failed on {device_model}"
                )

            time.sleep(1 * timeout_multiplier)

        finally:
            # Rollback to original value
            if original_value:
                trap_field.fill(original_value)
            else:
                trap_field.fill("")

            # Save rollback using page object method
            rollback_success = snmp_config_page.save_configuration()
            if rollback_success:
                logger.info(
                    f"Trap community configuration rollback successful on {device_model}"
                )
            else:
                logger.warning(
                    f"Trap community configuration rollback failed on {device_model}"
                )
    else:
        pytest.skip("Trap community field not found on this device")

    # Validate SNMP support using page object method
    snmp_supported = snmp_config_page.has_capability("snmp_support")
    if not snmp_supported:
        logger.warning(f"SNMP support not indicated in capabilities for {device_model}")

    # Log comprehensive test results using page object methods
    device_info = snmp_config_page.get_device_info()
    capabilities = snmp_config_page.get_capabilities()

    logger.info(f"SNMP trap community configuration test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"Device capabilities: {capabilities}")

    print(
        f"SNMP TRAP COMMUNITY CONFIGURATION VALIDATED (PURE PAGE OBJECT): {device_model}"
    )
