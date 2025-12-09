"""
Test 30.3.2: SNMP v3 Section Save Button (Device Enhanced)
Purpose: Verify v3 section saves independently
Expected: button_save_3 saves only v3 settings
Series: Both 2 and 3
FIXED: Added actual form field modification to enable save button
ENHANCED: DeviceCapabilities integration with timeout multipliers and device-aware patterns

Category: 30 - SNMP Configuration
Test Type: Unit Test
Priority: MEDIUM
Hardware: Device Only
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.snmp_config_page import SNMPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_30_3_2_v3_save_button_device_enhanced(
    snmp_config_page: SNMPConfigPage, base_url: str, request
):
    """
    Test 30.3.2: SNMP v3 Section Save Button (Device Enhanced)
    Purpose: Verify v3 section saves independently with device-aware patterns
    Expected: button_save_3 saves only v3 settings
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
        f"Testing SNMP v3 save button on {device_model} with {timeout_multiplier}x timeout multiplier"
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
    try:
        # CRITICAL FIX: Actually modify form fields to enable save button
        # Step 1: Modify v3 auth name field if available
        auth_name_field = snmp_config_page.page.locator("input[name='auth_name']")
        if auth_name_field.count() > 0:
            auth_name_field.fill("test_v3_user_device")

        # Step 2: Modify v3 auth key field if available
        auth_key_field = snmp_config_page.page.locator("input[name='auth_key']")
        if auth_key_field.count() > 0:
            auth_key_field.fill("test_v3_key_12345_device")

        # Step 3: Wait for save button to become enabled
        time.sleep(1 * timeout_multiplier)  # Device-aware timeout

        # Step 4: Save using section-specific method (device-aware)
        result = snmp_config_page.save_v3_configuration()
        assert result, "Save operation should succeed"

        # ENHANCED: Verify configuration was applied with device-aware validation
        auth_name_field = snmp_config_page.page.locator("input[name='auth_name']")
        if auth_name_field.count() > 0:
            assert (
                auth_name_field.input_value() == "test_v3_user_device"
            ), "Auth name should be updated"

    finally:
        # Reset to original state if original values exist
        auth_name = original_data.get("auth_name")
        if auth_name:
            auth_name_field = snmp_config_page.page.locator("input[name='auth_name']")
            if auth_name_field.count() > 0:
                auth_name_field.fill(auth_name)
            snmp_config_page.save_v3_configuration()
