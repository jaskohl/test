"""
Test 29.7.1 Eth4 Presence - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Verify eth4 interface presence and visibility with device-aware patterns.
Expected: Test should verify eth4 IP field presence and editability using page object methods.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_7_1_eth4_presence(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.7.1: Eth4 Presence - Pure Page Object Pattern

    Purpose: Verify eth4 interface presence and visibility with device-aware patterns.
    """
    # Get device model from session
    device_model = request.session.device_hardware_model
    if not device_model or device_model == "Unknown":
        pytest.fail("Device model not detected - cannot determine network capabilities")

    # Create page object with device_model
    network_page = NetworkConfigPage(unlocked_config_page, device_model=device_model)

    # Validate Series 3 requirement using page object method
    device_series = network_page.get_series()
    if device_series != 3:
        pytest.skip(
            f"eth4 presence tests apply to Series 3 devices only (detected: Series {device_series})"
        )

    logger.info(f"Testing eth4 presence on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth4 panel using page object method
    network_page.expand_network_interface_panel("eth4")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Cross-validate eth4 availability using page object method
    network_interfaces = network_page.get_network_interfaces()
    eth4_available_in_capabilities = "eth4" in network_interfaces

    logger.info(
        f"eth4 availability from page object for {device_model}: {eth4_available_in_capabilities}"
    )
    logger.info(
        f"Available network interfaces for {device_model}: {network_interfaces}"
    )

    # eth4 IP field validation using page object method
    if network_page.has_element("input[name='ip_eth4']", timeout=device_timeout):
        eth4_ip = unlocked_config_page.locator("input[name='ip_eth4']")

        # Field presence and editability validation
        expect(eth4_ip).to_be_visible(timeout=device_timeout)
        expect(eth4_ip).to_be_editable()

        logger.info(
            f"eth4 interface presence verified on {device_model} - IP field visible and editable"
        )

        # Cross-validate UI presence with page object capabilities
        if eth4_available_in_capabilities:
            logger.info(
                f"eth4 presence confirmed - page object and UI both show availability for {device_model}"
            )
        else:
            logger.warning(
                f"eth4 available in UI but not in page object capabilities for {device_model}"
            )

    elif eth4_available_in_capabilities:
        # eth4 should be available according to page object but not visible in UI
        logger.warning(
            f"eth4 expected from page object but IP field not visible on {device_model}"
        )
        pytest.fail(
            f"eth4 expected to be available on {device_model} according to page object but not visible in UI"
        )
    else:
        # eth4 not available in either page object or UI - this is acceptable
        logger.info(
            f"eth4 not available on {device_model} - consistent with page object capabilities"
        )
        pytest.skip(
            f"eth4 not available on {device_model} - may not be available on this device variant"
        )

    # Validate series-specific network configuration patterns
    logger.info(
        f"eth4 presence validation completed for Series 3 device {device_model}"
    )

    print(f"ETH4 PRESENCE TEST COMPLETED: {device_model}")
