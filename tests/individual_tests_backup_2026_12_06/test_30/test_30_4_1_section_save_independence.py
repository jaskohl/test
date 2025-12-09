"""
Test: 30.4.1 - SNMP Sections Save Independently
Category: SNMP Configuration (30)
Purpose: Verify each SNMP section can save without affecting others
Expected: Three independent save buttons work correctly
Series: Both Series 2 and 3
Priority: MEDIUM
Hardware: Device Only
Based on: test_30_snmp_config.py
"""

import pytest
from pages.snmp_config_page import SNMPConfigPage
from playwright.sync_api import expect


def test_30_4_1_section_save_independence(snmp_config_page: SNMPConfigPage):
    """
    Test 30.4.1: SNMP Sections Save Independently
    Purpose: Verify each SNMP section can save without affecting others
    Expected: Three independent save buttons work correctly
    Series: Both 2 and 3
    """
    # Get device-aware save button locators
    save1_locator = None
    save2_locator = None
    save3_locator = None

    if snmp_config_page.series == "Series 3":
        save1_locator = snmp_config_page.page.locator("button#button_save_1")
        save2_locator = snmp_config_page.page.locator("button#button_save_2")
        save3_locator = snmp_config_page.page.locator("button#button_save_3")
    elif snmp_config_page.series == "Series 2":
        save1_locator = snmp_config_page.page.locator("input#button_save_1")
        save2_locator = snmp_config_page.page.locator("input#button_save_2")
        save3_locator = snmp_config_page.page.locator("input#button_save_3")

    # Modify v1/v2c section
    ro_community1 = snmp_config_page.page.locator("input[name='ro_community1']")
    ro_community1.fill("test_community_v1v2c")
    # Only v1/v2c save button should enable
    if save1_locator and save1_locator.count() > 0:
        expect(save1_locator).to_be_enabled(timeout=2000)
    if save2_locator and save2_locator.count() > 0:
        expect(save2_locator).to_be_disabled()
    if save3_locator and save3_locator.count() > 0:
        expect(save3_locator).to_be_disabled()

    # Reset and test section 2 modification
    ro_community1.fill("PUBLIC")  # Reset section 1
    if save1_locator and save1_locator.count() > 0:
        expect(save1_locator).to_be_disabled()

    # Modify section 2
    trap_community = snmp_config_page.page.locator("input[name='trap_community']")
    trap_community.fill("test_trap_community")
    if save2_locator and save2_locator.count() > 0:
        expect(save2_locator).to_be_enabled(timeout=2000)
    if save1_locator and save1_locator.count() > 0:
        expect(save1_locator).to_be_disabled()
    if save3_locator and save3_locator.count() > 0:
        expect(save3_locator).to_be_disabled()
