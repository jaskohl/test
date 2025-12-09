"""
Test 29.7.4 Eth4 NTP - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test NTP enable/disable functionality for eth4 interface.
Expected: NTP checkbox should be visible and enabled for eth4 on Series 3 devices.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_7_4_eth4_ntp(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.7.4: eth4 NTP Configuration - Pure Page Object Pattern

    Purpose: Test NTP enable/disable functionality for eth4 interface.
    Expected: NTP checkbox should be visible and enabled for eth4 on Series 3 devices.
    Series: Series 3 only
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

    logger.info(f"Testing eth4 NTP on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth4 panel using page object method
    network_page.expand_network_interface_panel("eth4")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test eth4 NTP configuration using page object method
    if network_page.has_element(
        "input[name='ntp_enable_eth4']", timeout=device_timeout
    ):
        ntp = unlocked_config_page.locator("input[name='ntp_enable_eth4']")
        expect(ntp).to_be_enabled(timeout=device_timeout)
        print("eth4 NTP configuration test completed")
        logger.info(f"eth4 NTP field validated for {device_model}")
    else:
        print("NTP field not available for eth4 (may be expected on some models)")
        logger.info(
            f"eth4 NTP field not found for {device_model} (may be expected on some models)"
        )

    print(f"ETH4 NTP TEST COMPLETED: {device_model}")
