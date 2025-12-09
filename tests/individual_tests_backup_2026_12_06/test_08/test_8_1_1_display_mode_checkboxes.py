"""
Category 8: Display Configuration - Test 8.1.1
Display Mode Checkboxes
Test Count: 1 of 13 in Category 8
Hardware: Device Only
Priority: MEDIUM - Front panel display settings
Series: Both Series 2 and 3
Based on test_08_display_config.py::TestDisplayModes::test_8_1_1_display_mode_checkboxes
"""

import pytest
from playwright.sync_api import Page, expect
from pages.display_config_page import DisplayConfigPage


def test_display_mode_checkboxes(display_config_page: DisplayConfigPage):
    """
    Test 8.1.1: Display Mode Checkboxes
    Purpose: Verify display mode checkboxes exist (5 modes)
    Expected: mode1, mode2, mode3, mode4, mode5 checkboxes available
    Fields: input[name='mode1'] through input[name='mode5']
    Series: Both 2 and 3
    """
    # Verify all 5 mode checkboxes exist
    for i in range(1, 6):
        checkbox = display_config_page.page.locator(f"input[name='mode{i}']")
        expect(checkbox).to_be_visible()
        # Should be checkbox type
        input_type = checkbox.get_attribute("type")
        assert input_type == "checkbox", f"mode{i} should be checkbox type"
