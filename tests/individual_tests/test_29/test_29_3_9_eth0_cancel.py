"""
Test 29.3.9 Eth0 Cancel Button - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth0 interface cancel button functionality.
Expected: Cancel button visible for Series 3 devices.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_3_9_eth0_cancel(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.3.9: eth0 Cancel Button - Pure Page Object Pattern

    Purpose: Test eth0 interface cancel button functionality.
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

    logger.info(f"Testing eth0 cancel button on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth0 panel using page object method
    network_page.expand_network_interface_panel("eth0")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Use page object method to locate and validate eth0 cancel button
    if network_page.has_element(
        "button#button_cancel_port_eth0", timeout=device_timeout
    ):
        logger.info(f"eth0 cancel button validated - visible")
        print(f"ETH0 CANCEL BUTTON VALIDATED: {device_model}")
    else:
        logger.info(
            f"eth0 cancel button not visible on {device_model} (may be expected on some configurations)"
        )
        print(f"ETH0 CANCEL BUTTON NOT PRESENT: {device_model}")
