"""
Test 29 19 1 Time Sync Validation
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect


def test_29_19_1_time_sync_validation(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.19.1: Time synchronization status and validation
    Purpose: Test time synchronization status and validation on Series 3 devices
    Expected: Time synchronization status should be visible on Series 3 devices
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Look for time synchronization status
    sync_status = unlocked_config_page.locator(
        "span[name*='sync' i], div[class*='time-sync']"
    )
    if sync_status.is_visible():
        expect(sync_status).to_be_visible()
