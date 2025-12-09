"""
Test 19.6.3: Table Column Headers Visible
Category 19: Dynamic UI Behavior & Element Validation - IMPROVED
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_6_3_table_column_headers_visible(logged_in_page: Page, base_url: str):
    """Test 19.6.3: Table column headers are visible"""
    logged_in_page.goto(f"{base_url}/")
    time.sleep(1)
    tables = logged_in_page.locator("table")
    if tables.count() > 0:
        headers = tables.first.locator("th")
        expect(headers.first).to_be_visible()
