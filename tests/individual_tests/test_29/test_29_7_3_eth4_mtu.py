"""
Test 29.7.3 Eth4 MTU - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Verify eth4 MTU configuration with default value.
Expected: Test should verify eth4 MTU field with default value of 1500.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_7_3_eth4_mtu(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.7.3: Eth4 MTU - Pure Page Object Pattern

    Purpose: Verify eth4 MTU configuration with default value.
    Expected: Test should verify eth4 MTU field with default value of 1500.
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

    logger.info(f"Testing eth4 MTU on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth4 panel using page object method
    network_page.expand_network_interface_panel("eth4")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test eth4 MTU field using page object method
    if network_page.has_element("input[name='mtu_eth4']", timeout=device_timeout):
        mtu = unlocked_config_page.locator("input[name='mtu_eth4']")
        expect(mtu).to_be_visible(timeout=device_timeout)

        # Verify default MTU value is 1500
        assert (
            mtu.input_value() == "1500"
        ), f"Expected default MTU 1500, got {mtu.input_value()}"
        print("eth4 MTU field verified - default value 1500")
        logger.info(f"eth4 MTU field validated for {device_model} - default value 1500")
    else:
        print(
            "eth4 MTU field not visible - may not be available on this device variant"
        )
        logger.info(
            f"eth4 MTU field not found for {device_model} (may not be available on this device variant)"
        )

    print(f"ETH4 MTU TEST COMPLETED: {device_model}")
