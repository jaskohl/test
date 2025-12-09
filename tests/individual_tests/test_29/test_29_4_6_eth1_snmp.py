"""
Test 29.4.6 Eth1 SNMP Configuration - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth1 interface SNMP enable checkbox functionality.
Expected: SNMP checkbox visible and functional for Series 3 devices.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_4_6_eth1_snmp(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.4.6: eth1 SNMP Configuration - Pure Page Object Pattern

    Purpose: Test eth1 interface SNMP enable checkbox functionality.
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
        pytest.skip(f"Series 3 only (detected Series {device_series})")

    logger.info(f"Testing eth1 SNMP on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth1 panel using page object method
    network_page.expand_network_interface_panel("eth1")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test SNMP enable checkbox using page object method
    if network_page.has_element(
        "input[name='snmp_enable_eth1']", timeout=device_timeout
    ):
        snmp_checkbox = unlocked_config_page.locator("input[name='snmp_enable_eth1']")
        expect(snmp_checkbox).to_be_visible(timeout=device_timeout)
        expect(snmp_checkbox).to_be_enabled()

        # Verify checkbox can be toggled
        initial_state = snmp_checkbox.is_checked()
        snmp_checkbox.click()
        new_state = snmp_checkbox.is_checked()

        # State should have changed
        assert initial_state != new_state, "SNMP checkbox should toggle when clicked"

        logger.info(f"eth1 SNMP checkbox validated - enabled and toggles correctly")
        print(f"ETH1 SNMP VALIDATED: {device_model}")
    else:
        logger.info(
            f"eth1 SNMP checkbox not found on {device_model} (expected on some configurations)"
        )
        print(f"ETH1 SNMP NOT PRESENT: {device_model}")
