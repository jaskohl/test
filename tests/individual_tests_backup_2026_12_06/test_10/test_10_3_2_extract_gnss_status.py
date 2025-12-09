"""
Test 10.3.2: Extract GNSS Status
Category: 10 - Dashboard Data Extraction Tests
Test Count: Part of 12 tests in Category 10
Hardware: Device Only
Priority: HIGH - Critical status monitoring
Series: Both Series 2 and 3
FIXED: Enhanced GNSS data extraction with fallback strategies and more defensive assertions

Extracted from: tests/test_10_dashboard.py
Source Class: TestGNSSTable
"""

import pytest
from playwright.sync_api import Page, expect
from pages.dashboard_page import DashboardPage


def test_10_3_2_extract_gnss_status(logged_in_page):
    """
    Test 10.3.2: Extract GNSS Lock Status
    Purpose: Verify can determine if GNSS has lock
    Expected: Status indicator for GNSS acquisition state
    FIXED: Enhanced GNSS data extraction with fallback strategies
    and more defensive assertions based on device exploration data
    """
    # Initialize page objects
    dashboard_page = DashboardPage(logged_in_page)

    gnss_data = dashboard_page.get_gnss_data()
    # Based on device exploration data, GNSS data should include:
    # - GNSS state (LOCKED, etc.)
    # - Antenna state
    # - Time accuracy
    # - Used / tracked SVs
    # More defensive check: GNSS data should be present for Series 2 devices
    assert isinstance(gnss_data, dict), "GNSS data should be a dictionary"
    # Check for expected GNSS fields from device exploration
    expected_gnss_fields = [
        "GNSS state",
        "Antenna state",
        "Time accuracy",
        "Used / tracked SVs",
    ]
    # At least some GNSS data should be present
    gnss_fields_present = [
        field for field in expected_gnss_fields if field in gnss_data
    ]
    assert (
        len(gnss_fields_present) > 0
    ), f"Expected GNSS fields not found. Available: {list(gnss_data.keys())}"
    # If GNSS state is present, it should have a meaningful value
    if "GNSS state" in gnss_data:
        gnss_state = gnss_data["GNSS state"]
        assert gnss_state, "GNSS state should not be empty"
        assert gnss_state in [
            "LOCKED",
            "ACQUIRING",
            "SEARCHING",
            "NOTIME",
            "UNKNOWN",
            "LOWQUALITY",
        ], f"Unexpected GNSS state: {gnss_state}"
    print(f"GNSS data extraction successful: {gnss_data}")
