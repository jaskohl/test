"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.9.2: Button Tooltips on Hover
Hardware: Device Only
Series: Both Series 2 and 3
Extracted from test_19_dynamic_ui.py
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_9_2_button_tooltips_on_hover(unlocked_config_page: Page, base_url: str):
    """Test 19.9.2: Button tooltips appear on hover"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    save_btn = unlocked_config_page.get_by_role("button", name="Save")
    save_btn.hover()
    time.sleep(0.5)
