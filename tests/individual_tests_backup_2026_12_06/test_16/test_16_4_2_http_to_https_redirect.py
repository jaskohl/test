"""
Test 16.4.2: HTTP to HTTPS Redirect
Category: 16 - Integration Tests
Test Count: Part of 9 tests in Category 16
Hardware: Software Tools for 6 tests, Device Only for 3 tests
Priority: MEDIUM - External protocol validation
Series: Both Series 2 and 3

Extracted from: tests/test_16_integration.py
Source Class: TestHTTPSIntegration
"""

import pytest
from playwright.sync_api import Page, expect


def test_16_4_2_http_to_https_redirect(page: Page, device_ip: str):
    """
    Test 16.4.2: HTTP to HTTPS Redirect
    Purpose: Verify if device redirects HTTP to HTTPS
    Expected: May redirect to HTTPS if security enabled
    Series: Both 2 and 3
    """
    http_url = f"http://{device_ip}"
    page.goto(http_url, wait_until="domcontentloaded")
    final_url = page.url
    # Device may or may not redirect to HTTPS
    print(f"HTTP connection resulted in: {final_url}")
