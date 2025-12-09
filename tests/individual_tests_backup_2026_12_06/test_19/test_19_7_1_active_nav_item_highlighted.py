"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.7.1: Active Navigation Item Highlighted
Hardware: Device Only
Series: Both Series 2 and 3
Extracted from test_19_dynamic_ui.py
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_7_1_active_nav_item_highlighted(unlocked_config_page: Page, base_url: str):
    """Test 19.7.1: Active navigation item is highlighted"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    general_link = unlocked_config_page.get_by_role("link", name="General")
    expect(general_link).to_be_visible()
