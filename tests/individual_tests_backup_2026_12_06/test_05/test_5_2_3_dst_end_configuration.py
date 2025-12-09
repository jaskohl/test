"""
Test: 5.2.3 - DST End Date Configuration
Category: Time Configuration (Category 5)
Purpose: Verify DST end date fields (week, day, month, time)
Expected: All 4 fields configurable
Series: Both Series 2 and 3
Priority: HIGH
Hardware: Device Only
Based on COMPLETE_TEST_LIST.md Section 5.2.3
Device exploration data: config_time.forms.json
"""

import pytest
from pages.time_config_page import TimeConfigPage
from playwright.sync_api import expect


def test_5_2_3_dst_end_configuration(time_config_page: TimeConfigPage):
    """
    Test 5.2.3: DST End Date Configuration
    Purpose: Verify DST end date fields (week, day, month, time)
    Expected: All 4 fields configurable
    Series: Both 2 and 3
    """
    # DST end week dropdown
    week_select = time_config_page.page.locator("select[name='dst_end_w']")
    expect(week_select).to_be_visible()
    week_select.select_option("1")  # 1st week
    # DST end day dropdown
    day_select = time_config_page.page.locator("select[name='dst_end_d']")
    expect(day_select).to_be_visible()
    day_select.select_option("0")  # Sunday
    # DST end month dropdown
    month_select = time_config_page.page.locator("select[name='dst_end_m']")
    expect(month_select).to_be_visible()
    month_select.select_option("11")  # November
    # DST end time field
    time_field = time_config_page.page.locator("input[name='dst_end_t']")
    expect(time_field).to_be_visible()
    time_field.fill("2:00")
    assert time_field.input_value() == "2:00"
