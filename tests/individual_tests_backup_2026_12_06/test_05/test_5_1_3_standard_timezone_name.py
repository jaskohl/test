"""
Test: 5.1.3 - Standard Timezone Name Configuration
Category: Time Configuration (Category 5)
Purpose: Verify standard time name field (e.g., "CST")
Expected: Accepts 3-4 character timezone abbreviations
Series: Both Series 2 and 3
Priority: HIGH
Hardware: Device Only
Based on COMPLETE_TEST_LIST.md Section 5.1.3
Device exploration data: config_time.forms.json
"""

import pytest
from pages.time_config_page import TimeConfigPage
from playwright.sync_api import expect


def test_5_1_3_standard_timezone_name(time_config_page: TimeConfigPage):
    """
    Test 5.1.3: Standard Timezone Name Configuration
    Purpose: Verify standard time name field (e.g., "CST")
    Expected: Accepts 3-4 character timezone abbreviations
    Series: Both 2 and 3
    """
    std_name_field = time_config_page.page.locator("input[name='std_name']")
    expect(std_name_field).to_be_visible()
    expect(std_name_field).to_be_editable()
    # Test standard timezone name
    std_name_field.fill("EST")
    assert std_name_field.input_value() == "EST"
