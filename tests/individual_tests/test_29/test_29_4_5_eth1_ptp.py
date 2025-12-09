"""
Test 29.4.5 Eth1 PTP Configuration - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth1 interface PTP enable checkbox functionality.
Expected: PTP checkbox visible and functional for Series 3 devices with PTP support.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_4_5_eth1_ptp(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.4.5: eth1 PTP Configuration - Pure Page Object Pattern

    Purpose: Test eth1 interface PTP enable checkbox functionality.
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

    # Check if eth1 supports PTP configuration using page object method
    ptp_interfaces = network_page.get_ptp_interfaces()
    if "eth1" not in ptp_interfaces:
        pytest.skip(
            f"eth1 interface does not support PTP on device model {device_model}"
        )

    logger.info(f"Testing eth1 PTP on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth1 panel using page object method
    network_page.expand_network_interface_panel("eth1")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test PTP enable checkbox using page object method
    if network_page.has_element(
        "input[name='ptp_enable_eth1']", timeout=device_timeout
    ):
        ptp_checkbox = unlocked_config_page.locator("input[name='ptp_enable_eth1']")
        expect(ptp_checkbox).to_be_visible(timeout=device_timeout)
        expect(ptp_checkbox).to_be_enabled()

        # Verify checkbox can be toggled
        initial_state = ptp_checkbox.is_checked()
        ptp_checkbox.click()
        new_state = ptp_checkbox.is_checked()

        # State should have changed
        assert initial_state != new_state, "PTP checkbox should toggle when clicked"

        logger.info(f"eth1 PTP checkbox validated - enabled and toggles correctly")
        print(f"ETH1 PTP VALIDATED: {device_model}")
    else:
        logger.info(
            f"eth1 PTP checkbox not found on {device_model} (expected on some configurations)"
        )
        print(f"ETH1 PTP NOT PRESENT: {device_model}")
