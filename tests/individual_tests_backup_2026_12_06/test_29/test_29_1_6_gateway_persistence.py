"""
Test 29 1 6 Gateway Persistence
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_29_1_6_gateway_persistence(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29 1 6 Gateway Persistence
    Purpose: Test that gateway configuration persists across page navigation
    Expected: Gateway value should be maintained after page reload/navigation
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    # Navigate to network page
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Expand gateway panel before field interaction
    try:
        gateway_header = unlocked_config_page.locator('a[href="#gateway_collapse"]')
        if gateway_header.count() > 0:
            aria_expanded = gateway_header.get_attribute("aria-expanded")
            if aria_expanded != "true":
                gateway_header.click()
                time.sleep(0.5)
    except Exception:
        pass  # Panel expansion is optional

    # Get current gateway value
    gateway = unlocked_config_page.locator("input[name='gateway']")
    current = gateway.input_value()

    # Navigate away to another page and back
    unlocked_config_page.goto(f"{base_url}/general", wait_until="domcontentloaded")
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Expand gateway panel again after navigation
    try:
        gateway_header = unlocked_config_page.locator('a[href="#gateway_collapse"]')
        if gateway_header.count() > 0:
            aria_expanded = gateway_header.get_attribute("aria-expanded")
            if aria_expanded != "true":
                gateway_header.click()
                time.sleep(0.5)
    except Exception:
        pass  # Panel expansion is optional

    # Verify gateway value persisted
    assert (
        unlocked_config_page.locator("input[name='gateway']").input_value() == current
    ), f"Gateway value should persist after navigation (was {current})"
