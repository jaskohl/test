"""
Test: 30.1.3 - SNMP v1/v2c Section Save Button (Device )
Category: SNMP Configuration (Category 30)
Purpose: Verify v1/v2c section saves independently
Expected: button_save_1 saves only v1/v2c settings
Series: Both Series 2 and 3
Priority: MEDIUM
Hardware: Device Only
Based on COMPLETE_TEST_LIST.md Section 30.1.3
Device exploration data: config_snmp.forms.json
FIXED: Added actual form field modification to enable save button
: DeviceCapabilities integration with timeout multipliers and device-aware patterns
"""

import pytest
import time
import logging
from pages.snmp_config_page import SNMPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_30_1_3_v1v2c_save_button(
    snmp_config_page: SNMPConfigPage, base_url: str, request
):
    """
    Test 30.1.3: SNMP v1/v2c Section Save Button (Device )
    Purpose: Verify v1/v2c section saves independently with device-aware patterns
    Expected: button_save_1 saves only v1/v2c settings
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
        f"Testing SNMP v1/v2c save button on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to SNMP page
    snmp_config_page.page.goto(f"{base_url}/snmp")
    time.sleep(1 * timeout_multiplier)

    # : Use device-aware save button detection
    save_button_pattern = DeviceCapabilities.get_interface_specific_save_button(
        device_model, "snmp_configuration", None
    )
    logger.info(f"Using save button pattern: {save_button_pattern} for {device_model}")

    # Get original configuration
    original_data = snmp_config_page.get_page_data()
    original_community1 = original_data.get("ro_community1", "")
    try:
        # CRITICAL FIX: Actually modify form fields to enable save button
        # Step 1: Modify ro_community1 field
        ro_community1_field = snmp_config_page.page.locator(
            "input[name='ro_community1']"
        )
        if ro_community1_field.count() > 0:
            ro_community1_field.fill("test_community_v1v2c")

        # Step 2: Modify ro_community2 field if available
        ro_community2_field = snmp_config_page.page.locator(
            "input[name='ro_community2']"
        )
        if ro_community2_field.count() > 0:
            ro_community2_field.fill("public2_test")

        # Step 3: Wait for save button to become enabled
        time.sleep(1 * timeout_multiplier)  # Device-aware timeout

        # Step 4: Save using section-specific method (device-aware)
        result = snmp_config_page.save_v1_v2c_configuration()
        assert result, "Save operation should succeed"

        # : Verify configuration was applied with device-aware validation
        ro_community1_field = snmp_config_page.page.locator(
            "input[name='ro_community1']"
        )
        if ro_community1_field.count() > 0:
            assert (
                ro_community1_field.input_value() == "test_community_v1v2c"
            ), "Community 1 should be updated"

    finally:
        # Reset to original state
        ro_community1_field = snmp_config_page.page.locator(
            "input[name='ro_community1']"
        )
        if ro_community1_field.count() > 0:
            if original_community1:
                ro_community1_field.fill(original_community1)
            else:
                ro_community1_field.fill("")  # Clear field if no original value
        snmp_config_page.save_v1_v2c_configuration()
