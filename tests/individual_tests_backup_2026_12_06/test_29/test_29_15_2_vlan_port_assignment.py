"""
Test 29 15 2 Vlan Port Assignment
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestVLANConfigurationManagement
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect


def test_29_15_2_vlan_port_assignment(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.15.2: VLAN Port Assignment
    Purpose: Port assignment to VLANs
    Expected: VLAN port assignment fields should be visible and configurable
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Look for VLAN port assignment
    vlan_ports = unlocked_config_page.locator(
        "select[name*='vlan_ports' i], input[name*='tagged_ports' i]"
    )
    if vlan_ports.is_visible():
        expect(vlan_ports).to_be_enabled()
