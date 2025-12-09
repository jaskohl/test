"""
Test 28 6 2 Syslog Cancel Button
Category: 28 - Tests\Test 28 Syslog Config
Extracted from: tests\test_28_syslog_config.py
Source Class: TestSyslogTarget1
Individual test file for better test isolation and debugging.
"""

import pytest
from pages.syslog_config_page import SyslogConfigPage


def test_28_6_2_syslog_cancel_button(syslog_config_page: SyslogConfigPage):
    """
    Test 28.6.2: Syslog Cancel Button Reverts Changes
    Purpose: Verify cancel reverts syslog configuration changes
    Expected: Fields return to form defaults (empty for target_a)
    Series: Both 2 and 3
    Note: Cancel resets to form defaults, not saved configuration
    """
    # Make change using page object method
    syslog_config_page.configure_syslog(target_a="10.0.0.99")
    # Verify change was applied
    changed_data = syslog_config_page.get_page_data()
    assert changed_data["target_a"] == "10.0.0.99", "Target A should be changed"
    # Use cancel button to revert changes
    syslog_config_page.cancel_configuration()
    # Verify cancel reset to form defaults (empty for target_a)
    cancelled_data = syslog_config_page.get_page_data()
    assert (
        cancelled_data["target_a"] == ""
    ), "Target A should be reset to empty (form default)"
