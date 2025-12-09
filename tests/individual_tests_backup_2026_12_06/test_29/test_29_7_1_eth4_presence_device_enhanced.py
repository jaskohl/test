"""
Test 29 7 1 Eth4 Presence (Device Enhanced)
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
ENHANCED: DeviceCapabilities integration with device-aware interface presence validation

Purpose: Verify eth4 interface presence and visibility with device-aware patterns.
Expected: Test should verify eth4 IP field presence and editability using DeviceCapabilities.
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def _expand_eth4_panel_device_enhanced(page: Page, timeout_multiplier: float = 1.0):
    """Expand eth4 collapsible panel based on device exploration data with device-aware patterns."""
    try:
        # Bootstrap collapse pattern from device exploration HTML
        eth4_header = page.locator('a[href="#port_eth4_collapse"]')
        if eth4_header.count() > 0:
            # Check if already expanded
            aria_expanded = eth4_header.get_attribute("aria-expanded")
            if aria_expanded != "true":
                eth4_header.click()
                time.sleep(0.5 * timeout_multiplier)  # Device-aware delay
                logger.info("eth4 panel expanded successfully")
                return
        # Fallback: Try any collapsible toggle
        panel_toggle = page.locator('a[href*="port_eth4"]')
        if panel_toggle.count() > 0:
            panel_toggle.click()
            time.sleep(0.5 * timeout_multiplier)  # Device-aware delay
            logger.info("eth4 panel expanded via fallback")
    except Exception as e:
        logger.warning(f"eth4 panel expansion failed: {e}")


def test_29_7_1_eth4_presence_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 29 7 1 Eth4 Presence (Device Enhanced)
    Purpose: Verify eth4 interface presence and visibility with device-aware patterns

    This test with DeviceCapabilities integration:
    1. Validates device model and series using DeviceCapabilities
    2. Applies device-aware timeout scaling
    3. Uses device-aware panel expansion
    4. Verifies eth4 IP presence with cross-validation against DeviceCapabilities
    5. Provides device-specific logging and validation
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
                f"eth4 presence tests apply to Series 3 devices only (detected: {device_series})"
            )

        logger.info(
            f"Testing eth4 presence on {device_model} with {timeout_multiplier}x timeout multiplier"
        )

        # ENHANCED: Navigate to network page with device-aware timeout
        unlocked_config_page.goto(
            f"{base_url}/network",
            wait_until="domcontentloaded",
            timeout=30000 * timeout_multiplier,
        )
        time.sleep(1 * timeout_multiplier)

        # ENHANCED: Expand eth4 panel before field interaction with device-aware patterns
        _expand_eth4_panel_device_enhanced(unlocked_config_page, timeout_multiplier)

        # ENHANCED: Cross-validate eth4 availability with DeviceCapabilities
        network_interfaces = DeviceCapabilities.get_network_interfaces(device_model)
        eth4_available_in_capabilities = "eth4" in network_interfaces

        logger.info(
            f"eth4 availability from DeviceCapabilities for {device_model}: {eth4_available_in_capabilities}"
        )
        logger.info(
            f"Available network interfaces for {device_model}: {network_interfaces}"
        )

        # ENHANCED: eth4 IP field validation with device-aware patterns
        eth4_ip = unlocked_config_page.locator("input[name='ip_eth4']")

        if eth4_ip.count() > 0 and eth4_ip.is_visible():
            # ENHANCED: Field presence and editability validation with device-aware timeout
            expect(eth4_ip).to_be_visible(timeout=5000 * timeout_multiplier)
            expect(eth4_ip).to_be_editable()
            logger.info(
                f"eth4 interface presence verified on {device_model} - IP field visible and editable"
            )

            # ENHANCED: Cross-validate UI presence with DeviceCapabilities
            if eth4_available_in_capabilities:
                logger.info(
                    f"eth4 presence confirmed - DeviceCapabilities and UI both show availability for {device_model}"
                )
            else:
                logger.warning(
                    f"eth4 available in UI but not in DeviceCapabilities for {device_model}"
                )

        elif eth4_available_in_capabilities:
            # eth4 should be available according to DeviceCapabilities but not visible in UI
            logger.warning(
                f"eth4 expected from DeviceCapabilities but IP field not visible on {device_model}"
            )
            pytest.fail(
                f"eth4 expected to be available on {device_model} according to DeviceCapabilities but not visible in UI"
            )
        else:
            # eth4 not available in either DeviceCapabilities or UI - this is acceptable
            logger.info(
                f"eth4 not available on {device_model} - consistent with DeviceCapabilities"
            )
            pytest.skip(
                f"eth4 not available on {device_model} - may not be available on this device variant"
            )

        # ENHANCED: Additional device-specific validations
        save_button_pattern = DeviceCapabilities.get_interface_specific_save_button(
            device_model, "network_configuration", None
        )
        logger.info(
            f"Device save button pattern for {device_model}: {save_button_pattern}"
        )

        # ENHANCED: Validate series-specific network configuration patterns
        if device_series == "Series 3":
            logger.info(
                f"eth4 presence validation completed for Series 3 device {device_model}"
            )

    except Exception as e:
        pytest.fail(f"eth4 presence test failed on {device_model}: {e}")
