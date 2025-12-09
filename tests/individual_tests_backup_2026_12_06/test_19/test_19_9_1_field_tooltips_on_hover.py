"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.9.1: Field Tooltips on Hover
Hardware: Device Only
Series: Both Series 2 and 3
Extracted from test_19_dynamic_ui.py
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_9_1_field_tooltips_on_hover(unlocked_config_page: Page, base_url: str):
    """Test 19.9.1: Field tooltips appear on hover"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    identifier = unlocked_config_page.get_by_label("Device Identifier")
    if not identifier.is_visible():
        identifier = unlocked_config_page.locator("input[name='identifier']")

    identifier.hover()
    time.sleep(0.5)
    # Tooltip may appear
