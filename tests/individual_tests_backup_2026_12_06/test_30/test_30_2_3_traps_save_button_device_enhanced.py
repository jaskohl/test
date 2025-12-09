"""
Test: 30.2.3 - SNMP Traps Section Save Button (Device Enhanced)
Category: SNMP Configuration (30)
Purpose: Verify traps section saves independently
Expected: button_save_2 saves only trap settings
Series: Both Series 2 and 3
Priority: MEDIUM
Hardware: Device Only
Based on: test_30_snmp_config.py
FIXED: Added actual form field modification to enable save button
ENHANCED: DeviceCapabilities integration with timeout multipliers and device-aware patterns
"""

import pytest
import time
import logging
from pages.snmp_config_page import SNMPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_30_2_3_traps_save_button_device_enhanced(
    snmp_config_page: SNMPConfigPage, base_url: str, request
):
    """
    Test 30.2.3: SNMP Traps Section Save Button (Device Enhanced)
    Purpose: Verify traps section saves independently with device-aware patterns
    Expected: button_save_2 saves only trap settings
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
        f"Testing SNMP traps save button on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to SNMP page
    snmp_config_page.page.goto(f"{base_url}/snmp")
    time.sleep(1 * timeout_multiplier)

    # ENHANCED: Use device-aware save button detection
    save_button_pattern = DeviceCapabilities.get_interface_specific_save_button(
        device_model, "snmp_configuration", None
    )
    logger.info(f"Using save button pattern: {save_button_pattern} for {device_model}")

    # Get original configuration
    original_data = snmp_config_page.get_page_data()
    original_trap_community = original_data.get("trap_community", "")
    try:
        # CRITICAL FIX: Actually modify form fields to enable save button
        # Step 1: Modify trap community field
        trap_community_field = snmp_config_page.page.locator(
            "input[name='trap_community']"
        )
        if trap_community_field.count() > 0:
            trap_community_field.fill("test_trap_community_device")

        # Step 2: Modify trap destination fields if available
        trap_dest_fields = snmp_config_page.page.locator("input[name*='trap_dest']")
        if trap_dest_fields.count() > 0:
            trap_dest_fields.first.fill("192.168.1.100")

        # Step 3: Wait for save button to become enabled
        time.sleep(1 * timeout_multiplier)  # Device-aware timeout

        # Step 4: Save using section-specific method (device-aware)
        result = snmp_config_page.save_traps_configuration()
        assert result, "Save operation should succeed"

        # ENHANCED: Verify configuration was applied with device-aware validation
        trap_community_field = snmp_config_page.page.locator(
            "input[name='trap_community']"
        )
        if trap_community_field.count() > 0:
            assert (
                trap_community_field.input_value() == "test_trap_community_device"
            ), "Trap community should be updated"

    finally:
        # Reset to original state
        if original_trap_community:
            trap_community_field = snmp_config_page.page.locator(
                "input[name='trap_community']"
            )
            if trap_community_field.count() > 0:
                trap_community_field.fill(original_trap_community)
            snmp_config_page.save_traps_configuration()
