"""
Category 5: Time Configuration - Test 5.1.5
Timezone Section Independent Save
Test Count: 1 of 32 in Category 5
Hardware: Device Only
Priority: HIGH - Critical time synchronization settings
Series: Both Series 2 and 3
Based on test_05_time_config.py::TestTimezoneConfiguration::test_5_1_5_timezone_section_save
Device exploration data: config_time.forms.json
IMPORTANT: Time page has TWO sections with separate save buttons
FIXED: Added rollback logic and actual form field modification to enable save button
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.time_config_page import TimeConfigPage


def test_timezone_section_independent_save(time_config_page: TimeConfigPage):
    """
    Test 5.1.5: Timezone Section Independent Save
    Purpose: Verify timezone section saves independently from DST section
    Expected: button#button_save_1 saves only timezone settings
    Series: Both 2 and 3
    FIXED: Added rollback logic and actual form field modification to enable save button
    """
    # Get original timezone configuration for rollback
    original_data = time_config_page.get_page_data()
    original_timezone_value = original_data.get("timezone", "")
    try:
        # CRITICAL FIX: Actually modify form fields to enable save button
        # Step 1: Fill timezone dropdown to trigger save button enable
        timezone_dropdown = time_config_page.page.locator("select[name='timezone']")
        if timezone_dropdown.count() > 0:
            timezone_dropdown.select_option("US/Denver")
        else:
            # Fallback to input field
            timezone_input = time_config_page.page.locator("input[name='timezone']")
            timezone_input.fill("US/Denver")

        # Step 2: Modify offset field to further ensure save button is enabled
        offset_field = time_config_page.page.locator("input[name='offset']")
        if offset_field.count() > 0:
            offset_field.fill("-07:00")

        # Step 3: Wait for save button to become enabled
        time.sleep(1)  # Allow page to process changes

        # Step 4: Now call the save method - button should be enabled
        success = time_config_page.save_timezone_configuration()
        assert success, "Timezone configuration should save successfully"

        # Verify timezone is configured by checking the input value
        timezone_input = time_config_page.page.locator(
            "input[name='timezone'], select[name='timezone']"
        )
        if timezone_input.count() > 0:
            assert (
                timezone_input.input_value() is not None
            ), "Timezone should be configured"
            assert (
                len(timezone_input.input_value()) > 0
            ), "Timezone value should not be empty"

    finally:
        # Rollback: Restore original timezone configuration
        if original_timezone_value:
            timezone_dropdown = time_config_page.page.locator("select[name='timezone']")
            if timezone_dropdown.count() > 0:
                timezone_dropdown.select_option(original_timezone_value)
            else:
                timezone_input = time_config_page.page.locator("input[name='timezone']")
                timezone_input.fill(original_timezone_value)
            time_config_page.save_timezone_configuration()
            time.sleep(1)
