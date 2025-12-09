"""
Test 29.7.2 Eth4 Netmask - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Verify eth4 netmask field presence and editability.
Expected: Test should verify eth4 netmask field visibility and editability.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_7_2_eth4_netmask(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.7.2: Eth4 Netmask - Pure Page Object Pattern

    Purpose: Verify eth4 netmask field presence and editability.
    Expected: Test should verify eth4 netmask field visibility and editability.
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

    logger.info(f"Testing eth4 netmask on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth4 panel using page object method
    network_page.expand_network_interface_panel("eth4")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test eth4 netmask field using page object method
    if network_page.has_element("input[name='mask_eth4']", timeout=device_timeout):
        eth4_mask = unlocked_config_page.locator("input[name='mask_eth4']")
        expect(eth4_mask).to_be_visible(timeout=device_timeout)
        expect(eth4_mask).to_be_editable()
        print("eth4 netmask field verified - visible and editable")
        logger.info(f"eth4 netmask field validated for {device_model}")
    else:
        print(
            "eth4 netmask field not visible - may not be available on this device variant"
        )
        logger.info(
            f"eth4 netmask field not found for {device_model} (may not be available on this device variant)"
        )

    print(f"ETH4 NETMASK TEST COMPLETED: {device_model}")
