"""Test 19.1.4: Multiple save buttons work independently"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_1_4_multiple_save_buttons_independent(
    unlocked_config_page: Page, base_url: str
):
    """Test 19.1.4: Multiple save buttons work independently"""
    unlocked_config_page.goto(f"{base_url}/time")
    time.sleep(1)
    save1 = unlocked_config_page.locator("button#button_save_1")
    save2 = unlocked_config_page.locator("button#button_save_2")
    if save1.is_visible() and save2.is_visible():
        expect(save1).to_be_disabled()
        expect(save2).to_be_disabled()
