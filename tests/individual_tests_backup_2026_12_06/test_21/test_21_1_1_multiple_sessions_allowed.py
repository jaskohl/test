"""
Test 21.1.1: Multiple Sessions Allowed
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


def test_21_1_1_multiple_sessions_allowed(browser, base_url: str, device_password: str):
    """Test 21.1.1: Multiple browser sessions can access device"""
    # Create two contexts (simulating two users)
    context1 = browser.new_context()
    context2 = browser.new_context()
    page1 = context1.new_page()
    page2 = context2.new_page()
    # Login with both
    for page in [page1, page2]:
        page.goto(base_url, wait_until="domcontentloaded")
        time.sleep(1)
        password_field = page.get_by_placeholder("Password")
        password_field.fill(device_password)
        page.locator("button[type='submit']").click()
        time.sleep(12)
    # Both should be logged in
    assert "Kronos" in page1.title()
    assert "Kronos" in page2.title()
    context1.close()
    context2.close()
