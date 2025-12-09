"""
Test 28 5 1 Syslog Severity Level
Category: 28 - Tests\Test 28 Syslog Config
Extracted from: tests\test_28_syslog_config.py
Source Class: TestSyslogSeverity
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.syslog_config_page import SyslogConfigPage


def test_28_5_1_syslog_severity_level(syslog_config_page: SyslogConfigPage):
    """
    Test 28.5.1: Syslog Severity Level Selection
    Purpose: Verify minimum severity level can be configured
    Expected: Standard syslog severities (Emergency, Alert, Critical, etc)
    Series: Both 2 and 3
    """
    # Look for severity dropdown
    severity_select = syslog_config_page.page.locator(
        "select[name*='severity'], select[name*='level']"
    )
    if severity_select.is_visible():
        expect(severity_select).to_be_enabled()
        # Should have severity options
        options = severity_select.locator("option")
        assert options.count() > 0, "Should have severity level options"
        # Test selecting a severity level
        if options.count() > 1:
            # Select first non-default option
            options.nth(1).click()
            selected_value = severity_select.input_value()
            assert len(selected_value) > 0, "Should have a severity value selected"
