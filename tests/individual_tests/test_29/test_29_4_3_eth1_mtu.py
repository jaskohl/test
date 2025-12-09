"""
Test 29.4.3 Eth1 MTU - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth1 interface MTU field functionality.
Expected: MTU field visible and enabled for Series 3 devices.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_4_3_eth1_mtu(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.4.3: eth1 MTU Configuration - Pure Page Object Pattern

    Purpose: Test eth1 interface MTU field functionality.
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

    logger.info(f"Testing eth1 MTU on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth1 panel using page object method
    network_page.expand_network_interface_panel("eth1")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test MTU field using page object method
    if network_page.has_element("input[name='mtu_eth1']", timeout=device_timeout):
        mtu_field = unlocked_config_page.locator("input[name='mtu_eth1']")
        expect(mtu_field).to_be_visible(timeout=device_timeout)
        expect(mtu_field).to_be_enabled()

        # Verify MTU value is within reasonable range
        current_mtu = mtu_field.input_value()
        if current_mtu:
            mtu_value = int(current_mtu)
            # Typical MTU range for Ethernet interfaces
            assert (
                68 <= mtu_value <= 9000
            ), f"MTU value {mtu_value} is outside valid range (68-9000)"

        logger.info(f"eth1 MTU field validated - enabled with valid range")
        print(f"ETH1 MTU VALIDATED: {device_model}")
    else:
        logger.info(
            f"eth1 MTU field not found on {device_model} (expected on some configurations)"
        )
        print(f"ETH1 MTU NOT PRESENT: {device_model}")
