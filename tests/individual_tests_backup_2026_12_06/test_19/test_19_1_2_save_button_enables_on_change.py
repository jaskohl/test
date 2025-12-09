"""Test 19.1.2: Save button enables when field changes"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_1_2_save_button_enables_on_change(
    unlocked_config_page: Page, base_url: str
):
    """Test 19.1.2: Save button enables when field changes"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(1)
    # IMPROVED: Use user-facing locator for better resilience
    identifier = unlocked_config_page.get_by_label("Device Identifier")
    if not identifier.is_visible():
        identifier = unlocked_config_page.locator("input[name='identifier']")

    identifier.fill("TEST-DEVICE")
    # FIXED: Add missing dispatch_event('change') per LOCATOR_STRATEGY.md requirement
    # Save buttons enable on onchange events (focus loss), triggered by dispatch_event('change')
    identifier.dispatch_event(
        "change"
    )  # CRITICAL: Triggers onchange event that calls changed('button_save')
    time.sleep(0.5)  # Allow JavaScript to execute
    # IMPROVED: Use user-facing locator
    save_btn = unlocked_config_page.get_by_role("button", name="Save")
    expect(save_btn).to_be_enabled()
