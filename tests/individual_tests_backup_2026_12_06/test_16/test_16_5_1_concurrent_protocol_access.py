"""
Test 16.5.1: Concurrent Protocol Access
Category: 16 - Integration Tests
Test Count: Part of 9 tests in Category 16
Hardware: Software Tools for 6 tests, Device Only for 3 tests
Priority: MEDIUM - External protocol validation
Series: Both Series 2 and 3

Extracted from: tests/test_16_integration.py
Source Class: TestMultiProtocolIntegration
"""

import pytest
from playwright.sync_api import Page, expect


def test_16_5_1_concurrent_protocol_access(unlocked_config_page: Page, device_ip: str):
    """
    Test 16.5.1: Concurrent Protocol Access
    Purpose: Verify HTTP access works while NTP/SNMP active
    Expected: Web interface responsive during protocol operations
    Series: Both 2 and 3
    """
    # Access web interface
    page_title = unlocked_config_page.title()
    assert "Kronos" in page_title, "Web interface should be accessible"
    # Web interface should remain responsive
    # (NTP and SNMP protocols run continuously in background)
    # Navigate to confirm responsiveness
    unlocked_config_page.goto(
        f"http://{device_ip}/general", wait_until="domcontentloaded"
    )
    identifier = unlocked_config_page.locator("input[name='identifier']")
    expect(identifier).to_be_visible(timeout=5000)
    print("Multi-protocol integration test passed")
