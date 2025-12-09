"""
Category 10: Dashboard Data Extraction Tests - Test 10.1.1
All 4 Dashboard Tables Present
Test Count: 1 of 12 in Category 10
Hardware: Device Only
Priority: HIGH - Critical status monitoring
Series: Both Series 2 and 3
Based on test_10_dashboard.py::TestDashboardTables::test_10_1_1_all_tables_present
FIXED: Added retry logic for table loading on Series 3 devices
"""

import pytest
from playwright.sync_api import Page, expect
from pages.dashboard_page import DashboardPage


def test_10_1_1_all_tables_present(logged_in_page):
    """
    Test 10.1.1: All 4 Dashboard Tables Present
    Purpose: Verify dashboard contains all 4 status tables
    Expected: Tables for Status, GNSS, Time Sync, and Alarms visible
    Series: Both 2 and 3
    FIXED: Added retry logic for table loading on Series 3 devices
    """
    # Note: Device has no semantic table attributes, using CSS selector
    tables = logged_in_page.locator("table")
    # Retry logic for table loading (Series 3 devices may load tables asynchronously)
    max_retries = 3
    table_count = 0
    for attempt in range(max_retries):
        table_count = tables.count()
        if table_count == 4:
            break
        # Wait and retry
        logged_in_page.wait_for_timeout(10000)
    assert (
        table_count == 4
    ), f"Dashboard should have 4 tables, found {table_count} after {max_retries} attempts"
    # Verify each table is visible
    for i in range(4):
        expect(tables.nth(i)).to_be_visible()
