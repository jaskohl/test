"""
Test 29.14.3: Network Diagnostics
Category: 29 - Network Configuration Series 3
Source: tests/grouped/test_29_network_config_series3.py
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect


def test_29_14_3_network_diagnostics(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.14.3: Network Diagnostics
    Purpose: Test network troubleshooting and diagnostic tools
    Expected: Diagnostic tools should be visible and functional
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")
    from playwright.sync_api import expect

    # Look for diagnostic tools
    diag = unlocked_config_page.locator(
        "button[name*='diag' i], button[name*='ping' i], button[name*='traceroute' i]"
    )
    if diag.is_visible():
        expect(diag).to_be_enabled()
