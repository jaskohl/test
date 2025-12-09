"""
Test: 5.2.2 - DST Begin Date Configuration
Category: Time Configuration (Category 5)
Purpose: Verify DST begin date fields (week, day, month, time)
Expected: All 4 fields configurable
Series: Both Series 2 and 3
Priority: HIGH
Hardware: Device Only
Based on COMPLETE_TEST_LIST.md Section 5.2.2
Device exploration data: config_time.forms.json
"""

import pytest
from pages.time_config_page import TimeConfigPage
from playwright.sync_api import expect


def test_5_2_2_dst_begin_configuration(time_config_page: TimeConfigPage):
    """
    Test 5.2.2: DST Begin Date Configuration
    Purpose: Verify DST begin date fields (week, day, month, time)
    Expected: All 4 fields configurable
    Series: Both 2 and 3
    """
    # DST begin week dropdown
    week_select = time_config_page.page.locator("select[name='dst_begin_w']")
    expect(week_select).to_be_visible()
    week_select.select_option("2")  # 2nd week
    # DST begin day dropdown
    day_select = time_config_page.page.locator("select[name='dst_begin_d']")
    expect(day_select).to_be_visible()
    day_select.select_option("0")  # Sunday
    # DST begin month dropdown
    month_select = time_config_page.page.locator("select[name='dst_begin_m']")
    expect(month_select).to_be_visible()
    month_select.select_option("3")  # March
    # DST begin time field
    time_field = time_config_page.page.locator("input[name='dst_begin_t']")
    expect(time_field).to_be_visible()
    time_field.fill("2:00")
    assert time_field.input_value() == "2:00"
