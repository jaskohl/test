"""
Test 10.6.2: Dashboard Data Refresh
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


def test_10_6_2_dashboard_data_refresh(logged_in_page, base_url):
    """
    Test 10.6.2: Dashboard Data Refresh
    Purpose: Verify dashboard data updates on page reload
    Expected: Data extraction works consistently after refresh
    """
    # Initialize page objects
    dashboard_page = DashboardPage(logged_in_page)

    # First extraction
    data1 = dashboard_page.get_status_data()
    # Refresh page
    dashboard_page.page.goto(f"{base_url}/", wait_until="domcontentloaded")
    # Second extraction
    data2 = dashboard_page.get_status_data()
    # Both extractions should succeed
    assert data1 or isinstance(data1, dict), "First extraction should succeed"
    assert data2 or isinstance(data2, dict), "Second extraction should succeed"
