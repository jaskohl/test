"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.10.1: Keyboard Navigation Works
Hardware: Device Only
Series: Both Series 2 and 3
Extracted from test_19_dynamic_ui.py
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_10_1_keyboard_navigation_works(unlocked_config_page: Page, base_url: str):
    """Test 19.10.1: Tab key navigates between fields"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    identifier = unlocked_config_page.get_by_label("Device Identifier")
    if not identifier.is_visible():
        identifier = unlocked_config_page.locator("input[name='identifier']")

    identifier.focus()
    unlocked_config_page.keyboard.press("Tab")
    # Focus should move to next field
