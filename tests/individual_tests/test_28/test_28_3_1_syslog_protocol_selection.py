"""
Test 28 3 1 Syslog Protocol Selection
Category: 28 - Tests\Test 28 Syslog Config
Extracted from: tests\test_28_syslog_config.py
Source Class: TestSyslogProtocol
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.syslog_config_page import SyslogConfigPage


def test_28_3_1_syslog_protocol_selection(syslog_config_page: SyslogConfigPage):
    """
    Test 28.3.1: Syslog Protocol Selection (UDP/TCP)
    Purpose: Verify syslog protocol can be selected
    Expected: UDP and/or TCP options available
    Series: Both 2 and 3
    NOTE: Device has protocol_a and protocol_b selects - use .first to avoid strict mode
    """
    # Device has select[name='protocol_a'] and select[name='protocol_b']
    # Use .first to get protocol_a
    protocol_select = syslog_config_page.page.locator("select[name*='protocol']").first
    expect(protocol_select).to_be_visible()
    expect(protocol_select).to_be_enabled()
    # Check for UDP/TCP options
    options = protocol_select.locator("option")
    option_texts = []
    for i in range(options.count()):
        option_texts.append(options.nth(i).inner_text())
    # Should have protocol options
    assert any(
        "UDP" in text or "TCP" in text for text in option_texts
    ), "Should have UDP or TCP protocol options"
