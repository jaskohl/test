"""Test 19.1.1: Save buttons start disabled"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_1_1_save_button_initially_disabled(
    unlocked_config_page: Page, base_url: str
):
    """Test 19.1.1: Save buttons start disabled"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(1)
    # IMPROVED: Use user-facing locator instead of CSS selector
    save_btn = unlocked_config_page.get_by_role("button", name="Save")
    expect(save_btn).to_be_disabled()
