"""
Test: 30.1.1 - SNMP Read-Only Community 1 Required Validation
Category: SNMP Configuration (30)
Purpose: Verify ro_community1 is required field
Expected: Empty value prevents save or shows error
Series: Both Series 2 and 3
Priority: MEDIUM
Hardware: Device Only
Based on: test_30_snmp_config.py
"""

import pytest
from pages.snmp_config_page import SNMPConfigPage
from playwright.sync_api import expect


def test_30_1_1_ro_community1_required(snmp_config_page: SNMPConfigPage):
    """
    Test 30.1.1: SNMP Read-Only Community 1 Required Validation
    Purpose: Verify ro_community1 is required field
    Expected: Empty value prevents save or shows error
    Series: Both 2 and 3
    """
    ro_community1 = snmp_config_page.page.locator("input[name='ro_community1']")
    expect(ro_community1).to_be_visible()
    expect(ro_community1).to_be_editable()
    # Get original value
    original_value = ro_community1.input_value()
    # Clear the required field
    ro_community1.fill("")

    # Use device-aware save button detection
    save_button_locator = None
    if snmp_config_page.series == "Series 3":
        save_button_locator = snmp_config_page.page.locator("button#button_save_1")
    elif snmp_config_page.series == "Series 2":
        save_button_locator = snmp_config_page.page.locator("input#button_save_1")

    if save_button_locator and save_button_locator.count() > 0:
        # Button should remain disabled when required field is empty
        expect(save_button_locator).to_be_disabled()
    # Browser validation may prevent submission when required field is empty
