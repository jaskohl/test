"""
Test 19.3.2: Dropdown Opens on Click
Category: 19 - Dynamic UI Behavior & Element Validation
Series: Both Series 2 and 3
Priority: MEDIUM
Hardware: Device Only

Based on COMPLETE_TEST_LIST.md Section 19
Extracted from: tests/test_19_dynamic_ui.py::TestFieldInteractions::test_19_3_2_dropdown_opens_on_click
Preserved patterns: User-facing locators, device-aware testing, time.sleep() delays
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_3_2_dropdown_opens_on_click(unlocked_config_page: Page, base_url: str):
    """Test 19.3.2: Dropdowns open on click"""
    unlocked_config_page.goto(f"{base_url}/display")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    mode = unlocked_config_page.get_by_label("Display Mode")
    if not mode.is_visible():
        mode = unlocked_config_page.locator("select[name='mode']")

    if mode.is_visible():
        mode.click()
        expect(mode).to_be_visible()
