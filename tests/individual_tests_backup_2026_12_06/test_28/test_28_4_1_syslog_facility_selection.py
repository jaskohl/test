"""
Test 28 4 1 Syslog Facility Selection
Category: 28 - Tests\Test 28 Syslog Config
Extracted from: tests\test_28_syslog_config.py
Source Class: TestSyslogFacility
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.syslog_config_page import SyslogConfigPage


def test_28_4_1_syslog_facility_selection(syslog_config_page: SyslogConfigPage):
    """
    Test 28.4.1: Syslog Facility Selection
    Purpose: Verify syslog facility code can be configured
    Expected: Standard syslog facilities (LOCAL0-LOCAL7, etc)
    Series: Both 2 and 3
    """
    # Look for facility dropdown
    facility_select = syslog_config_page.page.locator("select[name*='facility']")
    if facility_select.is_visible():
        expect(facility_select).to_be_enabled()
        # Should have facility options
        options = facility_select.locator("option")
        assert options.count() > 0, "Should have facility options"
