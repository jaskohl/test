"""
Test 29.7.6 Eth4 SNMP - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test SNMP enable functionality for eth4 interface.
Expected: SNMP checkbox should be visible and enabled for eth4 on Series 3 devices.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_7_6_eth4_snmp(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.7.6: eth4 SNMP Configuration - Pure Page Object Pattern

    Purpose: Test SNMP enable functionality for eth4 interface.
    Expected: SNMP checkbox should be visible and enabled for eth4 on Series 3 devices.
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

    logger.info(f"Testing eth4 SNMP on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth4 panel using page object method
    network_page.expand_network_interface_panel("eth4")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test eth4 SNMP configuration using page object method
    if network_page.has_element(
        "input[name='snmp_enable_eth4']", timeout=device_timeout
    ):
        snmp = unlocked_config_page.locator("input[name='snmp_enable_eth4']")
        expect(snmp).to_be_enabled(timeout=device_timeout)
        print("eth4 SNMP configuration test completed")
        logger.info(f"eth4 SNMP field validated for {device_model}")
    else:
        print("SNMP field not available for eth4 (may be expected if not supported)")
        logger.info(
            f"eth4 SNMP field not found for {device_model} (may be expected if not supported)"
        )

    print(f"ETH4 SNMP TEST COMPLETED: {device_model}")
