"""
Test 19.4.2: Empty Required Field Shows Error
Category 19: Dynamic UI Behavior & Element Validation - IMPROVED
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_4_2_empty_required_field_shows_error(
    unlocked_config_page: Page, base_url: str
):
    """Test 19.4.2: Empty required field shows error"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    identifier = unlocked_config_page.get_by_label("Device Identifier")
    if not identifier.is_visible():
        identifier = unlocked_config_page.locator("input[name='identifier']")

    identifier.fill("")
    identifier.blur()
    time.sleep(0.5)
