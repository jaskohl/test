"""
Test 19.3.3: Checkbox Toggles on Click
Category: 19 - Dynamic UI Behavior & Element Validation
Series: Both Series 2 and 3
Priority: MEDIUM
Hardware: Device Only

Based on COMPLETE_TEST_LIST.md Section 19
Extracted from: tests/test_19_dynamic_ui.py::TestFieldInteractions::test_19_3_3_checkbox_toggles_on_click
Preserved patterns: User-facing locators, device-aware testing, time.sleep() delays
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_3_3_checkbox_toggles_on_click(unlocked_config_page: Page, base_url: str):
    """Test 19.3.3: Checkboxes toggle on click"""
    unlocked_config_page.goto(f"{base_url}/gnss")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    galileo = unlocked_config_page.get_by_label("Galileo")
    if not galileo.is_visible():
        galileo = unlocked_config_page.locator("input[name='galileo']")

    if galileo.is_visible():
        was_checked = galileo.is_checked()
        galileo.click()
        is_checked = galileo.is_checked()
        assert was_checked != is_checked
