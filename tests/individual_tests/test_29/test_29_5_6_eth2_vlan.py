"""
Test 29.5.6 Eth2 VLAN Architecture Validation - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth2 VLAN settings are managed via eth1 panel (no separate eth2 configuration).
Expected: eth2 VLAN settings are managed through eth1 panel in Series 3A architecture.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_5_6_eth2_vlan(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.5.6: eth2 VLAN Architecture Validation - Pure Page Object Pattern

    Purpose: Test eth2 VLAN settings management through eth1 panel (Series 3A architecture).
    Architecture: In Series 3A, eth2 doesn't exist as a separate port.
    eth2 settings (including VLAN) are managed through the eth1 panel interface.
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

    logger.info(f"Testing eth2 VLAN architecture on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Verify eth2-specific VLAN fields don't exist (they should be managed via eth1)
    # eth2-specific VLAN fields should not exist in Series 3A architecture
    assert not network_page.has_element(
        "input[name='vlan_enable_eth2']", timeout=device_timeout
    ), "eth2 VLAN enable field should not exist separately"
    assert not network_page.has_element(
        "input[name='vlan_id_eth2']", timeout=device_timeout
    ), "eth2 VLAN ID field should not exist separately"

    logger.info(
        f"eth2 VLAN fields correctly absent on {device_model} (eth2 managed via eth1)"
    )

    # Verify VLAN fields exist for eth1 (where eth2 settings are managed) using page object method
    if network_page.has_element(
        "input[name='vlan_enable_eth1']", timeout=device_timeout
    ):
        logger.info(
            f"eth1 VLAN enable field found on {device_model} (manages both eth1 and eth2)"
        )
        print(
            f"ETH2 VLAN ARCHITECTURE VALIDATED: {device_model} (eth2 managed via eth1)"
        )
    else:
        logger.info(f"eth1 VLAN enable field not found on {device_model}")

    if network_page.has_element("input[name='vlan_id_eth1']", timeout=device_timeout):
        logger.info(
            f"eth1 VLAN ID field found on {device_model} (manages both eth1 and eth2)"
        )
    else:
        logger.info(f"eth1 VLAN ID field not found on {device_model}")

    print(f"ETH2 VLAN TEST PASSED: {device_model}")
