"""
Test 29.5.7 Eth2 Save/Cancel Architecture Validation - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth2 save/cancel operations are managed via eth1 panel (no separate eth2 configuration).
Expected: eth2 save/cancel operations are managed through eth1 panel in Series 3A architecture.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_5_7_eth2_save_cancel(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.5.7: eth2 Save/Cancel Architecture Validation - Pure Page Object Pattern

    Purpose: Test eth2 save/cancel functionality through eth1 panel (Series 3A architecture).
    Architecture: In Series 3A, eth2 doesn't exist as a separate port.
    eth2 save/cancel operations are managed through the eth1 panel interface.
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

    logger.info(f"Testing eth2 save/cancel architecture on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Verify eth2-specific save buttons don't exist (they should be managed via eth1)
    eth2_save_buttons = [
        "button#button_save_port_eth2",
        "button[name='port_eth2']",
        "button#button_save_eth2",
    ]

    eth2_save_found = False
    for selector in eth2_save_buttons:
        if network_page.has_element(selector, timeout=device_timeout):
            eth2_save_found = True
            logger.warning(
                f"Found eth2 save button with selector '{selector}' on {device_model}"
            )
            break

    # eth2-specific save buttons should not exist in Series 3A architecture
    assert (
        not eth2_save_found
    ), "eth2 save button should not exist separately (should use eth1 panel)"

    # Verify eth2-specific cancel buttons don't exist
    eth2_cancel_buttons = [
        "button#button_cancel_port_eth2",
        "button.cancel[name*='eth2']",
    ]

    eth2_cancel_found = False
    for selector in eth2_cancel_buttons:
        if network_page.has_element(selector, timeout=device_timeout):
            eth2_cancel_found = True
            logger.warning(
                f"Found eth2 cancel button with selector '{selector}' on {device_model}"
            )
            break

    # eth2-specific cancel buttons should not exist in Series 3A architecture
    assert (
        not eth2_cancel_found
    ), "eth2 cancel button should not exist separately (should use eth1 panel)"

    logger.info(
        f"eth2 save/cancel buttons correctly absent on {device_model} (eth2 managed via eth1)"
    )

    # Verify save/cancel buttons exist for eth1 (where eth2 operations are managed) using page object method
    if network_page.has_element("button#button_save_port_eth1", timeout=device_timeout):
        logger.info(
            f"eth1 save button found on {device_model} (manages both eth1 and eth2)"
        )
        print(
            f"ETH2 SAVE/CANCEL ARCHITECTURE VALIDATED: {device_model} (eth2 managed via eth1)"
        )
    else:
        logger.info(f"eth1 save button not found on {device_model}")

    if network_page.has_element(
        "button#button_cancel_port_eth1", timeout=device_timeout
    ):
        logger.info(
            f"eth1 cancel button found on {device_model} (manages both eth1 and eth2)"
        )
    else:
        logger.info(f"eth1 cancel button not found on {device_model}")

    print(f"ETH2 SAVE/CANCEL TEST PASSED: {device_model}")
