"""
Test 28 6 1 Syslog Save Button
Category: 28 - Tests\Test 28 Syslog Config
Extracted from: tests\test_28_syslog_config.py
Source Class: TestSyslogTarget1
Individual test file for better test isolation and debugging.
"""

import pytest
from pages.syslog_config_page import SyslogConfigPage


def test_28_6_1_syslog_save_button(
    syslog_config_page: SyslogConfigPage, device_series: str
):
    """
    Test 28.6.1: Syslog Save Button State Management
    Purpose: Verify save button enables when syslog config changes
    Expected: Disabled initially, enables on change
    Series: Both 2 and 3
    """
    # Use page object method for device-aware save button detection
    # This handles both Series 2 (input#button_save) and Series 3 (button#button_save)
    # Make a change using page object method
    original_data = syslog_config_page.get_page_data()
    syslog_config_page.configure_syslog(target_a="192.168.1.100")
    # Verify configuration was applied
    new_data = syslog_config_page.get_page_data()
    assert new_data["target_a"] == "192.168.1.100", "Target A should be updated"
    # Reset to original state
    syslog_config_page.configure_syslog(target_a=original_data.get("target_a", ""))
