"""
Test 2.1.1: General Section Accessible
Purpose: Verify general section navigation and content availability

Category: 2 - Configuration Section Navigation
Test Type: Unit Test
Priority: HIGH
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_2_1_1_general_section_access(unlocked_config_page: Page, base_url: str):
    """Test 2.1.1: General Section Accessible"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(0.5)  # Brief pause to allow page to load
    # Verify URL and page content
    assert "general" in unlocked_config_page.url, "Should navigate to general page"
    # Verify key elements present
    identifier_field = unlocked_config_page.locator("input[name='identifier']")
    expect(identifier_field).to_be_visible()
