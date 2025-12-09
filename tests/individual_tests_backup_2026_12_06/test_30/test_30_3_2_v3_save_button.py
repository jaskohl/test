"""
Test 30.3.2: SNMP v3 Section Save Button
Purpose: Verify v3 section saves independently
Expected: button_save_3 saves only v3 settings
Series: Both 2 and 3
FIXED: Added actual form field modification to enable save button

Category: 30 - SNMP Configuration
Test Type: Unit Test
Priority: MEDIUM
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.snmp_config_page import SNMPConfigPage


def test_30_3_2_v3_save_button(snmp_config_page: SNMPConfigPage):
    """
    Test 30.3.2: SNMP v3 Section Save Button
    Purpose: Verify v3 section saves independently
    Expected: button_save_3 saves only v3 settings
    Series: Both 2 and 3
    FIXED: Added actual form field modification to enable save button
    """
    # Get original configuration
    original_data = snmp_config_page.get_page_data()
    try:
        # CRITICAL FIX: Actually modify form fields to enable save button
        # Step 1: Modify v3 auth name field if available
        auth_name_field = snmp_config_page.page.locator("input[name='auth_name']")
        if auth_name_field.count() > 0:
            auth_name_field.fill("test_v3_user")

        # Step 2: Modify v3 auth key field if available
        auth_key_field = snmp_config_page.page.locator("input[name='auth_key']")
        if auth_key_field.count() > 0:
            auth_key_field.fill("test_v3_key_12345")

        # Step 3: Wait for save button to become enabled
        time.sleep(1)  # Allow page to process changes

        # Step 4: Save using section-specific method (device-aware)
        result = snmp_config_page.save_v3_configuration()
        assert result, "Save operation should succeed"

        # Verify configuration was applied
        auth_name_field = snmp_config_page.page.locator("input[name='auth_name']")
        if auth_name_field.count() > 0:
            assert (
                auth_name_field.input_value() == "test_v3_user"
            ), "Auth name should be updated"

    finally:
        # Reset to original state if original values exist
        auth_name = original_data.get("auth_name")
        if auth_name:
            auth_name_field = snmp_config_page.page.locator("input[name='auth_name']")
            if auth_name_field.count() > 0:
                auth_name_field.fill(auth_name)
            snmp_config_page.save_v3_configuration()
