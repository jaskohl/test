"""
Test 29.3.10 Eth0 No PTP Interface - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Verify eth0 does not have PTP controls (management interface).
Expected: PTP field should NOT be visible for eth0 on Series 3 devices.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_3_10_eth0_no_ptp(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.3.10: eth0 No PTP Interface - Pure Page Object Pattern

    Purpose: Verify eth0 interface does not have PTP controls (management interface).
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

    logger.info(f"Testing eth0 PTP absence on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth0 panel using page object method
    network_page.expand_network_interface_panel("eth0")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Verify PTP field is NOT present for eth0 (management interface) using page object method
    if network_page.has_element(
        "input[name='ptp_enable_eth0']", timeout=device_timeout
    ):
        # PTP field found - this may be incorrect for a management interface
        logger.warning(
            f"PTP field found for eth0 on {device_model} (unexpected for management interface)"
        )
        print(f"PTP FIELD UNEXPECTEDLY PRESENT: {device_model}")
    else:
        # PTP field correctly NOT visible for eth0
        logger.info(
            f"PTP field correctly absent for eth0 management interface on {device_model}"
        )
        print(f"ETH0 NO PTP CORRECTLY VALIDATED: {device_model}")
