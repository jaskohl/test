"""
Test 29 1 2 Gateway Validation
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page


def test_29_1_2_gateway_validation(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.1.2: Gateway IP Validation
    Purpose: Verify gateway accepts valid IP addresses
    Expected: Multiple valid IP formats accepted
    Series: Series 3 only
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")
    # Expand gateway panel before field interaction
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
    gateway = unlocked_config_page.locator("input[name='gateway']")
    for ip in ["172.16.0.1", "192.168.1.1", "10.0.0.1"]:
        gateway.fill(ip)
        assert gateway.input_value() == ip
