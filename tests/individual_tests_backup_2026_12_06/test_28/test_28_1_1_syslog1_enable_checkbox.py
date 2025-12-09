"""
Test 28 1 1 Syslog1 Enable Checkbox
Category: 28 - Tests\Test 28 Syslog Config
Extracted from: tests\test_28_syslog_config.py
Source Class: TestSyslogTarget1
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.syslog_config_page import SyslogConfigPage


def test_28_1_1_syslog1_enable_checkbox(syslog_config_page: SyslogConfigPage):
    """
    Test 28.1.1: Syslog Target 1 Enable
    Purpose: Verify first syslog target can be enabled/disabled
    Expected: Checkbox toggles syslog1 functionality
    Series: Both 2 and 3
    """
    # Look for syslog enable checkbox (target 1)
    syslog1_enable = syslog_config_page.page.locator(
        "input[name*='syslog'][type='checkbox'], input[name*='enable'][type='checkbox']"
    ).first
    if syslog1_enable.is_visible():
        expect(syslog1_enable).to_be_enabled()
        # Toggle checkbox
        was_checked = syslog1_enable.is_checked()
        syslog1_enable.click()
        assert syslog1_enable.is_checked() != was_checked, "Checkbox should toggle"
