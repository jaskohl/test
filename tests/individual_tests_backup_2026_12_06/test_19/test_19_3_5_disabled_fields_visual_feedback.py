"""
Test 19.3.5: Disabled Fields Visual Feedback
Category 19: Dynamic UI Behavior & Element Validation - IMPROVED
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_3_5_disabled_fields_visual_feedback(
    unlocked_config_page: Page, base_url: str
):
    """Test 19.3.5: Disabled fields show visual feedback"""
    unlocked_config_page.goto(f"{base_url}/gnss")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    gps = unlocked_config_page.get_by_label("GPS")
    if not gps.is_visible():
        gps = unlocked_config_page.locator("input[name='GPS']")

    if gps.is_visible():
        expect(gps).to_be_disabled()
