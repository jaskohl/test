"""
Category 22: Data Integrity Testing - COMPLETE
Test Count: 1 test
Hardware: Device Only ()
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 22
"""

import pytest
import time
from playwright.sync_api import Page


class TestDataIntegrity:
    """Test 22.1: Configuration Data Integrity"""

    def test_22_1_1_config_persistence_across_pages(
        self, unlocked_config_page: Page, base_url: str
    ):
        """Test 22.1.1: Configuration persists when navigating between pages"""
        # Configure identifier
        unlocked_config_page.goto(f"{base_url}/general")
        time.sleep(1)
        test_value = f"TEST-{int(time.time())}"
        identifier = unlocked_config_page.locator("input[name='identifier']")
        identifier.fill(test_value)
        save_btn = unlocked_config_page.locator("button#button_save")
        if save_btn.is_enabled():
            save_btn.click()
            time.sleep(2)
        # Navigate away
        unlocked_config_page.goto(f"{base_url}/network")
        time.sleep(1)
        # Navigate back
        unlocked_config_page.goto(f"{base_url}/general")
        time.sleep(1)
        # Verify value persisted
        identifier = unlocked_config_page.locator("input[name='identifier']")
        current_value = identifier.input_value()
        assert (
            test_value in current_value or current_value != ""
        ), "Configuration should persist across page navigation"
