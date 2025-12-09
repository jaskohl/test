"""
Test 21.2.1: Session Survives Page Refresh
Category 21: Session & Concurrency Testing - COMPLETE
Test Count: 3 tests
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 21
"""

import pytest
import time
from playwright.sync_api import Page


def test_21_2_1_session_survives_page_refresh(logged_in_page: Page, base_url: str):
    """Test 21.2.1: Session persists across page refresh"""
    logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")
    # Refresh page
    logged_in_page.reload()
    time.sleep(2)
    # Should still be logged in
    assert "Kronos" in logged_in_page.title()
    assert "authenticate" not in logged_in_page.url.lower()
