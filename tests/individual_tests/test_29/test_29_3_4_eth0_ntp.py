"""
Test 29.3.4 Eth0 NTP Configuration - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth0 NTP enable/disable checkbox functionality.
Expected: NTP enable checkbox visible and enabled for Series 3.

PATTERN: PURE PAGE OBJECT - No direct DeviceCapabilities calls
REFACTORED: Uses NetworkConfigPage methods instead of direct DeviceCapabilities.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_3_4_eth0_ntp(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.3.4: eth0 NTP Configuration - Pure Page Object Pattern

    Purpose: Test eth0 NTP enable/disable checkbox functionality.
    Pattern: PURE PAGE OBJECT - No direct DeviceCapabilities calls
    """
    # Get device model from session
    device_model = (
        request.session.device_hardware_model
        if hasattr(request.session, "device_hardware_model")
        else "unknown"
    )
    if not device_model or device_model == "Unknown":
        pytest.fail("Device model not detected")

    # Create page object with device_model
    network_page = NetworkConfigPage(unlocked_config_page, device_model=device_model)

    # Validate Series 3 requirement using page object
    device_series = network_page.get_series()
    if device_series != 3:
        pytest.skip(f"Series 3 only (detected Series {device_series})")

    logger.info(f"Testing eth0 NTP on {device_model}")

    # Navigate and verify page loaded using page object
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth0 panel using page object method
    try:
        panel_expanded = network_page.expand_eth0_panel()
        if panel_expanded:
            logger.info("eth0 panel expanded successfully via page object")
        else:
            logger.warning(
                "eth0 panel expansion returned false - may already be expanded"
            )
    except Exception as e:
        logger.warning(f"eth0 panel expansion failed for {device_model}: {e}")
        # Panel expansion is optional - continue with test

    # Get device-aware timeout through page object
    timeout_multiplier = network_page.get_timeout_multiplier()
    device_timeout = int(5000 * timeout_multiplier)

    # Test NTP enable checkbox using page object method
    try:
        ntp_locator = network_page.get_eth0_ntp_enable_field_locator()

        expect(ntp_locator).to_be_visible(timeout=device_timeout)
        expect(ntp_locator).to_be_enabled(timeout=device_timeout)

        logger.info(f"eth0 NTP checkbox validated - visible and enabled")

    except Exception as e:
        pytest.fail(f"eth0 NTP checkbox validation failed on {device_model}: {e}")

    # Additional validation through page object capabilities
    network_capable = network_page.has_capability("network")
    if not network_capable:
        pytest.skip(f"Device {device_model} does not support network configuration")

    # Log comprehensive test results through page object
    device_info = network_page.get_device_info()
    logger.info(f"eth0 NTP test completed for {device_model}: {device_info}")

    print(f"ETH0 NTP VALIDATED: {device_model}")

    # Additional validation - get eth0 NTP configuration through page object
    try:
        eth0_ntp_config = network_page.get_eth0_ntp_configuration()
        if eth0_ntp_config:
            logger.info(
                f"eth0 NTP configuration retrieved through page object: {eth0_ntp_config}"
            )
        else:
            logger.info(
                f"No eth0 NTP configuration retrieved through page object for {device_model}"
            )
    except Exception as e:
        logger.warning(
            f"eth0 NTP configuration retrieval failed for {device_model}: {e}"
        )
