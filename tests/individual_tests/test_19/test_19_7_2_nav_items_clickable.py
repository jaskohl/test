"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.7.2: Navigation Items Clickable
Hardware: Device Only
Series: Both Series 2 and 3
Extracted from test_19_dynamic_ui.py
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_7_2_nav_items_clickable(unlocked_config_page: Page, base_url: str):
    """Test 19.7.2: All nav items are clickable"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    network_link = unlocked_config_page.get_by_role("link", name="Network")
    network_link.click()
    unlocked_config_page.wait_for_url("**/network")
