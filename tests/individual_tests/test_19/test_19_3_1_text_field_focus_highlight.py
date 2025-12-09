"""Test 19.3.1: Text fields highlight on focus"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_3_1_text_field_focus_highlight(unlocked_config_page: Page, base_url: str):
    """Test 19.3.1: Text fields highlight on focus"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    identifier = unlocked_config_page.get_by_label("Device Identifier")
    if not identifier.is_visible():
        identifier = unlocked_config_page.locator("input[name='identifier']")

    identifier.focus()
    expect(identifier).to_be_focused()
