"""
Test 20.1.1: Password not visible in DOM
Category: 20 - Security & Penetration Testing
Test Count: Part of 7 tests in Category 20
Hardware: Device Only
Priority: HIGH
Series: Both Series 2 and 3

Extracted from: tests/test_20_security.py
Source Class: TestAuthenticationSecurity
"""

import pytest
from playwright.sync_api import Page


def test_20_1_1_password_not_visible_in_dom(
    page: Page, base_url: str, device_password: str
):
    """
    Test 20.1.1: Password not stored in DOM
    Purpose: Ensure password is not visible in DOM or page source
    Expected: Password field should have type='password' and password should not appear in page source
    """
    page.goto(base_url, wait_until="domcontentloaded")
    password_field = page.get_by_placeholder("Password")
    password_field.fill(device_password)
    # Check password field type
    field_type = password_field.get_attribute("type")
    assert field_type == "password", "Password field should have type='password'"
    # Check password not in page source
    page_content = page.content()
    assert (
        device_password not in page_content
    ), "Password should not appear in page source"
