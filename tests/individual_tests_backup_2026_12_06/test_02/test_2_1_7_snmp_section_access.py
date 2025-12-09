"""
Test 2.1.7: SNMP Section Accessible
Purpose: Verify SNMP section navigation and community string configuration availability

Category: 2 - Configuration Section Navigation
Test Type: Unit Test
Priority: HIGH
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_2_1_7_snmp_section_access(unlocked_config_page: Page, base_url: str):
    """Test 2.1.7: SNMP Section Accessible"""
    unlocked_config_page.goto(f"{base_url}/snmp")
    assert "snmp" in unlocked_config_page.url, "Should navigate to SNMP page"
    # Verify SNMP configuration fields
    ro_community_field = unlocked_config_page.locator("input[name='ro_community1']")
    expect(ro_community_field).to_be_visible()
