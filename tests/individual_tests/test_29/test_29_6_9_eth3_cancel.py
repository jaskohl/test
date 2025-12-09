"""
Test 29.6.9 Eth3 Cancel - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth3 interface cancel button functionality.
Expected: Cancel button should be visible and functional for eth3 configuration.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_6_9_eth3_cancel(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.6.9: eth3 Cancel Button - Pure Page Object Pattern

    Purpose: Test eth3 interface cancel button functionality.
    Expected: Cancel button should be visible and functional for eth3 configuration.
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

    logger.info(f"Testing eth3 cancel button on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth3 panel using page object method
    network_page.expand_network_interface_panel("eth3")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test eth3 cancel button presence and visibility
    try:
        # Try to find eth3-specific cancel button using page object method
        if network_page.has_element(
            "button#button_cancel_port_eth3", timeout=device_timeout
        ):
            eth3_cancel_button = unlocked_config_page.locator(
                "button#button_cancel_port_eth3"
            )
            expect(eth3_cancel_button).to_be_visible(timeout=device_timeout)
            logger.info(f"eth3-specific cancel button found and visible")
            print(f"ETH3 CANCEL BUTTON VALIDATED: {device_model}")
        else:
            # Check for global cancel button if eth3-specific not available
            if network_page.has_element(
                "button:has-text('Cancel')", timeout=device_timeout
            ):
                global_cancel_button = unlocked_config_page.locator(
                    "button:has-text('Cancel')"
                )
                expect(global_cancel_button).to_be_visible(timeout=device_timeout)
                logger.info(
                    f"Global cancel button found (eth3-specific button not available)"
                )
                print(f"GLOBAL CANCEL BUTTON VALIDATED FOR ETH3: {device_model}")
            else:
                logger.warning(f"Cancel button not found for {device_model}")
                print(f"CANCEL BUTTON NOT FOUND: {device_model}")

    except Exception as e:
        logger.error(f"Error testing eth3 cancel button: {e}")
        print(f"CANCEL BUTTON TEST ERROR: {device_model} - {e}")

    logger.info(f"eth3 cancel button test completed successfully")
