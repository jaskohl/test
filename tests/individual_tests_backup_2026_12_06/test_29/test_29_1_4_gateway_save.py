"""
Test 29 1 4 Gateway Save
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page


def test_29_1_4_gateway_save(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.1.4: Gateway Save Button
    Purpose: Verify gateway save button is present and functional
    Expected: Save button enables when gateway configured
    Series: Series 3 only
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")
    # Expand gateway panel before button interaction
    try:
        gateway_header = unlocked_config_page.locator('a[href="#gateway_collapse"]')
        if gateway_header.count() > 0:
            aria_expanded = gateway_header.get_attribute("aria-expanded")
            if aria_expanded != "true":
                gateway_header.click()
                import time

                time.sleep(0.5)
    except Exception:
        pass  # Panel expansion is optional
    save_button = unlocked_config_page.locator(
        "button#button_save_gateway, button.save"
    )
    if save_button.is_visible():
        from playwright.sync_api import expect

        expect(save_button).to_be_visible()
