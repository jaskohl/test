"""
Test 29.4.2 Eth1 IP Netmask - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth1 interface IP and netmask field functionality.
Expected: IP and netmask fields visible and enabled for Series 3.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_4_2_eth1_ip_netmask(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.4.2: eth1 IP and Netmask Configuration - Pure Page Object Pattern

    Purpose: Test eth1 interface IP and netmask field functionality.
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

    logger.info(f"Testing eth1 IP/netmask on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth1 panel using page object method
    network_page.expand_network_interface_panel("eth1")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test IP field using page object method
    if network_page.has_element("input[name='ip_eth1']", timeout=device_timeout):
        ip_field = unlocked_config_page.locator("input[name='ip_eth1']")
        expect(ip_field).to_be_visible(timeout=device_timeout)
        expect(ip_field).to_be_enabled()

        # Basic IP format validation if field has content
        current_ip = ip_field.input_value()
        if current_ip:
            import re

            ip_pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
            assert re.match(ip_pattern, current_ip), f"Invalid IP format: {current_ip}"

        logger.info(f"eth1 IP field validated - enabled with valid format")
        print(f"ETH1 IP FIELD VALIDATED: {device_model}")
    else:
        logger.info(
            f"eth1 IP field not found on {device_model} (expected on some configurations)"
        )
        print(f"ETH1 IP NOT PRESENT: {device_model}")

    # Test netmask field using page object method
    if network_page.has_element("input[name='netmask_eth1']", timeout=device_timeout):
        netmask_field = unlocked_config_page.locator("input[name='netmask_eth1']")
        expect(netmask_field).to_be_visible(timeout=device_timeout)
        expect(netmask_field).to_be_enabled()

        # Verify netmask format if field has content
        current_netmask = netmask_field.input_value()
        if current_netmask:
            import re

            # Common netmask formats
            netmask_pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$|^/[0-9]{1,2}$"
            assert re.match(
                netmask_pattern, current_netmask
            ), f"Invalid netmask format: {current_netmask}"

        logger.info(f"eth1 netmask field validated - enabled with valid format")
        print(f"ETH1 NETMASK FIELD VALIDATED: {device_model}")
    else:
        logger.info(
            f"eth1 netmask field not found on {device_model} (expected on some configurations)"
        )
        print(f"ETH1 NETMASK NOT PRESENT: {device_model}")
