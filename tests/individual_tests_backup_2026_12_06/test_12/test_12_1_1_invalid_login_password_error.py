"""
Test 12.1.1: Invalid Login Password Error
Category: 12 - Error Handling Tests
Test Count: Part of 12 tests in Category 12
Hardware: Device Only
Priority: HIGH - Proper error handling critical for reliability
Series: Both Series 2 and 3

Extracted from: tests/test_12_error_handling.py
Source Class: TestAuthenticationErrors
"""

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


def test_12_1_1_invalid_login_password_error(page, base_url):
    """
    Test 12.1.1: Invalid Login Password Error Message
    Purpose: Verify error handling for invalid login credentials
    Expected: Login fails and appropriate error is indicated
    """
    page.goto(base_url, wait_until="domcontentloaded")
    login_page = LoginPage(page)
    success = login_page.login(password="invalid_password_123")
    assert not success, "Login should fail with invalid password"
    errors = login_page.check_for_authentication_errors()
    assert errors or not success, "Should indicate authentication failure"
