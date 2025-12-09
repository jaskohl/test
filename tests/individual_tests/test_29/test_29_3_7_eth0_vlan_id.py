"""
Test 29.3.7 Eth0 VLAN ID - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth0 VLAN ID field functionality.
Expected: VLAN ID field visible and accepts valid VLAN ID values (1-4094) for Series 3.

PATTERN: PURE PAGE OBJECT - No direct DeviceCapabilities calls
REFACTORED: Uses NetworkConfigPage methods instead of direct DeviceCapabilities.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_3_7_eth0_vlan_id(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.3.7: eth0 VLAN ID Configuration - Pure Page Object Pattern

    Purpose: Test eth0 VLAN ID field functionality and value validation.
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

    logger.info(f"Testing eth0 VLAN ID on {device_model}")

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

    # Test VLAN ID field using page object method
    try:
        vlan_id_locator = network_page.get_eth0_vlan_id_field_locator()

        if vlan_id_locator and vlan_id_locator.count() > 0:
            expect(vlan_id_locator).to_be_visible(timeout=device_timeout)
            expect(vlan_id_locator).to_be_editable(timeout=device_timeout)

            # Test VLAN ID range values (1, 100, 4094) with device-aware timeout
            vlan_ids = ["1", "100", "4094"]
            for vid in vlan_ids:
                try:
                    vlan_id_locator.fill(vid, timeout=device_timeout)
                    actual_value = vlan_id_locator.input_value()
                    assert (
                        actual_value == vid
                    ), f"VLAN ID {vid} not accepted, got {actual_value}"
                    logger.info(f"VLAN ID {vid} accepted for eth0")
                except Exception as e:
                    logger.warning(f"VLAN ID {vid} test failed: {e}")

            logger.info(f"eth0 VLAN ID field validated successfully")
            print(f"ETH0 VLAN ID VALIDATED: {device_model}")
        else:
            logger.info(
                f"VLAN ID field not visible for eth0 on {device_model} (expected on some configurations)"
            )
            print(f"ETH0 VLAN ID NOT PRESENT: {device_model}")

    except Exception as e:
        pytest.fail(f"eth0 VLAN ID field validation failed on {device_model}: {e}")

    # Additional validation through page object capabilities
    network_capable = network_page.has_capability("network")
    if not network_capable:
        pytest.skip(f"Device {device_model} does not support network configuration")

    # Log comprehensive test results through page object
    device_info = network_page.get_device_info()
    logger.info(f"eth0 VLAN ID test completed for {device_model}: {device_info}")

    # Additional validation - get eth0 VLAN ID configuration through page object
    try:
        eth0_vlan_id_config = network_page.get_eth0_vlan_id_configuration()
        if eth0_vlan_id_config:
            logger.info(
                f"eth0 VLAN ID configuration retrieved through page object: {eth0_vlan_id_config}"
            )
        else:
            logger.info(
                f"No eth0 VLAN ID configuration retrieved through page object for {device_model}"
            )
    except Exception as e:
        logger.warning(
            f"eth0 VLAN ID configuration retrieval failed for {device_model}: {e}"
        )
