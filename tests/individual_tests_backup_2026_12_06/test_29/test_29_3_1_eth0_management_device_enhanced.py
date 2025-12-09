"""
Test 29 3 1 Eth0 Management Interface Testing (Device Enhanced)
Category: 29 - Network Configuration Series 3
Extracted from: tests/grouped/test_29_network_config_series3.py
Source Class: TestEth0Management
Individual test file for better test isolation and debugging.
ENHANCED: DeviceCapabilities integration with device-aware validation patterns

Purpose: Test eth0 management interface properties and PTP absence verification with device-aware patterns.
Expected: Test should verify eth0 IP visibility, editability, and confirm PTP is not available.
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def _expand_eth0_panel_device_enhanced(page: Page, timeout_multiplier: float = 1.0):
    """Expand eth0 collapsible panel based on device exploration data with device-aware patterns."""
    try:
        # Bootstrap collapse pattern from device exploration HTML
        eth0_header = page.locator('a[href="#port_eth0_collapse"]')
        if eth0_header.count() > 0:
            # Check if already expanded
            aria_expanded = eth0_header.get_attribute("aria-expanded")
            if aria_expanded != "true":
                eth0_header.click()
                time.sleep(0.5 * timeout_multiplier)  # Device-aware delay
                logger.info("eth0 panel expanded successfully")
                return
        # Fallback: Try any collapsible toggle
        panel_toggle = page.locator('a[href*="port_eth0"]')
        if panel_toggle.count() > 0:
            panel_toggle.click()
            time.sleep(0.5 * timeout_multiplier)  # Device-aware delay
            logger.info("eth0 panel expanded via fallback")
    except Exception as e:
        logger.warning(f"eth0 panel expansion failed: {e}")


def test_29_3_1_eth0_management_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 29 3 1 Eth0 Management Interface Testing (Device Enhanced)

    Purpose: Test eth0 management interface properties and PTP absence verification with device-aware patterns.

    This test with DeviceCapabilities integration:
    1. Validates device model and series using DeviceCapabilities
    2. Applies device-aware timeout scaling
    3. Uses device-aware panel expansion
    4. Verifies eth0 IP visibility and editability with device validation
    5. Confirms PTP is not available on eth0 (management interface)
    6. Cross-validates with DeviceCapabilities network interface data
    """
    # ENHANCED: Use request.session.device_hardware_model for device detection
    device_model = request.session.device_hardware_model
    if device_model == "Unknown":
        pytest.fail("Device model not detected - cannot determine network capabilities")

    device_series = DeviceCapabilities.get_series(device_model)

    # ENHANCED: Apply timeout multiplier for device-aware testing
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    try:
        # ENHANCED: Series validation using DeviceCapabilities
        if device_series != "Series 3":
            pytest.skip(
                f"eth0 management tests apply to Series 3 devices only (detected: {device_series})"
            )

        logger.info(
            f"Testing eth0 management interface on {device_model} with {timeout_multiplier}x timeout multiplier"
        )

        # ENHANCED: Navigate to network page with device-aware timeout
        unlocked_config_page.goto(
            f"{base_url}/network",
            wait_until="domcontentloaded",
            timeout=30000 * timeout_multiplier,
        )
        time.sleep(1 * timeout_multiplier)

        # ENHANCED: Expand eth0 panel before field interaction with device-aware patterns
        _expand_eth0_panel_device_enhanced(unlocked_config_page, timeout_multiplier)

        # ENHANCED: eth0 IP field validation with device-aware patterns
        eth0_ip = unlocked_config_page.locator("input[name='ip_eth0']")
        if eth0_ip.count() > 0:
            # ENHANCED: Field visibility and editability validation with device-aware timeout
            expect(eth0_ip).to_be_visible(timeout=5000 * timeout_multiplier)
            expect(eth0_ip).to_be_editable()
            logger.info(f"eth0 IP field found and editable on {device_model}")
        else:
            pytest.fail(f"eth0 IP field not found on {device_model}")

        # ENHANCED: eth0 is management interface - PTP should NOT be available (device-aware validation)
        ptp_field = unlocked_config_page.locator("input[name='ptp_enable_eth0']")
        if ptp_field.count() > 0:
            assert (
                not ptp_field.is_visible()
            ), f"PTP should not be available on eth0 management interface for {device_model}"
            logger.info(
                f"PTP correctly not available on eth0 management interface for {device_model}"
            )

        # ENHANCED: Cross-validate with DeviceCapabilities network interface data
        network_interfaces = DeviceCapabilities.get_network_interfaces(device_model)
        if "eth0" in network_interfaces:
            logger.info(
                f"eth0 confirmed in available network interfaces for {device_model}: {network_interfaces}"
            )
        else:
            logger.warning(
                f"eth0 not found in DeviceCapabilities network interfaces for {device_model}"
            )

        # ENHANCED: Validate device series-specific network configuration patterns
        if device_series == "Series 3":
            assert (
                eth0_ip.count() > 0
            ), f"Series 3 device {device_model} should have eth0 management interface"
            logger.info(
                f"eth0 management interface validation passed for Series 3 device {device_model}"
            )

        # ENHANCED: Additional device-specific validations
        save_button_pattern = DeviceCapabilities.get_interface_specific_save_button(
            device_model, "network_configuration", None
        )
        logger.info(
            f"Device save button pattern for {device_model}: {save_button_pattern}"
        )

    except Exception as e:
        pytest.fail(f"eth0 management interface test failed on {device_model}: {e}")
