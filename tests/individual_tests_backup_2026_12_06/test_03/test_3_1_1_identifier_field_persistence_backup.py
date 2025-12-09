"""
Test 3.1.1: Identifier Field Persistence
Purpose: Verify device identifier field accepts and persists values
Expected: Values saved and persist after page reload

Category: 3 - General Configuration
Test Type: Unit Test
Priority: HIGH
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_3_1_1_identifier_field_persistence(general_config_page: GeneralConfigPage):
    """
    Test 3.1.1: Identifier Field Persistence
    Purpose: Verify device identifier field accepts and persists values
    Expected: Values saved and persist after page reload
    FIXED: Removed domcontentloaded timeout issue - 5000ms is sufficient for embedded devices
    FIXED: Added proper error handling for domcontentloaded wait
    """
    field_name = "identifier"
    test_value = "Test Kronos Device 001"

    # Get original values for rollback
    original_data = general_config_page.get_page_data()
    original_value = original_data.get(field_name, "")
    try:
        # Configure the field using page object method
        general_config_page.configure_device_info(**{field_name: test_value})
        general_config_page.save_configuration()
        # FIXED: Removed problematic domcontentloaded timeout - device handles save operation
        # Wait briefly for device to persist data
        time.sleep(3)
        # Reload and verify persistence
        general_config_page.navigate_to_page()
        page_data = general_config_page.get_page_data()
        assert (
            page_data.get(field_name) == test_value
        ), f"{field_name} should persist after save"
    finally:
        # Rollback: Restore original value
        general_config_page.configure_device_info(**{field_name: original_value})
        general_config_page.save_configuration()
        time.sleep(1)
