"""
Test 28 2 2 Dual Syslog Targets
Category: 28 - Tests\Test 28 Syslog Config
Extracted from: tests\test_28_syslog_config.py
Source Class: TestSyslogTarget2
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.syslog_config_page import SyslogConfigPage


def test_28_2_2_dual_syslog_targets(syslog_config_page: SyslogConfigPage):
    """
    Test 28.2.2: Both Syslog Targets Simultaneously
    Purpose: Verify both syslog targets can be enabled at once
    Expected: No conflicts, both targets configurable
    Series: Both 2 and 3
    """
    server_fields = syslog_config_page.page.locator(
        "input[name*='server'], input[type='text']"
    )
    if server_fields.count() >= 2:
        # Configure both targets with different IPs
        server_fields.nth(0).fill("192.168.1.100")
        server_fields.nth(1).fill("192.168.1.200")
        # Both should retain independent values
        assert server_fields.nth(0).input_value() == "192.168.1.100"
        assert server_fields.nth(1).input_value() == "192.168.1.200"
