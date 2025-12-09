"""
Test 28 7 1 Syslog Configuration Persists
Category: 28 - Tests\Test 28 Syslog Config
Extracted from: tests\test_28_syslog_config.py
Source Class: TestSyslogTarget1
Individual test file for better test isolation and debugging.
"""

import pytest
import time
from pages.syslog_config_page import SyslogConfigPage


def test_28_7_1_syslog_configuration_persists(syslog_config_page: SyslogConfigPage):
    """
    Test 28.7.1: Syslog Configuration Persistence
    Purpose: Verify syslog settings persist after save and reload
    Expected: Configuration survives page reload
    Series: Both 2 and 3
    """
    # Get original configuration
    original_data = syslog_config_page.get_page_data()
    original_target_a = original_data.get("target_a", "")
    # Make a change using page object method (triggers JavaScript events)
    test_server = "192.168.10.50"
    syslog_config_page.configure_syslog(target_a=test_server)
    # Allow time for JavaScript to process change events and enable save button
    time.sleep(0.5)
    # Verify save button is enabled before attempting to save
    assert (
        syslog_config_page.is_save_button_enabled()
    ), "Save button should be enabled after configuration changes"
    # Save configuration
    syslog_config_page.save_configuration()
    # Reload page
    syslog_config_page.navigate_to_page()
    # Verify persistence
    reloaded_data = syslog_config_page.get_page_data()
    assert (
        reloaded_data["target_a"] == test_server
    ), "Syslog target A should persist after save and reload"
    # Reset to original configuration
    syslog_config_page.configure_syslog(target_a=original_target_a)
    time.sleep(0.5)
    if syslog_config_page.is_save_button_enabled():
        syslog_config_page.save_configuration()
