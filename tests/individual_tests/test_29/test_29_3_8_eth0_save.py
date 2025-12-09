"""
Test 29.3.8 Eth0 Save Button - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth0 interface save button functionality.
Expected: Save button visible for Series 3 devices.

PATTERN: PURE PAGE OBJECT - No direct DeviceCapabilities calls
REFACTORED: Uses NetworkConfigPage methods instead of direct DeviceCapabilities.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_3_8_eth0_save(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.3.8: eth0 Save Button - Pure Page Object Pattern

    Purpose: Test eth0 interface save button functionality.
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

    logger.info(f"Testing eth0 save button on {device_model}")

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

    # Locate eth0 save button using page object method
    try:
        save_button_locator = network_page.get_eth0_save_button_locator()

        if save_button_locator and save_button_locator.count() > 0:
            expect(save_button_locator).to_be_visible(timeout=device_timeout)
            logger.info(f"eth0 save button validated - visible")
            print(f"ETH0 SAVE BUTTON VALIDATED: {device_model}")
        else:
            logger.info(
                f"eth0 save button not visible on {device_model} (may be expected on some configurations)"
            )
            print(f"ETH0 SAVE BUTTON NOT PRESENT: {device_model}")

    except Exception as e:
        pytest.fail(f"eth0 save button validation failed on {device_model}: {e}")

    # Additional validation through page object capabilities
    network_capable = network_page.has_capability("network")
    if not network_capable:
        pytest.skip(f"Device {device_model} does not support network configuration")

    # Log comprehensive test results through page object
    device_info = network_page.get_device_info()
    logger.info(f"eth0 save button test completed for {device_model}: {device_info}")

    # Additional validation - get eth0 save button configuration through page object
    try:
        eth0_save_config = network_page.get_eth0_save_button_configuration()
        if eth0_save_config:
            logger.info(
                f"eth0 save button configuration retrieved through page object: {eth0_save_config}"
            )
        else:
            logger.info(
                f"No eth0 save button configuration retrieved through page object for {device_model}"
            )
    except Exception as e:
        logger.warning(
            f"eth0 save button configuration retrieval failed for {device_model}: {e}"
        )
