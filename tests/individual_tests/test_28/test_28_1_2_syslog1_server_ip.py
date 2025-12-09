"""
Test 28 1 2 Syslog1 Server IP
Category: 28 - Tests\Test 28 Syslog Config
Extracted from: tests\test_28_syslog_config.py
Source Class: TestSyslogTarget1
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.syslog_config_page import SyslogConfigPage


def test_28_1_2_syslog1_server_ip(syslog_config_page: SyslogConfigPage):
    """
    Test 28.1.2: Syslog Target 1 Server IP
    Purpose: Verify syslog server IP address field
    Expected: Accepts valid IPv4 addresses
    Series: Both 2 and 3
    """
    # Look for syslog server IP field (first target)
    server_ip = syslog_config_page.page.locator(
        "input[name*='syslog'][type='text'], input[name*='server']"
    ).first
    if server_ip.is_visible():
        expect(server_ip).to_be_editable()
        # Test valid IP
        server_ip.fill("192.168.1.100")
        assert server_ip.input_value() == "192.168.1.100"
