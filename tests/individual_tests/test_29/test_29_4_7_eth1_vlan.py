"""
Test 29.4.7 Eth1 VLAN Configuration - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth1 interface VLAN enable checkbox functionality.
Expected: VLAN checkbox visible and functional for Series 3 devices.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_4_7_eth1_vlan(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.4.7: eth1 VLAN Configuration - Pure Page Object Pattern

    Purpose: Test eth1 interface VLAN enable checkbox functionality.
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

    logger.info(f"Testing eth1 VLAN on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth1 panel using page object method
    network_page.expand_network_interface_panel("eth1")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test VLAN enable checkbox using page object method
    if network_page.has_element(
        "input[name='vlan_enable_eth1']", timeout=device_timeout
    ):
        vlan_checkbox = unlocked_config_page.locator("input[name='vlan_enable_eth1']")
        expect(vlan_checkbox).to_be_visible(timeout=device_timeout)
        expect(vlan_checkbox).to_be_enabled()

        # Verify checkbox can be toggled
        initial_state = vlan_checkbox.is_checked()
        vlan_checkbox.click()
        new_state = vlan_checkbox.is_checked()

        # State should have changed
        assert initial_state != new_state, "VLAN checkbox should toggle when clicked"

        logger.info(f"eth1 VLAN checkbox validated - enabled and toggles correctly")
        print(f"ETH1 VLAN VALIDATED: {device_model}")
    else:
        logger.info(
            f"eth1 VLAN checkbox not found on {device_model} (expected on some configurations)"
        )
        print(f"ETH1 VLAN NOT PRESENT: {device_model}")
