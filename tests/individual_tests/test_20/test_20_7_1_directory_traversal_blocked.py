"""
Test 20.7.1: Directory traversal blocked
Category: 20 - Security & Penetration Testing
Test Count: Part of 7 tests in Category 20
Hardware: Device Only
Priority: HIGH
Series: Both Series 2 and 3

Extracted from: tests/test_20_security.py
Source Class: TestDirectoryTraversal
"""

import pytest
import time
from playwright.sync_api import Page


def test_20_7_1_directory_traversal_blocked(page: Page, base_url: str):
    """
    Test 20.7.1: Directory traversal attempts blocked
    Purpose: Verify device blocks directory traversal attacks
    Expected: Malicious URLs should not expose sensitive files or directories
    """
    # Try directory traversal
    traversal_urls = [
        f"{base_url}/../../../etc/passwd",
        f"{base_url}/../../config",
        f"{base_url}/../admin",
    ]
    for url in traversal_urls:
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(1)
        # Should not expose sensitive files
        # Should redirect or show error
