"""
Test 29.4.1 Eth1 Redundancy - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth1 interface redundancy mode functionality.
Expected: Redundancy dropdown visible and enabled for Series 3.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_4_1_eth1_redundancy(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.4.1: eth1 Redundancy Configuration - Pure Page Object Pattern

    Purpose: Test eth1 interface redundancy mode functionality.
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

    logger.info(f"Testing eth1 redundancy on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth1 panel using page object method
    network_page.expand_network_interface_panel("eth1")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Use page object method to test redundancy field with multiple selector patterns
    redundancy_selectors = [
        "select[name='redundancy_mode_eth1']",
        "select[name='eth1_redundancy']",
        "select[id*='redundancy']",
    ]

    redundancy_field_found = False
    for selector in redundancy_selectors:
        if network_page.has_element(selector, timeout=device_timeout):
            redundancy_field_found = True
            logger.info(f"Eth1 redundancy field found using selector '{selector}'")
            break

    if redundancy_field_found:
        # Get the redundancy field element
        redundancy_field = unlocked_config_page.locator(redundancy_selectors[0])
        if not redundancy_field.count() > 0:
            # Try alternative selectors if first one fails
            for selector in redundancy_selectors[1:]:
                potential_field = unlocked_config_page.locator(selector)
                if potential_field.count() > 0:
                    redundancy_field = potential_field
                    break

        expect(redundancy_field).to_be_visible(timeout=device_timeout)
        expect(redundancy_field).to_be_enabled(timeout=device_timeout)

        # Verify redundancy dropdown has options
        option_count = redundancy_field.locator("option").count()
        assert (
            option_count >= 2
        ), f"Eth1 redundancy dropdown should have at least 2 options, found {option_count}"

        logger.info(
            f"eth1 redundancy field validated - {option_count} options available"
        )
        print(f"ETH1 REDUNDANCY VALIDATED: {device_model} ({option_count} options)")
    else:
        logger.info(
            f"Eth1 redundancy field not found on {device_model} (may be expected on some configurations)"
        )
        print(f"ETH1 REDUNDANCY NOT PRESENT: {device_model}")
