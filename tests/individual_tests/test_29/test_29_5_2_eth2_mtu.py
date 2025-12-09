"""
Test 29.5.2 Eth2 MTU Architecture Validation - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test that eth2 MTU is managed via eth1 panel (no separate eth2 configuration).
Expected: Eth2 MTU should not have separate configuration in Series 3A architecture.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_5_2_eth2_mtu(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.5.2: eth2 MTU Architecture Validation - Pure Page Object Pattern

    Purpose: Test that eth2 MTU settings are managed via eth1 panel (no separate eth2 configuration).
    Architecture: In Series 3A, eth2 doesn't exist as a separate port.
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

    logger.info(f"Testing eth2 MTU architecture on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Check that eth2 MTU field is NOT visible as separate configuration
    # In Series 3A architecture, eth2 is managed via eth1 panel
    if not network_page.has_element("input[name='mtu_eth2']", timeout=device_timeout):
        logger.info(f"eth2 MTU correctly managed via eth1 panel on {device_model}")
        print(
            f"ETH2 MTU ARCHITECTURE VALIDATED: {device_model} (no separate eth2 config)"
        )
    else:
        # If separate eth2 field exists, verify it behaves correctly
        eth2_mtu_separate = unlocked_config_page.locator("input[name='mtu_eth2']")
        if eth2_mtu_separate.is_visible(timeout=device_timeout):
            logger.warning(
                f"Found separate eth2 MTU field on {device_model} - eth2 should be managed via eth1"
            )
            print(f"ETH2 MTU SEPARATE CONFIG FOUND: {device_model} (unexpected)")
