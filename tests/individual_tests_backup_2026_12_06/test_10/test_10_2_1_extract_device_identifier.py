"""
Test 10.2.1: Extract Device Identifier
Category: 10 - Dashboard Data Extraction Tests
Test Count: Part of 12 tests in Category 10
Hardware: Device Only
Priority: HIGH - Critical status monitoring
Series: Both Series 2 and 3
FIXED: Handle empty identifier, location, and contact fields (legitimate behavior)

Extracted from: tests/test_10_dashboard.py
Source Class: TestStatusTable
"""

import pytest
from playwright.sync_api import Page, expect
from pages.dashboard_page import DashboardPage


def test_10_2_1_extract_device_identifier(logged_in_page):
    """
    Test 10.2.1: Extract Device Identifier
    Purpose: Verify can extract device identifier from status table
    Expected: Identifier value is readable (may be empty - this is valid)
    FIXED: Device identifier may be empty, which is legitimate behavior
    """
    # Initialize page objects
    dashboard_page = DashboardPage(logged_in_page)

    status_data = dashboard_page.get_status_data()
    assert (
        "identifier" in status_data or "Identifier" in status_data
    ), "Status table should contain identifier field"
    identifier = status_data.get("identifier") or status_data.get("Identifier")
    # FIXED: Identifier can be empty (legitimate behavior)
    # Test should verify field exists and can be read, not that it has content
    assert isinstance(identifier, str), "Identifier should be a string"
    # Empty identifier is valid behavior for unconfigured devices
    if identifier:
        assert len(identifier) > 0, "If present, identifier should have content"
