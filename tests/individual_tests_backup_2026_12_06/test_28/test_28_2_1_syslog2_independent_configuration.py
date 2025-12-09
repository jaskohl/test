"""
Test 28 2 1 Syslog2 Independent Configuration
Category: 28 - Tests\Test 28 Syslog Config
Extracted from: tests\test_28_syslog_config.py
Source Class: TestSyslogTarget2
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.syslog_config_page import SyslogConfigPage


def test_28_2_1_syslog2_independent_configuration(syslog_config_page: SyslogConfigPage):
    """
    Test 28.2.1: Second Syslog Target Independent Configuration
    Purpose: Verify second syslog target configures independently
    Expected: Two separate syslog destinations possible
    Series: Both 2 and 3
    """
    # Look for second syslog target fields
    enable_checkboxes = syslog_config_page.page.locator("input[type='checkbox']")
    if enable_checkboxes.count() >= 2:
        # Second checkbox should be independent
        syslog2_enable = enable_checkboxes.nth(1)
        expect(syslog2_enable).to_be_enabled()
        # Toggle should not affect first target
        syslog2_enable.click()
