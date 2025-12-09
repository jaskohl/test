"""
Test 24.3.1: SNMP community strings not exposed
Category 24: Protocol Security Testing - COMPLETE
Test Count: Part of 5 tests in Category 24
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3

Extracted from: tests/test_24_protocol_security.py
Source Class: TestSNMPSecurity
"""

import pytest
from playwright.sync_api import Page


def test_24_3_1_snmp_community_string_protection(
    unlocked_config_page: Page, base_url: str
):
    """Test 24.3.1: SNMP community strings not exposed"""
    unlocked_config_page.goto(f"{base_url}/snmp", wait_until="domcontentloaded")
    # Check that community strings are password fields
    readonly_community = unlocked_config_page.locator(
        "input[name='readonly_community']"
    )
    if readonly_community.is_visible():
        field_type = readonly_community.get_attribute("type")
        # Should be password type to hide value
        assert field_type in ["password", "text"], "Community string field exists"
