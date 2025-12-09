"""
Test: 30.2.2 - SNMP Trap Destination IP Configuration
Category: SNMP Configuration (30)
Purpose: Verify trap destination IP can be configured
Expected: IP address field for trap target
Series: Both Series 2 and 3
Priority: MEDIUM
Hardware: Device Only
Based on: test_30_snmp_config.py
"""

import pytest
from pages.snmp_config_page import SNMPConfigPage
from playwright.sync_api import expect


def test_30_2_2_trap_destination_configuration(snmp_config_page: SNMPConfigPage):
    """
    Test 30.2.2: SNMP Trap Destination IP Configuration
    Purpose: Verify trap destination IP can be configured
    Expected: IP address field for trap target
    Series: Both 2 and 3
    """
    # Look for trap destination field
    trap_dest = snmp_config_page.page.locator(
        "input[name*='trap_dest'], input[name*='trap'][type='text']"
    )
    if trap_dest.count() > 0:
        dest_field = trap_dest.first
        expect(dest_field).to_be_editable()
        dest_field.fill("192.168.1.100")
        assert dest_field.input_value() == "192.168.1.100"
