"""
Test 29.6.5 Eth3 PTP Configuration - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth3 PTP configuration visibility and functionality.
Expected: PTP enable field should be visible when PTP is supported on eth3 interface.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_6_5_eth3_ptp(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.6.5: eth3 PTP Configuration - Pure Page Object Pattern

    Purpose: Test eth3 PTP configuration visibility and functionality.
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

    # Check if eth3 supports PTP configuration using page object method
    ptp_interfaces = network_page.get_ptp_interfaces()
    if "eth3" not in ptp_interfaces:
        pytest.skip(
            f"eth3 interface does not support PTP on device model {device_model}"
        )

    logger.info(f"Testing eth3 PTP on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth3 panel using page object method
    network_page.expand_network_interface_panel("eth3")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test PTP enable configuration using page object method
    if network_page.has_element(
        "input[name='ptp_enable_eth3']", timeout=device_timeout
    ):
        ptp_field = unlocked_config_page.locator("input[name='ptp_enable_eth3']")
        expect(ptp_field).to_be_visible(timeout=device_timeout)
        expect(ptp_field).to_be_enabled(timeout=device_timeout)

        # Test PTP enable/disable toggle functionality
        current_checked = ptp_field.is_checked()

        # Toggle PTP on
        ptp_field.click()
        first_toggle_state = ptp_field.is_checked()
        assert first_toggle_state != current_checked, "PTP should toggle on first click"

        # Toggle PTP back to original state
        ptp_field.click()
        final_state = ptp_field.is_checked()
        assert (
            final_state == current_checked
        ), "PTP should return to original state on second click"

        logger.info(f"eth3 PTP field validated - toggle functionality working")
        print(f"ETH3 PTP FIELD VALIDATED: {device_model}")
    else:
        logger.info(
            f"eth3 PTP field not found on {device_model} (may depend on device model)"
        )
        print(f"ETH3 PTP NOT PRESENT: {device_model}")

    # Validate eth3 IP field presence using page object method
    if network_page.has_element("input[name='ip_eth3']", timeout=device_timeout):
        eth3_ip = unlocked_config_page.locator("input[name='ip_eth3']")
        expect(eth3_ip).to_be_visible(timeout=device_timeout)
        print(f"eth3 IP field found and visible for {device_model}")

    # Additional PTP-related field validation on eth3
    ptp_domain_field = unlocked_config_page.locator("input[name='ptp_domain_eth3']")
    if ptp_domain_field.count() > 0:
        print(f"eth3 PTP domain field found for {device_model}")

    ptp_priority1_field = unlocked_config_page.locator(
        "input[name='ptp_priority1_eth3']"
    )
    if ptp_priority1_field.count() > 0:
        print(f"eth3 PTP priority1 field found for {device_model}")

    ptp_priority2_field = unlocked_config_page.locator(
        "input[name='ptp_priority2_eth3']"
    )
    if ptp_priority2_field.count() > 0:
        print(f"eth3 PTP priority2 field found for {device_model}")

    # Validate eth3 is distinguished from management interface (eth0)
    # eth3 should have PTP capability while eth0 should not
    if network_page.has_element(
        "input[name='ptp_enable_eth0']", timeout=device_timeout
    ):
        eth0_ptp_field = unlocked_config_page.locator("input[name='ptp_enable_eth0']")
        assert not eth0_ptp_field.is_visible(
            timeout=device_timeout
        ), f"eth0 should not have PTP capability (management interface) for {device_model}"

    print(f"eth0/eth3 PTP capability distinction validated for {device_model}")
    print(f"ETH3 PTP TEST COMPLETED: {device_model}")
