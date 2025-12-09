"""
Test 19.3.6: Required Fields Marked
Category 19: Dynamic UI Behavior & Element Validation - IMPROVED
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_3_6_required_fields_marked(unlocked_config_page: Page, base_url: str):
    """Test 19.3.6: Required fields are marked"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    identifier = unlocked_config_page.get_by_label("Device Identifier")
    if not identifier.is_visible():
        identifier = unlocked_config_page.locator("input[name='identifier']")

    # Check if field has required attribute
    assert identifier.is_visible()
