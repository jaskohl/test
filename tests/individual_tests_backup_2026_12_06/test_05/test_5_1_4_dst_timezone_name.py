"""
Category 5: Time Configuration - Test 5.1.4
DST Timezone Name Configuration
Test Count: 1 of 32 in Category 5
Hardware: Device Only
Priority: HIGH - Critical time synchronization settings
Series: Both Series 2 and 3
Based on test_05_time_config.py::TestTimezoneConfiguration::test_5_1_4_dst_timezone_name
Device exploration data: config_time.forms.json
IMPORTANT: Time page has TWO sections with separate save buttons
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.time_config_page import TimeConfigPage


def test_dst_timezone_name(time_config_page: TimeConfigPage):
    """
    Test 5.1.4: DST Timezone Name Configuration
    Purpose: Verify daylight saving time name field (e.g., "CDT")
    Expected: Accepts 3-4 character timezone abbreviations
    Series: Both 2 and 3
    """
    dst_name_field = time_config_page.page.locator("input[name='dst_name']")
    expect(dst_name_field).to_be_visible()
    expect(dst_name_field).to_be_editable()
    # Test DST timezone name
    dst_name_field.fill("EDT")
    assert dst_name_field.input_value() == "EDT"
