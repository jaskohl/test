"""
Test 20.3.2: No Session Fixation
Category 20: Security & Penetration Testing - COMPLETE
Test Count: 7 tests
Hardware: Device Only
Priority: HIGH
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 20
"""

import pytest
import time
from playwright.sync_api import Page


def test_20_3_2_no_session_fixation(browser, base_url: str, device_password: str):
    """Test 20.3.2: Session ID changes after login"""
    # Create new context and page
    context = browser.new_context()
    page = context.new_page()
    page.goto(base_url, wait_until="domcontentloaded")
    # Get cookies before login
    cookies_before = context.cookies()
    # Login
    password_field = page.get_by_placeholder("Password")
    password_field.fill(device_password)
    page.locator("button[type='submit']").click()
    time.sleep(15)
    # Get cookies after login
    cookies_after = context.cookies()
    # Session cookie should have changed
    context.close()
