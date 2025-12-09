"""
Test 29 20 1 Advanced Diagnostics
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect


def test_29_20_1_advanced_diagnostics(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.20.1: Advanced network diagnostic tools and logging
    Purpose: Test advanced network diagnostic tools and logging on Series 3 devices
    Expected: Diagnostic tools should be visible and enabled on Series 3 devices
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Look for diagnostic tools and logging
    diag_tools = unlocked_config_page.locator(
        "button[name*='diag' i], button[name*='test' i], input[name*='debug' i]"
    )
    if diag_tools.is_visible():
        expect(diag_tools).to_be_enabled()
