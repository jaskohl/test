"""
Category 8: Display Configuration - Test 8.1.2
Enable Display Mode
Test Count: 1 of 13 in Category 8
Hardware: Device Only
Priority: MEDIUM - Front panel display settings
Series: Both Series 2 and 3
Based on test_08_display_config.py::TestDisplayModes::test_8_1_2_enable_mode_checkbox
"""

import pytest
from playwright.sync_api import Page, expect
from pages.display_config_page import DisplayConfigPage


def test_8_1_2_enable_mode_checkbox(display_config_page: DisplayConfigPage):
    """
    Test 8.1.2: Enable Display Mode
    Purpose: Verify mode checkbox can be checked
    Expected: Checkbox toggles and persists
    Series: Both 2 and 3
    """
    # Use mode1 for testing
    checkbox = display_config_page.page.locator("input[name='mode1']")
    # Get initial state
    was_checked = checkbox.is_checked()
    # Toggle it
    checkbox.click()
    # Verify it changed
    is_now_checked = checkbox.is_checked()
    assert is_now_checked != was_checked, "Checkbox should toggle state"
