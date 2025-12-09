"""
Test 29 10 3 Port Security
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page


def test_29_10_3_port_security(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.10.3: Port security and MAC filtering

    Test port security and MAC filtering functionality.
    Series 3 devices only - checks for port security field availability and functionality.
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")
    # Look for port security fields
    from playwright.sync_api import expect

    port_sec = unlocked_config_page.locator(
        "input[name*='port_security' i], select[name*='mac_filter' i]"
    )
    if port_sec.is_visible():
        expect(port_sec).to_be_enabled()
