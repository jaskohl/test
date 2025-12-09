"""
Test 29.6.2 Eth3 IP Netmask - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth3 IP address and netmask configuration.
Expected: IP field editable, netmask field visible and functional.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_6_2_eth3_ip_netmask(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.6.2: eth3 IP and Netmask Configuration - Pure Page Object Pattern

    Purpose: Test eth3 IP address and netmask configuration.
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

    logger.info(f"Testing eth3 IP/netmask on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth3 panel using page object method
    network_page.expand_network_interface_panel("eth3")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test eth3 IP address field using page object method
    if network_page.has_element("input[name='ip_eth3']", timeout=device_timeout):
        eth3_ip_field = unlocked_config_page.locator("input[name='ip_eth3']")
        expect(eth3_ip_field).to_be_visible(timeout=device_timeout)
        expect(eth3_ip_field).to_be_editable()

        # Test valid IP address inputs
        test_ips = ["192.168.3.10", "10.0.0.50", "172.16.25.100"]
        for test_ip in test_ips:
            eth3_ip_field.fill(test_ip)
            actual_value = eth3_ip_field.input_value()
            assert (
                actual_value == test_ip
            ), f"IP address {test_ip} not accepted, got {actual_value}"

        # Restore default test IP
        eth3_ip_field.fill("192.168.3.10")
        logger.info(f"eth3 IP address field validated - editable and accepts valid IPs")
        print(f"ETH3 IP FIELD VALIDATED: {device_model}")
    else:
        logger.info(
            f"eth3 IP field not found on {device_model} (may depend on device model)"
        )
        print(f"ETH3 IP NOT PRESENT: {device_model}")

    # Test eth3 netmask field using page object method
    netmask_selectors = [
        "input[name='mask_eth3']",
        "input[name='netmask_eth3']",
        "select[name='netmask_eth3']",
    ]

    netmask_field_found = False
    for selector in netmask_selectors:
        if network_page.has_element(selector, timeout=device_timeout):
            netmask_field_found = True
            logger.info(f"eth3 netmask field found using selector '{selector}'")
            break

    if netmask_field_found:
        netmask_field = unlocked_config_page.locator(netmask_selectors[0])
        # Try to find the correct selector that was found
        for selector in netmask_selectors:
            potential_field = unlocked_config_page.locator(selector)
            if potential_field.count() > 0:
                netmask_field = potential_field
                break

        if "select" in selector:
            expect(netmask_field).to_be_enabled()
            option_count = netmask_field.locator("option").count()
            assert (
                option_count >= 1
            ), f"Netmask dropdown should have options, found {option_count}"
        else:
            expect(netmask_field).to_be_editable()

        logger.info(f"eth3 netmask field validated using selector '{selector}'")
        print(f"ETH3 NETMASK FIELD VALIDATED: {device_model}")
    else:
        logger.info(
            f"eth3 netmask field not found on {device_model} (may depend on device model)"
        )
        print(f"ETH3 NETMASK NOT PRESENT: {device_model}")
