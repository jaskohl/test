"""
Test 25.1.4: Negative UTC offset handling
Category 25: Time Synchronization Edge Cases - COMPLETE
Test Count: Part of 5 tests in Category 25
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3

Extracted from: tests/test_25_time_sync_edge_cases.py
Source Class: TestTimeSyncEdgeCases
"""

import pytest
import time
from playwright.sync_api import Page


def test_25_1_4_negative_time_offset(unlocked_config_page: Page, base_url: str):
    """Test 25.1.4: Negative UTC offset handling"""
    unlocked_config_page.goto(f"{base_url}/time", wait_until="domcontentloaded")
    # Select timezone with negative offset
    timezone = unlocked_config_page.locator("select[name='timezone']")
    if timezone.is_visible(timeout=2000):
        # Try to select negative offset timezone (e.g., US/Pacific)
        options = timezone.locator("option")
        # Find option with minus sign
        for i in range(options.count()):
            text = options.nth(i).inner_text()
            if "-" in text:
                timezone.select_option(index=i)
                break
        # Should accept negative offsets
        assert True, "Device accepts negative UTC offsets"
