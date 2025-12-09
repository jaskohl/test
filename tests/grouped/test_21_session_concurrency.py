"""
Category 21: Session & Concurrency Testing - COMPLETE
Test Count: 3 tests
Hardware: Device Only ()
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 21
"""

import pytest
import time
from playwright.sync_api import Page


class TestConcurrentSessions:
    """Test 21.1: Concurrent Session Management"""

    def test_21_1_1_multiple_sessions_allowed(
        self, browser, base_url: str, device_password: str
    ):
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

    def test_21_1_2_concurrent_config_changes(
        self, browser, base_url: str, device_password: str
    ):
        """Test 21.1.2: Concurrent configuration changes handling"""
        # Create two contexts
        context1 = browser.new_context()
        context2 = browser.new_context()
        page1 = context1.new_page()
        page2 = context2.new_page()
        # Both login and unlock config
        for page in [page1, page2]:
            page.goto(base_url, wait_until="domcontentloaded")
            time.sleep(1)
            password_field = page.get_by_placeholder("Password")
            password_field.fill(device_password)
            page.locator("button[type='submit']").click()
            time.sleep(12)
            # Unlock config
            page.goto(f"{base_url}/", wait_until="domcontentloaded")
            configure_btn = page.locator("a[title*='locked']").filter(
                has_text="Configure"
            )
            if configure_btn.is_visible():
                configure_btn.click()
                time.sleep(1)
                cfg_password = page.locator("input[name='cfg_password']")
                if cfg_password.is_visible():
                    cfg_password.fill(device_password)
                    page.locator("button[type='submit']").click()
                    time.sleep(12)
        # Both navigate to same config page
        page1.goto(f"{base_url}/display", wait_until="domcontentloaded")
        page2.goto(f"{base_url}/display", wait_until="domcontentloaded")
        time.sleep(1)
        # Make changes in both (last write wins)
        mode1 = page1.locator("select[name='mode']")
        mode2 = page2.locator("select[name='mode']")
        if mode1.is_visible() and mode2.is_visible():
            mode1.select_option(index=1)
            mode2.select_option(index=2)
        context1.close()
        context2.close()


class TestSessionPersistence:
    """Test 21.2: Session Persistence"""

    def test_21_2_1_session_survives_page_refresh(
        self, logged_in_page: Page, base_url: str
    ):
        """Test 21.2.1: Session persists across page refresh"""
        logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")
        # Refresh page
        logged_in_page.reload()
        time.sleep(2)
        # Should still be logged in
        assert "Kronos" in logged_in_page.title()
        assert "authenticate" not in logged_in_page.url.lower()
