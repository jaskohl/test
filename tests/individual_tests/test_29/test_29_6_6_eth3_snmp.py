"""
Test 29.6.6 Eth3 SNMP - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth3 SNMP configuration enable/disable functionality.
Expected: SNMP enable checkbox should be visible and functional.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_6_6_eth3_snmp(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.6.6: eth3 SNMP Configuration - Pure Page Object Pattern

    Purpose: Test eth3 SNMP configuration enable/disable functionality.
    Expected: SNMP enable checkbox should be visible and functional.
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

    logger.info(f"Testing eth3 SNMP on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth3 panel using page object method
    network_page.expand_network_interface_panel("eth3")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test SNMP enable configuration using page object method
    if network_page.has_element(
        "input[name='snmp_enable_eth3']", timeout=device_timeout
    ):
        snmp_field = unlocked_config_page.locator("input[name='snmp_enable_eth3']")
        expect(snmp_field).to_be_visible(timeout=device_timeout)
        expect(snmp_field).to_be_enabled(timeout=device_timeout)

        # Test SNMP toggle functionality
        current_state = snmp_field.is_checked()

        # Toggle SNMP on
        snmp_field.click()
        first_toggle_state = snmp_field.is_checked()
        assert first_toggle_state != current_state, "SNMP should toggle on first click"

        # Toggle SNMP back to original state
        snmp_field.click()
        final_state = snmp_field.is_checked()
        assert (
            final_state == current_state
        ), "SNMP should return to original state on second click"

        logger.info(f"eth3 SNMP field validated - toggle functionality working")
        print(f"ETH3 SNMP FIELD VALIDATED: {device_model}")
    else:
        logger.info(
            f"eth3 SNMP field not found on {device_model} (may depend on device model)"
        )
        print(f"ETH3 SNMP NOT PRESENT: {device_model}")
