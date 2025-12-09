"""
Test 17.4.1: UI works at 1920x1080
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


def test_17_4_1_desktop_resolution(logged_in_page: Page, base_url: str):
    """Test 17.4.1: UI works at 1920x1080"""
    logged_in_page.set_viewport_size({"width": 1920, "height": 1080})
    logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")
    # Dashboard should be fully visible
    tables = logged_in_page.locator("table")
    expect(tables.first).to_be_visible()
