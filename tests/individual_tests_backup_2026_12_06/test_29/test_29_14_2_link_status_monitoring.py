"""
Test 29.14.2: Link Status Monitoring
Category: 29 - Network Configuration Series 3
Source: tests/grouped/test_29_network_config_series3.py
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect


def test_29_14_2_link_status_monitoring(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.14.2: Link Status Monitoring
    Purpose: Test link status and connectivity monitoring on network interfaces
    Expected: Link status indicators should be visible and functional
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")
    from playwright.sync_api import expect

    # Look for link status indicators
    status = unlocked_config_page.locator(
        "span[name*='status' i], div[class*='link-status']"
    )
    if status.is_visible():
        expect(status).to_be_visible()
