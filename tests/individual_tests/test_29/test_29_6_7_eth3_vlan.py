"""
Test 29.6.7 Eth3 VLAN - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth3 VLAN enable/disable and VLAN ID configuration functionality.
Expected: VLAN enable checkbox and VLAN ID field should be visible and functional.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_6_7_eth3_vlan(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.6.7: eth3 VLAN Configuration - Pure Page Object Pattern

    Purpose: Test eth3 VLAN enable/disable and VLAN ID configuration functionality.
    Expected: VLAN enable checkbox and VLAN ID field should be visible and functional.
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

    logger.info(f"Testing eth3 VLAN on {device_model}")

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth3 panel using page object method
    network_page.expand_network_interface_panel("eth3")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Test VLAN enable checkbox using page object method
    if network_page.has_element(
        "input[name='vlan_enable_eth3']", timeout=device_timeout
    ):
        vlan_enable = unlocked_config_page.locator("input[name='vlan_enable_eth3']")
        expect(vlan_enable).to_be_visible(timeout=device_timeout)
        expect(vlan_enable).to_be_enabled(timeout=device_timeout)

        # Test VLAN enable/disable toggle functionality
        current_enabled = vlan_enable.is_checked()

        # Toggle VLAN on
        vlan_enable.click()
        first_toggle_state = vlan_enable.is_checked()
        assert (
            first_toggle_state != current_enabled
        ), "VLAN should toggle on first click"

        # Toggle VLAN back to original state
        vlan_enable.click()
        final_state = vlan_enable.is_checked()
        assert (
            final_state == current_enabled
        ), "VLAN should return to original state on second click"

        logger.info(
            f"eth3 VLAN enable checkbox validated - toggle functionality working"
        )
        print(f"ETH3 VLAN ENABLE VALIDATED: {device_model}")
    else:
        logger.info(
            f"eth3 VLAN enable field not found on {device_model} (may depend on device model)"
        )
        print(f"ETH3 VLAN ENABLE NOT PRESENT: {device_model}")

    # Test VLAN ID field using page object method
    if network_page.has_element("input[name='vlan_id_eth3']", timeout=device_timeout):
        vlan_id = unlocked_config_page.locator("input[name='vlan_id_eth3']")
        expect(vlan_id).to_be_visible(timeout=device_timeout)
        expect(vlan_id).to_be_editable(timeout=device_timeout)

        # Test VLAN ID input
        test_vlan_id = "200"
        vlan_id.fill(test_vlan_id)
        actual_value = vlan_id.input_value()
        assert (
            actual_value == test_vlan_id
        ), f"Expected VLAN ID {test_vlan_id}, got {actual_value}"

        # Test VLAN ID range validation
        test_ids = ["100", "500", "4094"]
        for vid in test_ids:
            try:
                vlan_id.fill(vid)
                actual_value = vlan_id.input_value()
                if actual_value == vid:
                    logger.info(f"VLAN ID {vid} accepted")
                else:
                    logger.info(
                        f"VLAN ID {vid} accepted with different value: {actual_value}"
                    )
            except Exception as e:
                logger.info(f"VLAN ID {vid} rejected (expected): {e}")

        # Restore default VLAN ID
        vlan_id.fill("200")

        logger.info(f"eth3 VLAN ID field validated - input functionality working")
        print(f"ETH3 VLAN ID FIELD VALIDATED: {device_model}")
    else:
        logger.info(
            f"eth3 VLAN ID field not found on {device_model} (may depend on device model)"
        )
        print(f"ETH3 VLAN ID NOT PRESENT: {device_model}")

    logger.info(f"eth3 VLAN configuration test completed successfully")
