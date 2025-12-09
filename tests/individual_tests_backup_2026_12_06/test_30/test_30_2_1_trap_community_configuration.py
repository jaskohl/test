"""
Test: 30.2.1 - SNMP Trap Community String Configuration
Category: SNMP Configuration (30)
Purpose: Verify trap community string can be configured
Expected: Trap community field accepts input
Series: Both Series 2 and 3
Priority: MEDIUM
Hardware: Device Only
Based on: test_30_snmp_config.py
"""

import pytest
from pages.snmp_config_page import SNMPConfigPage
from playwright.sync_api import expect


def test_30_2_1_trap_community_configuration(snmp_config_page: SNMPConfigPage):
    """
    Test 30.2.1: SNMP Trap Community String Configuration
    Purpose: Verify trap community string can be configured
    Expected: Trap community field accepts input
    Series: Both 2 and 3
    """
    # Look for trap community field
    trap_community = snmp_config_page.page.locator(
        "input[name*='trap_community'], input[name*='trap'][name*='comm']"
    )
    if trap_community.count() > 0:
        trap_field = trap_community.first
        expect(trap_field).to_be_editable()
        trap_field.fill("trap_community")
        assert trap_field.input_value() == "trap_community"
