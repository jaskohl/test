"""
Test 17.4.2: UI works at 1366x768
Category: 17 - Cross-Browser & Responsive Tests
Test Count: Part of 5 tests in Category 17
Hardware: Device Only
Priority: LOW
Series: Both Series 2 and 3

Extracted from: tests/test_17_cross_browser.py
Source Class: TestResponsiveDesign
"""

import pytest
from playwright.sync_api import Page, expect


def test_17_4_2_laptop_resolution(logged_in_page: Page, base_url: str):
    """Test 17.4.2: UI works at 1366x768"""
    logged_in_page.set_viewport_size({"width": 1366, "height": 768})
    logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")
    # UI should remain usable
    tables = logged_in_page.locator("table")
    expect(tables.first).to_be_visible()
