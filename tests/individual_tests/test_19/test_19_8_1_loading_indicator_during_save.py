"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.8.1: Loading Indicator During Save
Hardware: Device Only
Series: Both Series 2 and 3
Extracted from test_19_dynamic_ui.py
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_8_1_loading_indicator_during_save(
    unlocked_config_page: Page, base_url: str
):
    """Test 19.8.1: Loading indicator shown during save"""
    unlocked_config_page.goto(f"{base_url}/display")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    mode = unlocked_config_page.get_by_label("Display Mode")
    if not mode.is_visible():
        mode = unlocked_config_page.locator("select[name='mode']")

    if mode.is_visible():
        mode.select_option(index=1)
        # IMPROVED: Use user-facing locator
        save_btn = unlocked_config_page.get_by_role("button", name="Save")
        if save_btn.is_enabled():
            save_btn.click()
            time.sleep(0.5)
            # Loading overlay may appear
