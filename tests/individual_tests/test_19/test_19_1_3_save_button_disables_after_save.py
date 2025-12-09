"""
Test 19.1.3: Save button disables after successful save
Category 19: Dynamic UI Behavior & Element Validation
Hardware: Device Only
Series: Both Series 2 and 3
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_1_3_save_button_disables_after_save(
    unlocked_config_page: Page, base_url: str
):
    """Test 19.1.3: Save button disables after successful save"""
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
            time.sleep(2)
            expect(save_btn).to_be_disabled()
