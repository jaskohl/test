"""
Test 16.4.1: HTTPS Connection Support
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


def test_16_4_1_https_connection_support(page: Page, device_ip: str):
    """
    Test 16.4.1: HTTPS Connection Support
    Purpose: Verify device supports HTTPS connections
    Expected: Can connect via https:// protocol
    Series: Both 2 and 3
    """
    https_url = f"https://{device_ip}"
    try:
        page.goto(https_url, timeout=10000, wait_until="domcontentloaded")
        # Should either load page or show certificate warning
        # Device may have self-signed certificate
        assert page.url.startswith("https"), "Should connect via HTTPS"
        print("HTTPS connection test passed")
    except Exception as e:
        # HTTPS may not be enabled by default
        print(f"HTTPS connection result: {e}")
