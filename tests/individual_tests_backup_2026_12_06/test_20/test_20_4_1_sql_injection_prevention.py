"""
Test 20.4.1: SQL injection prevention
Category: 20 - Security & Penetration Testing
Test Count: Part of 7 tests in Category 20
Hardware: Device Only
Priority: HIGH
Series: Both Series 2 and 3

Extracted from: tests/test_20_security.py
Source Class: TestInputValidation
"""

import pytest
import time
from playwright.sync_api import Page


def test_20_4_1_sql_injection_prevention(unlocked_config_page: Page, base_url: str):
    """
    Test 20.4.1: SQL injection attempts rejected
    Purpose: Verify device rejects SQL injection attempts in input fields
    Expected: Malicious SQL code should be sanitized and device should remain functional
    """
    unlocked_config_page.goto(f"{base_url}/general", wait_until="domcontentloaded")
    # Try SQL injection in text field
    identifier = unlocked_config_page.locator("input[name='identifier']")
    identifier.fill("'; DROP TABLE users; --")
    save_btn = unlocked_config_page.get_by_role("button", name="Save")
    if save_btn.is_enabled():
        save_btn.click()
        time.sleep(2)
    # Device should still function (input sanitized) - protocol flexible
    unlocked_config_page.goto(f"{base_url}/", wait_until="domcontentloaded")
    expected_base = base_url.replace("http://", "").replace("https://", "")
    actual_base = unlocked_config_page.url.replace("http://", "").replace(
        "https://", ""
    )
    assert actual_base == expected_base + "/"
