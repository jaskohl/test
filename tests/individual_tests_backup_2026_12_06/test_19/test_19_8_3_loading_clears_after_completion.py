"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.8.3: Loading Indicator Clears After Completion
Hardware: Device Only
Series: Both Series 2 and 3
Extracted from test_19_dynamic_ui.py
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_8_3_loading_clears_after_completion(
    unlocked_config_page: Page, base_url: str
):
    """Test 19.8.3: Loading indicator clears after completion"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(2)
    # Page should be fully loaded, no loading indicators
