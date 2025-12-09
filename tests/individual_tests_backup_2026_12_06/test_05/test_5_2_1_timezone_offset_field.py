"""
Category 5: Time Configuration - Test 5.1.2
Timezone Offset Field
Test Count: 1 of 32 in Category 5
Hardware: Device Only
Priority: HIGH - Critical time synchronization settings
Series: Both Series 2 and 3
Based on test_05_time_config.py::TestTimezoneConfiguration::test_5_1_2_timezone_offset_field
Device exploration data: config_time.forms.json
IMPORTANT: Time page has TWO sections with separate save buttons
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.time_config_page import TimeConfigPage


def test_5_2_1_timezone_offset_field(time_config_page: TimeConfigPage):
    """
    Test 5.1.2: Timezone Offset Field
    Purpose: Verify timezone offset field accepts valid formats
    Expected: Accepts +/-HH:MM format
    Series: Both 2 and 3
    """
    # Test offset field
    offset_field = time_config_page.page.locator("input[name='offset']")
    expect(offset_field).to_be_visible()
    expect(offset_field).to_be_editable()
    # Test valid offset
    offset_field.fill("+05:00")
    assert offset_field.input_value() == "+05:00"
