"""
Test 2.1.3: Time Section Accessible
Purpose: Verify time section navigation and timezone configuration availability

Category: 2 - Configuration Section Navigation
Test Type: Unit Test
Priority: HIGH
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_2_1_3_time_section_access(unlocked_config_page: Page, base_url: str):
    """Test 2.1.3: Time Section Accessible"""
    unlocked_config_page.goto(f"{base_url}/time")
    assert "time" in unlocked_config_page.url, "Should navigate to time page"
    # Verify timezone dropdown present
    unlocked_config_page.goto(f"{base_url}/time")
    assert "time" in unlocked_config_page.url, "Should navigate to time page"
    # Verify timezone dropdown present
    timezone_select = unlocked_config_page.locator("select[name='timezones']")
    expect(timezone_select).to_be_visible()
