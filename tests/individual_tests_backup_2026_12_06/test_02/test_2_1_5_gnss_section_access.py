"""
Test 2.1.5: GNSS Section Accessible
Purpose: Verify GNSS section navigation and GPS configuration availability

Category: 2 - Configuration Section Navigation
Test Type: Unit Test
Priority: HIGH
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_2_1_5_gnss_section_access(unlocked_config_page: Page, base_url: str):
    """Test 2.1.5: GNSS Section Accessible"""
    unlocked_config_page.goto(f"{base_url}/gnss")
    assert "gnss" in unlocked_config_page.url, "Should navigate to GNSS page"
    # Verify GPS checkbox (always present and checked)
    gps_checkbox = unlocked_config_page.locator("input[value='1']")
    expect(gps_checkbox).to_be_visible()
