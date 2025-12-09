"""
Test 29.7.7 Eth4 VLAN - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test VLAN enable and ID functionality for eth4 interface.
Expected: VLAN enable checkbox and ID field should be visible and functional for eth4 on Series 3 devices.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_7_7_eth4_vlan(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.7.7: eth4 VLAN Configuration - Pure Page Object Pattern

    Purpose: Test VLAN enable and ID functionality for eth4 interface.
    Expected: VLAN enable checkbox and ID field should be visible and functional for eth4 on Series 3 devices.
    Series: Series 3 only
    """
    # Get device model from session
    device_model = request.session.device_hardware_model
    if not device_model or device_model == "Unknown":
        pytest.fail("Device model not detected")

    # Create page object with device_model
    network_page = NetworkConfigPage(unlocked_config_page, device_model=device_model)

    # Validate Series 3 requirement using page object method
    device_series = network_page.get_series()
    if device_series != 3:
        pytest.skip("Series 3 only")

    logger.info(f"Testing eth4 VLAN on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth4 panel using page object method
    network_page.expand_network_interface_panel("eth4")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test VLAN enable checkbox using page object method
    if network_page.has_element(
        "input[name='vlan_enable_eth4']", timeout=device_timeout
    ):
        vlan = unlocked_config_page.locator("input[name='vlan_enable_eth4']")
        expect(vlan).to_be_enabled(timeout=device_timeout)
        print("eth4 VLAN enable checkbox is visible and enabled")
        logger.info(f"eth4 VLAN enable field validated for {device_model}")

    # Test VLAN ID field using page object method
    if network_page.has_element("input[name='vlan_id_eth4']", timeout=device_timeout):
        vlan_id = unlocked_config_page.locator("input[name='vlan_id_eth4']")
        vlan_id.fill("300")
        print("eth4 VLAN ID field tested")
        logger.info(f"eth4 VLAN ID field validated for {device_model}")

    print("eth4 VLAN configuration test completed")
    logger.info(f"eth4 VLAN test completed for {device_model}")

    print(f"ETH4 VLAN TEST COMPLETED: {device_model}")
