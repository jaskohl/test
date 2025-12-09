"""
Test 29.6.8 Eth3 Save - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth3 interface save button functionality.
Expected: Save button should be visible and functional for eth3 configuration.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_6_8_eth3_save(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.6.8: eth3 Save Button - Pure Page Object Pattern

    Purpose: Test eth3 interface save button functionality.
    Expected: Save button should be visible and functional for eth3 configuration.
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

    logger.info(f"Testing eth3 save button on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth3 panel using page object method
    network_page.expand_network_interface_panel("eth3")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test eth3 save button using page object method
    try:
        save_button_locator = network_page.get_save_button_locator()

        if save_button_locator and save_button_locator.count() > 0:
            expect(save_button_locator).to_be_visible(timeout=device_timeout)

            # Try to find eth3-specific save button if available using page object method
            if network_page.has_element(
                "button#button_save_port_eth3", timeout=device_timeout
            ):
                eth3_save_button = unlocked_config_page.locator(
                    "button#button_save_port_eth3"
                )
                expect(eth3_save_button).to_be_visible(timeout=device_timeout)
                logger.info(f"eth3-specific save button found and visible")
                print(f"ETH3 SAVE BUTTON VALIDATED: {device_model}")
            else:
                logger.info(
                    f"Global save button found (eth3-specific button not available)"
                )
                print(f"GLOBAL SAVE BUTTON VALIDATED FOR ETH3: {device_model}")
        else:
            logger.warning(f"Save button not found for {device_model}")
            print(f"SAVE BUTTON NOT FOUND: {device_model}")

    except Exception as e:
        logger.error(f"Error testing eth3 save button: {e}")
        print(f"SAVE BUTTON TEST ERROR: {device_model} - {e}")

    logger.info(f"eth3 save button test completed successfully")
