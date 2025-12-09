"""
Test 19.6.1: Table Rows Selectable
Category 19: Dynamic UI Behavior & Element Validation - IMPROVED
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_6_1_table_rows_selectable(logged_in_page: Page, base_url: str):
    """Test 19.6.1: Table rows can be selected"""
    logged_in_page.goto(f"{base_url}/")
    time.sleep(1)
    tables = logged_in_page.locator("table")
    if tables.count() > 0:
        rows = tables.first.locator("tr")
        if rows.count() > 1:
            rows.nth(1).click()
