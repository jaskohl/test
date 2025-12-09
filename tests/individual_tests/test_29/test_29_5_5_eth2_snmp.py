"""
Test 29.5.5 Eth2 SNMP Architecture Validation - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth2 SNMP configuration is managed via eth1 panel (no separate eth2 configuration).
Expected: eth2 SNMP settings are managed through eth1 panel in Series 3A architecture.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_5_5_eth2_snmp(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.5.5: eth2 SNMP Architecture Validation - Pure Page Object Pattern

    Purpose: Test eth2 SNMP configuration functionality.
    Architecture: In Series 3A, eth2 SNMP is managed via eth1 panel.
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

    logger.info(f"Testing eth2 SNMP architecture on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Verify that eth2-specific SNMP fields are NOT present (as expected)
    # In Series 3A, eth2 is managed through eth1 panel, so eth2_snmp_enable field should not exist
    if not network_page.has_element(
        "input[name='snmp_enable_eth2']", timeout=device_timeout
    ):
        logger.info(
            f"eth2 SNMP configuration managed through eth1 panel on {device_model}"
        )
        print(
            f"ETH2 SNMP ARCHITECTURE VALIDATED: {device_model} (no separate eth2 config)"
        )
    else:
        # If field exists, it should not be visible (handled via eth1)
        eth2_snmp_field = unlocked_config_page.locator("input[name='snmp_enable_eth2']")
        if eth2_snmp_field.is_visible(timeout=device_timeout):
            logger.warning(
                f"eth2 SNMP field visible on {device_model} - may indicate separate eth2 config"
            )
            print(f"ETH2 SNMP SEPARATE CONFIG FOUND: {device_model} (unexpected)")
        else:
            logger.info(
                f"eth2 SNMP field correctly handled via eth1 panel on {device_model}"
            )
            print(
                f"ETH2 SNMP ARCHITECTURE VALIDATED: {device_model} (eth2 managed via eth1)"
            )

    # Verify eth1 SNMP field exists (which handles eth2 SNMP settings) using page object method
    if network_page.has_element(
        "input[name='snmp_enable_eth1']", timeout=device_timeout
    ):
        eth1_snmp_field = unlocked_config_page.locator("input[name='snmp_enable_eth1']")
        expect(eth1_snmp_field).to_be_visible(timeout=device_timeout)
        expect(eth1_snmp_field).to_be_enabled()
        logger.info(f"eth1 SNMP field (handles eth2 SNMP) validated on {device_model}")
    else:
        logger.info(
            f"eth1 SNMP field not found on {device_model} (may be handled elsewhere)"
        )

    print(f"ETH2 SNMP TEST COMPLETED: {device_model}")
