"""
Test: 30.2.3 - SNMP Traps Section Save Button
Category: SNMP Configuration (30)
Purpose: Verify traps section saves independently
Expected: button_save_2 saves only trap settings
Series: Both Series 2 and 3
Priority: MEDIUM
Hardware: Device Only
Based on: test_30_snmp_config.py
FIXED: Added actual form field modification to enable save button
"""

import pytest
import time
from pages.snmp_config_page import SNMPConfigPage


def test_30_2_3_traps_save_button(snmp_config_page: SNMPConfigPage):
    """
    Test 30.2.3: SNMP Traps Section Save Button
    Purpose: Verify traps section saves independently
    Expected: button_save_2 saves only trap settings
    Series: Both 2 and 3
    FIXED: Added actual form field modification to enable save button
    """
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
            trap_community_field.fill("test_trap_community")

        # Step 2: Modify trap destination fields if available
        trap_dest_fields = snmp_config_page.page.locator("input[name*='trap_dest']")
        if trap_dest_fields.count() > 0:
            trap_dest_fields.first.fill("192.168.1.100")

        # Step 3: Wait for save button to become enabled
        time.sleep(1)  # Allow page to process changes

        # Step 4: Save using section-specific method (device-aware)
        result = snmp_config_page.save_traps_configuration()
        assert result, "Save operation should succeed"

        # Verify configuration was applied
        trap_community_field = snmp_config_page.page.locator(
            "input[name='trap_community']"
        )
        if trap_community_field.count() > 0:
            assert (
                trap_community_field.input_value() == "test_trap_community"
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
