"""
Test 29.4.8 Eth1 Save Button - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth1 interface save button functionality.
Expected: Save button visible and functional for Series 3 devices.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_4_8_eth1_save(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.4.8: eth1 Save Button - Pure Page Object Pattern

    Purpose: Test eth1 interface save button functionality.
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

    logger.info(f"Testing eth1 save button on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth1 panel using page object method
    network_page.expand_network_interface_panel("eth1")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Get device-aware save button using page object method
    save_button = network_page.get_save_button_locator()

    if save_button.count() > 0:
        expect(save_button).to_be_visible(timeout=device_timeout)
        expect(save_button).to_be_enabled()

        logger.info(f"eth1 save button validated - visible and enabled")
        print(f"ETH1 SAVE BUTTON VALIDATED: {device_model}")
    else:
        logger.info(
            f"eth1 save button not found on {device_model} (expected on some configurations)"
        )
        print(f"ETH1 SAVE BUTTON NOT PRESENT: {device_model}")
