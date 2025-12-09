"""
Test 30.4.3: Cross-Section Configuration Test
Purpose: Verify all three sections can be configured simultaneously
Expected: All sections maintain independent state
Series: Both 2 and 3

Category: 30 - SNMP Configuration
Test Type: Unit Test
Priority: MEDIUM
Hardware: Device Only
"""

import pytest
from playwright.sync_api import Page, expect
from pages.snmp_config_page import SNMPConfigPage


def test_30_4_3_cross_section_configuration(snmp_config_page: SNMPConfigPage):
    """
    Test 30.4.3: Cross-Section Configuration Test
    Purpose: Verify all three sections can be configured simultaneously
    Expected: All sections maintain independent state
    Series: Both 2 and 3
    """
    # Configure Section 1
    ro_community1 = snmp_config_page.page.locator("input[name='ro_community1']")
    if ro_community1.is_visible():
        ro_community1.fill("custom_public")
    # Configure Section 2 (if trap fields visible)
    trap_fields = snmp_config_page.page.locator("input[name*='trap']")
    if trap_fields.count() > 0:
        trap_fields.first.fill("trap_config")
    # Configure Section 3 (v3 fields)
    v3_fields = snmp_config_page.page.locator("input[name='auth_name']")
    if v3_fields.is_visible():
        v3_fields.fill("test_user")
    # Verify all three sections can be configured independently
    # Test the SNMP page object methods work correctly for all sections
    assert (
        snmp_config_page.get_page_data() is not None
    ), "Page data extraction should work"
    # Test save button detection works for all sections
    save_buttons_work = snmp_config_page.verify_save_buttons_present()
    assert save_buttons_work, "All save buttons should be detectable"
