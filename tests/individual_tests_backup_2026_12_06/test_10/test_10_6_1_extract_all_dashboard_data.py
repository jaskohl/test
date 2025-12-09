"""
Test 10.6.1: Extract All Dashboard Data
Category: 10 - Dashboard Data Extraction Tests
Test Count: Part of 12 tests in Category 10
Hardware: Device Only
Priority: HIGH - Critical status monitoring
Series: Both Series 2 and 3

Extracted from: tests/test_10_dashboard.py
Source Class: TestDashboardDataCompleteness
"""

import pytest
from playwright.sync_api import Page, expect
from pages.dashboard_page import DashboardPage


def test_10_6_1_extract_all_dashboard_data(logged_in_page):
    """
    Test 10.6.1: Extract Complete Dashboard Data
    Purpose: Verify can extract data from all 4 tables
    Expected: All tables return data dictionaries
    """
    # Initialize page objects
    dashboard_page = DashboardPage(logged_in_page)

    # Extract all data
    status_data = dashboard_page.get_status_data()
    gnss_data = dashboard_page.get_gnss_data()
    time_sync_data = dashboard_page.get_time_sync_data()
    alarms_data = dashboard_page.get_alarms_data()
    # All extractions should return data
    assert status_data or isinstance(
        status_data, dict
    ), "Should extract status table data"
    assert gnss_data or isinstance(gnss_data, dict), "Should extract GNSS table data"
    assert time_sync_data or isinstance(
        time_sync_data, dict
    ), "Should extract time sync table data"
    assert alarms_data is not None, "Should extract alarms table data"
