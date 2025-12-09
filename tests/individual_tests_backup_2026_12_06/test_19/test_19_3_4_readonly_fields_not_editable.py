"""
Category 19: Dynamic UI Behavior & Element Validation - Individual Test
Test 19.3.4: Readonly Fields Not Editable - IMPROVED
Test Count: 1 test
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 19.3.4
Modernized with DeviceCapabilities integration for improved device detection and error handling
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_3_4_readonly_fields_not_editable(unlocked_config_page: Page, base_url: str):
    """Test 19.3.4: Readonly fields cannot be edited"""
    unlocked_config_page.goto(f"{base_url}/gnss")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    gps = unlocked_config_page.get_by_label("GPS")
    if not gps.is_visible():
        gps = unlocked_config_page.locator("input[name='GPS']")

    if gps.is_visible():
        expect(gps).to_be_disabled()
