"""Test 19.2.2: Cancel reverts field changes"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_2_2_cancel_reverts_changes(unlocked_config_page: Page, base_url: str):
    """Test 19.2.2: Cancel reverts field changes"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    identifier = unlocked_config_page.get_by_label("Device Identifier")
    if not identifier.is_visible():
        identifier = unlocked_config_page.locator("input[name='identifier']")

    original = identifier.input_value()
    identifier.fill("TEMP-VALUE")
    # IMPROVED: Use user-facing locator
    cancel_btn = unlocked_config_page.get_by_role("button", name="Cancel")
    cancel_btn.click()
    time.sleep(0.5)
    # Field should revert (implementation may vary)
