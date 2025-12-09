"""
Test: 5.2.5 - Complete Time Configuration Workflow
Category: Time Configuration (Category 5)
Purpose: Verify both timezone and DST can be configured together
Expected: Both sections save independently and persist
Series: Both Series 2 and 3
Priority: HIGH
Hardware: Device Only
Based on COMPLETE_TEST_LIST.md Section 5.2.5
Device exploration data: config_time.forms.json
"""

import pytest
from pages.time_config_page import TimeConfigPage


def test_5_2_5_complete_time_configuration(time_config_page: TimeConfigPage):
    """
    Test 5.2.5: Complete Time Configuration Workflow
    Purpose: Verify both timezone and DST can be configured together
    Expected: Both sections save independently and persist
    Series: Both 2 and 3
    """
    # Get original configuration for rollback
    original_data = time_config_page.get_page_data()
    original_timezone = original_data.get("timezone", "")
    original_dst_status = time_config_page.get_dst_status()
    try:
        # Configure timezone section
        success = time_config_page.set_timezone_with_save("US/Denver")
        assert success, "Timezone configuration should save successfully"

        # Configure DST section
        success = time_config_page.set_dst_with_save(True)
        assert success, "DST configuration should save successfully"

        # Verify both configurations persist
        timezone_input = time_config_page.page.locator("input[name='timezone']")
        assert timezone_input.input_value() is not None, "Timezone should persist"
        assert (
            len(timezone_input.input_value()) > 0
        ), "Timezone value should not be empty"

        dst_status = time_config_page.get_dst_status()
        assert dst_status is True, "DST should persist"

    finally:
        # Rollback: Restore original configuration
        if original_timezone:
            time_config_page.configure_timezone(original_timezone)
            time_config_page.save_timezone_configuration()
        time_config_page.set_dst_with_save(original_dst_status)
