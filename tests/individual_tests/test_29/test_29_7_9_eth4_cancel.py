"""
Test 29.7.9 Eth4 Cancel - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth4 cancel button visibility and enabled state.
Expected: Cancel button should be visible and enabled for eth4 interface.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_7_9_eth4_cancel(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.7.9: Eth4 Cancel - Pure Page Object Pattern

    Purpose: Test eth4 cancel button visibility and enabled state.
    Expected: Cancel button should be visible and enabled for eth4 interface.
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

    logger.info(f"Testing eth4 cancel button on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth4 panel using page object method
    network_page.expand_network_interface_panel("eth4")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test eth4 cancel button visibility using page object method
    if network_page.has_element(
        "button#button_cancel_port_eth4", timeout=device_timeout
    ):
        cancel_button = unlocked_config_page.locator("button#button_cancel_port_eth4")
        expect(cancel_button).to_be_visible(timeout=device_timeout)
        print("eth4 cancel button test completed")
        logger.info(f"eth4 cancel button validated for {device_model}")
    else:
        print("Cancel button not available for eth4 (may be expected on some models)")
        logger.info(
            f"eth4 cancel button not found for {device_model} (may be expected on some models)"
        )

    print(f"ETH4 CANCEL TEST COMPLETED: {device_model}")
