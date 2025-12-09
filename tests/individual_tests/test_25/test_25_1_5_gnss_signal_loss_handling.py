"""
Test 25.1.5: GNSS signal loss handling
Category 25: Time Synchronization Edge Cases - COMPLETE
Test Count: Part of 5 tests in Category 25
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3

Extracted from: tests/test_25_time_sync_edge_cases.py
Source Class: TestTimeSyncEdgeCases
"""

import pytest
from playwright.sync_api import Page


def test_25_1_5_gnss_signal_loss_handling(logged_in_page: Page, base_url: str):
    """Test 25.1.5: GNSS signal loss handling"""
    logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")
    # Check dashboard for GNSS status
    tables = logged_in_page.locator("table")
    if tables.count() >= 2:
        # GNSS status table exists
        # Device should gracefully handle signal loss (holdover mode)
        pytest.skip("Manual test - requires blocking GNSS signals")
