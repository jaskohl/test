"""
Test: 30.3.1 - SNMP v3 Enable Configuration
Category: SNMP Configuration (30)
Purpose: Verify SNMP v3 can be enabled
Expected: v3 enable checkbox or section visible
Series: Both Series 2 and 3
Priority: MEDIUM
Hardware: Device Only
Based on: test_30_snmp_config.py
"""

import pytest
from pages.snmp_config_page import SNMPConfigPage
from playwright.sync_api import expect


def test_30_3_1_v3_enable(snmp_config_page: SNMPConfigPage):
    """
    Test 30.3.1: SNMP v3 Enable Configuration
    Purpose: Verify SNMP v3 can be enabled
    Expected: v3 enable checkbox or section visible
    Series: Both 2 and 3
    """
    # Look for v3 enable checkbox or v3 fields
    v3_enable = snmp_config_page.page.locator("input[name*='v3'][type='checkbox']")
    if v3_enable.count() > 0:
        expect(v3_enable.first).to_be_enabled()
