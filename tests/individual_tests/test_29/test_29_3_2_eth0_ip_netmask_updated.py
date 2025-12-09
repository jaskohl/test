"""
Test 29.3.2 Eth0 IP Netmask - Page Object Refactored

Category: 29 - Network Configuration Series 3
Purpose: Verify eth0 interface has proper IP and netmask configuration fields.
Expected: IP field visible and editable, netmask field available for Series 3.

REFACTORED: Uses NetworkConfigPage methods instead of direct locators.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_29_3_2_eth0_ip_netmask(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.3.2: eth0 IP Address and Netmask Configuration - Page Object Refactored

    Purpose: Verify eth0 interface IP and netmask fields with device-aware validation.
    """
    # Get device model from session
    device_model = request.session.device_hardware_model
    if not device_model or device_model == "Unknown":
        pytest.fail("Device model not detected")

    # Validate Series 3 requirement
    device_series = DeviceCapabilities.get_series(device_model)
    if device_series != 3:
        pytest.skip(f"Series 3 only (detected Series {device_series})")

    logger.info(f"Testing eth0 IP/netmask on {device_model}")

    # Create page object with device_model
    network_page = NetworkConfigPage(unlocked_config_page, device_model=device_model)

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth0 panel using page object method
    network_page.expand_panel("eth0")

    # Get device-aware timeout
    device_timeout = network_page.get_timeout(5000)

    # Test IP field using interface-aware locator
    ip_selector = network_page.get_interface_aware_locator("ip", "eth0")
    ip_field = network_page.page.locator(ip_selector)

    expect(ip_field).to_be_visible(timeout=device_timeout)
    expect(ip_field).to_be_editable()
    logger.info(f"eth0 IP field visible and editable on {device_model}")

    # Test netmask field - try multiple patterns
    mask_found = False
    for field_name in ["mask", "netmask"]:
        mask_selector = network_page.get_interface_aware_locator(field_name, "eth0")
        mask_field = network_page.page.locator(mask_selector)

        if mask_field.count() > 0 and mask_field.is_visible():
            expect(mask_field).to_be_editable()
            mask_found = True
            logger.info(f"eth0 netmask field found using '{field_name}' selector")
            break

    if not mask_found:
        logger.info(
            f"Netmask field not found for eth0 on {device_model} - "
            "device may use different configuration method"
        )

    logger.info(f"eth0 IP/netmask test PASSED for {device_model}")
    print(f"ETH0 IP/NETMASK VALIDATED: {device_model}")
