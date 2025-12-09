"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.8.2: Loading Indicator During Page Load
Hardware: Device Only
Series: Both Series 2 and 3
Extracted from test_19_dynamic_ui.py
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_8_2_loading_indicator_during_page_load(
    unlocked_config_page: Page, base_url: str
):
    """Test 19.8.2: Loading indicator during page navigation"""
    unlocked_config_page.goto(f"{base_url}/general")
    # IMPROVED: Use user-facing locator
    network_link = unlocked_config_page.get_by_role("link", name="Network")
    expect(network_link).to_be_visible()
    expect(network_link).to_be_enabled()
    network_link.click()
    unlocked_config_page.wait_for_url("**/network")
    # Brief loading state during navigation
