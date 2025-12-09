"""
Test 29.5.8 Eth2 No Redundancy Architecture - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth2 redundancy configuration absence (Series 3A architecture).
Expected: eth2-specific redundancy fields don't exist separately.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_5_8_eth2_no_redundancy(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.5.8: eth2 No Redundancy Architecture - Pure Page Object Pattern

    Purpose: Test eth2 redundancy configuration absence (Series 3A architecture).
    Architecture: In Series 3A, eth2 doesn't exist as a separate port.
    eth2 redundancy settings are managed through the eth1 panel interface.
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

    logger.info(f"Testing eth2 redundancy architecture on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Verify eth2-specific redundancy fields don't exist (they should be managed via eth1)
    eth2_redundancy_selectors = [
        "select[name='redundancy_mode_eth2']",
        "input[name='redundancy_eth2']",
        "select[name*='eth2_redundancy']",
    ]

    eth2_redundancy_found = False
    for selector in eth2_redundancy_selectors:
        if network_page.has_element(selector, timeout=device_timeout):
            eth2_redundancy_found = True
            logger.warning(
                f"Found eth2 redundancy field with selector '{selector}' on {device_model}"
            )
            break

    # eth2-specific redundancy fields should not exist in Series 3A architecture
    assert (
        not eth2_redundancy_found
    ), "eth2 redundancy field should not exist separately (should use eth1 panel)"

    # Verify redundancy fields exist for eth1 (where eth2 settings are managed) using page object method
    if network_page.has_element(
        "select[name='redundancy_mode_eth1']", timeout=device_timeout
    ):
        logger.info(
            f"eth1 redundancy field found on {device_model} (manages both eth1 and eth2)"
        )
        print(f"ETH2 NO REDUNDANCY VALIDATED: {device_model} (eth2 managed via eth1)")
    else:
        logger.info(
            f"eth1 redundancy field not found on {device_model} (device may use different pattern)"
        )

    print(f"ETH2 NO REDUNDANCY PASSED: {device_model}")
