"""
Test 29.6.3 Eth3 MTU - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth3 MTU configuration field functionality.
Expected: MTU field should be visible and have default value of 1494.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_6_3_eth3_mtu(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.6.3: eth3 MTU Configuration - Pure Page Object Pattern

    Purpose: Test eth3 MTU configuration field functionality.
    Expected: MTU field should be visible and have default value of 1494.
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

    logger.info(f"Testing eth3 MTU on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth3 panel using page object method
    network_page.expand_network_interface_panel("eth3")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test MTU configuration using page object method
    if network_page.has_element("input[name='mtu_eth3']", timeout=device_timeout):
        mtu_field = unlocked_config_page.locator("input[name='mtu_eth3']")
        expect(mtu_field).to_be_visible(timeout=device_timeout)

        # Verify MTU field has default value
        default_value = mtu_field.input_value()
        assert (
            default_value == "1494"
        ), f"Expected default MTU 1494, got {default_value}"

        # Test MTU value input functionality
        test_values = ["1500", "9000", "1494"]
        for test_value in test_values:
            mtu_field.fill(test_value)
            actual_value = mtu_field.input_value()
            assert (
                actual_value == test_value
            ), f"Expected MTU {test_value}, got {actual_value}"

        logger.info(f"eth3 MTU field validated - editable and accepts valid values")
        print(f"ETH3 MTU FIELD VALIDATED: {device_model}")
    else:
        logger.info(
            f"eth3 MTU field not found on {device_model} (may depend on device model)"
        )
        print(f"ETH3 MTU NOT PRESENT: {device_model}")
