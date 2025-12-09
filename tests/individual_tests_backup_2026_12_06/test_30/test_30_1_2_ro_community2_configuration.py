"""
Test: 30.1.2 - SNMP Read-Only Community 2 Configuration
Category: SNMP Configuration (30)
Purpose: Verify second RO community string can be configured
Expected: Optional second community string field
Series: Both Series 2 and 3
Priority: MEDIUM
Hardware: Device Only
Based on: test_30_snmp_config.py
"""

import pytest
from pages.snmp_config_page import SNMPConfigPage
from playwright.sync_api import expect


def test_30_1_2_ro_community2_configuration(snmp_config_page: SNMPConfigPage):
    """
    Test 30.1.2: SNMP Read-Only Community 2 Configuration
    Purpose: Verify second RO community string can be configured
    Expected: Optional second community string field
    Series: Both 2 and 3
    """
    ro_community2 = snmp_config_page.page.locator("input[name='ro_community2']")
    if ro_community2.is_visible():
        expect(ro_community2).to_be_editable()
        ro_community2.fill("public2")
        assert ro_community2.input_value() == "public2"
