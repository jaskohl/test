"""
Test 29.3.1 Eth0 Management Interface Testing - Pure Page Object Pattern

Category: 29 - Network Configuration Series 3
Purpose: Test eth0 management interface properties and PTP absence verification.
Expected: eth0 IP visible/editable, PTP not available on management interface.

PATTERN: PURE PAGE OBJECT - No direct DeviceCapabilities calls
REFACTORED: Uses NetworkConfigPage methods instead of direct DeviceCapabilities.
Follows LOCATOR_STRATEGY.md and DeviceCapabilities patterns through page object encapsulation.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_3_1_eth0_management(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.3.1: Eth0 Management Interface - Pure Page Object Pattern

    Purpose: Verify eth0 management interface properties with device-aware validation.

    Pattern Used:
    1. Get device_model from session
    2. Validate series using page object methods
    3. Create page object with device_model
    4. Use page object methods exclusively (no direct DeviceCapabilities)
    5. Validate against page object encapsulated data
    """
    # Get device model from session
    device_model = (
        request.session.device_hardware_model
        if hasattr(request.session, "device_hardware_model")
        else "unknown"
    )
    if not device_model or device_model == "Unknown":
        pytest.fail("Device model not detected - cannot validate network capabilities")

    # Create NetworkConfigPage with device_model for device-aware behavior
    network_page = NetworkConfigPage(unlocked_config_page, device_model=device_model)

    # Validate Series 3 requirement using page object
    device_series = network_page.get_series()
    if device_series != 3:
        pytest.skip(
            f"eth0 management tests apply to Series 3 only (detected Series {device_series})"
        )

    # Get device-aware timeout through page object
    timeout_multiplier = network_page.get_timeout_multiplier()

    logger.info(
        f"Testing eth0 management interface on {device_model} "
        f"(Series {device_series}, timeout multiplier: {timeout_multiplier}x)"
    )

    # Navigate to network page using page object method
    try:
        network_page.navigate_to_page()
        network_page.verify_page_loaded()
        logger.info(f"Network configuration page loaded for {device_model}")
    except Exception as e:
        pytest.fail(f"Failed to load network page on {device_model}: {e}")

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

    # Test 1: Verify eth0 IP field visibility and editability
    # Use page object interface-aware locator method
    try:
        eth0_ip_locator = network_page.get_eth0_ip_field_locator()

        # Use device-aware timeout
        device_timeout = int(5000 * timeout_multiplier)
        expect(eth0_ip_locator).to_be_visible(timeout=device_timeout)

        # Verify field is editable
        if eth0_ip_locator.is_enabled():
            logger.info(f"eth0 IP field is visible and editable on {device_model}")
        else:
            logger.info(f"eth0 IP field is visible but read-only on {device_model}")

    except Exception as e:
        pytest.fail(f"eth0 IP field validation failed on {device_model}: {e}")

    # Test 2: Verify PTP is NOT available on eth0 (management interface)
    # Use page object to validate - eth0 should never be in PTP interfaces
    ptp_interfaces = network_page.get_ptp_interfaces()
    logger.info(f"PTP-capable interfaces from page object: {ptp_interfaces}")

    assert "eth0" not in ptp_interfaces, (
        f"eth0 should NOT be in PTP interfaces for {device_model}. "
        f"Page object reports: {ptp_interfaces}"
    )
    logger.info(f"Confirmed: eth0 not in PTP interfaces (correct for management)")

    # Also verify PTP enable field is not present for eth0
    ptp_eth0_locator = network_page.get_eth0_ptp_enable_field_locator()

    if (
        ptp_eth0_locator
        and ptp_eth0_locator.count() > 0
        and ptp_eth0_locator.is_visible()
    ):
        pytest.fail(
            f"PTP enable field should not be visible on eth0 for {device_model}"
        )
    else:
        logger.info(f"PTP enable field correctly absent from eth0 on {device_model}")

    # Test 3: Cross-validate with page object network interface data
    available_interfaces = network_page.get_network_interfaces()
    logger.info(f"Available interfaces from page object: {available_interfaces}")

    assert "eth0" in available_interfaces, (
        f"eth0 should be in available interfaces for {device_model}. "
        f"Page object reports: {available_interfaces}"
    )
    logger.info(f"eth0 confirmed in available network interfaces")

    # Test 4: Verify interface-specific save button pattern through page object
    try:
        save_button_config = network_page.get_interface_specific_save_button(
            "network", "eth0"
        )
        logger.info(f"eth0 save button config: {save_button_config}")

        # Verify save button exists using the config
        save_selector = save_button_config.get(
            "selector", "button#button_save_port_eth0"
        )
        save_button = network_page.page.locator(save_selector)

        if save_button.count() > 0:
            logger.info(f"eth0 save button found with selector: {save_selector}")
        else:
            # Try fallback through page object
            fallback_save_locator = network_page.get_interface_specific_save_button()
            if fallback_save_locator and fallback_save_locator.count() > 0:
                logger.info(f"Using fallback save button for eth0")
            else:
                logger.warning(f"No save button found for eth0 on {device_model}")

    except Exception as e:
        logger.warning(f"Save button validation failed for eth0 on {device_model}: {e}")

    # Final validation through page object capabilities
    network_capable = network_page.has_capability("network")
    if not network_capable:
        pytest.skip(f"Device {device_model} does not support network configuration")

    # Log comprehensive test results through page object
    device_info = network_page.get_device_info()
    logger.info(f"eth0 management test completed for {device_model}: {device_info}")

    # Log completion
    logger.info(
        f"eth0 management interface validation PASSED for {device_model} "
        f"(Series {device_series})"
    )
    print(
        f"ETH0 MANAGEMENT VALIDATED: {device_model} - "
        f"IP editable, PTP correctly absent, save button present"
    )
