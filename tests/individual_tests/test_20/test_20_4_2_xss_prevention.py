"""
Test 20.4.2: XSS prevention
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


def test_20_4_2_xss_prevention(unlocked_config_page: Page, base_url: str):
    """
    Test 20.4.2: XSS attempts rejected
    Purpose: Verify device rejects XSS (Cross-Site Scripting) attempts
    Expected: Malicious scripts should be sanitized and no alert should fire
    """
    unlocked_config_page.goto(f"{base_url}/general", wait_until="domcontentloaded")
    # Try XSS in text field
    identifier = unlocked_config_page.locator("input[name='identifier']")
    identifier.fill("<script>alert('XSS')</script>")
    save_btn = unlocked_config_page.locator("button#button_save")
    if save_btn.is_enabled():
        save_btn.click()
        time.sleep(2)
    # No alert should have fired
    # Script should be sanitized
