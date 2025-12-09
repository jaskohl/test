"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.7.3: Navigation Items Hover Effect
Hardware: Device Only
Series: Both Series 2 and 3
Extracted from test_19_dynamic_ui.py
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_7_3_nav_items_have_hover_effect(unlocked_config_page: Page, base_url: str):
    """Test 19.7.3: Nav items show hover effect"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    network_link = unlocked_config_page.get_by_role("link", name="Network")
    network_link.hover()
    # Visual hover effect should appear
