"""Test 19.2.1: Cancel button always enabled"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_2_1_cancel_button_always_enabled(unlocked_config_page: Page, base_url: str):
    """Test 19.2.1: Cancel button always enabled"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    cancel_btn = unlocked_config_page.get_by_role("button", name="Cancel")
    expect(cancel_btn).to_be_enabled()
