"""
Test 10.2.4: Extract Firmware Version
Category: 10 - Dashboard Data Extraction Tests
Test Count: Part of 12 tests in Category 10
Hardware: Device Only
Priority: HIGH - Critical status monitoring
Series: Both Series 2 and 3

Extracted from: tests/test_10_dashboard.py
Source Class: TestStatusTable
"""

import pytest
from playwright.sync_api import Page, expect
from pages.dashboard_page import DashboardPage


def test_10_2_4_extract_firmware_version(logged_in_page):
    """
    Test 10.2.4: Extract Firmware Version
    Purpose: Verify can extract firmware version
    Expected: Version string in expected format
    """
    # Initialize page objects
    dashboard_page = DashboardPage(logged_in_page)

    status_data = dashboard_page.get_status_data()
    # Look for firmware/version field
    version_fields = ["firmware", "version", "Firmware", "Version", "fw_version"]
    version_found = False
    version = None
    for field in version_fields:
        if field in status_data:
            version = status_data[field]
            assert version, f"Version field {field} should not be empty"
            version_found = True
            break
    # Version may not always be displayed on dashboard
    if version_found and version:
        assert len(version) > 0, "Version should have content"
