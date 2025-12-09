"""
Test 28 1 3 Syslog1 Port Configuration
Category: 28 - Tests\Test 28 Syslog Config
Extracted from: tests\test_28_syslog_config.py
Source Class: TestSyslogTarget1
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.syslog_config_page import SyslogConfigPage


def test_28_1_3_syslog1_port_configuration(syslog_config_page: SyslogConfigPage):
    """
    Test 28.1.3: Syslog Target 1 Port Configuration
    Purpose: Verify syslog port field (default 514)
    Expected: Accepts valid port numbers
    Series: Both 2 and 3
    """
    # Look for port field
    port_field = syslog_config_page.page.locator("input[name*='port']").first
    if port_field.is_visible():
        expect(port_field).to_be_editable()
        # Test default port
        port_field.fill("514")
        assert port_field.input_value() == "514"
        # Test custom port
        port_field.fill("1514")
        assert port_field.input_value() == "1514"
