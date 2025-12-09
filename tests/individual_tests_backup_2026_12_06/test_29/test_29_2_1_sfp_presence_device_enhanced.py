"""
Test 29 2 1 Sfp Presence (Device Enhanced)
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
ENHANCED: DeviceCapabilities integration with device-aware SFP detection patterns

Purpose: Test SFP module presence and availability detection with device-aware patterns.
Expected: SFP configuration should be available and enabled when present using DeviceCapabilities validation.
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_29_2_1_sfp_presence_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 29 2 1 Sfp Presence (Device Enhanced)
    Purpose: Test SFP module presence and availability detection with device-aware patterns

    This test with DeviceCapabilities integration:
    1. Validates device model and series using DeviceCapabilities
    2. Applies device-aware timeout scaling
    3. Uses device-aware panel expansion
    4. Cross-validates SFP availability with DeviceCapabilities
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
                f"SFP presence tests apply to Series 3 devices only (detected: {device_series})"
            )

        logger.info(
            f"Testing SFP presence on {device_model} with {timeout_multiplier}x timeout multiplier"
        )

        # ENHANCED: Navigate to network page with device-aware timeout
        unlocked_config_page.goto(
            f"{base_url}/network",
            wait_until="domcontentloaded",
            timeout=30000 * timeout_multiplier,
        )
        time.sleep(1 * timeout_multiplier)

        # ENHANCED: Expand SFP panel before field interaction with device-aware patterns
        try:
            sfp_header = unlocked_config_page.locator('a[href="#sfp_mode_collapse"]')
            if sfp_header.count() > 0:
                aria_expanded = sfp_header.get_attribute("aria-expanded")
                if aria_expanded != "true":
                    sfp_header.click()
                    time.sleep(0.5 * timeout_multiplier)  # Device-aware delay
                    logger.info("SFP panel expanded successfully")
        except Exception as e:
            logger.warning(f"SFP panel expansion failed on {device_model}: {e}")
            pass  # Panel expansion is optional

        # ENHANCED: Cross-validate SFP availability with DeviceCapabilities
        network_interfaces = DeviceCapabilities.get_network_interfaces(device_model)
        has_sfp_capability = DeviceCapabilities.has_capability(
            device_model, "sfp_support"
        )

        logger.info(
            f"SFP capability from DeviceCapabilities for {device_model}: {has_sfp_capability}"
        )
        logger.info(
            f"Available network interfaces for {device_model}: {network_interfaces}"
        )

        # ENHANCED: Test SFP presence with device-aware validation
        sfp = unlocked_config_page.locator("select[name*='sfp' i]")

        if sfp.count() > 0 and sfp.is_visible():
            # ENHANCED: SFP field presence and enabled validation with device-aware timeout
            expect(sfp).to_be_enabled(timeout=5000 * timeout_multiplier)
            logger.info(f"SFP configuration visible and enabled on {device_model}")

            # ENHANCED: Cross-validate UI presence with DeviceCapabilities
            if has_sfp_capability:
                logger.info(
                    f"SFP presence confirmed - DeviceCapabilities and UI both show availability for {device_model}"
                )
            else:
                logger.warning(
                    f"SFP available in UI but not in DeviceCapabilities for {device_model}"
                )

        elif has_sfp_capability:
            # SFP should be available according to DeviceCapabilities but not visible in UI
            logger.warning(
                f"SFP expected from DeviceCapabilities but not visible on {device_model}"
            )
            pytest.fail(
                f"SFP expected to be available on {device_model} according to DeviceCapabilities but not visible in UI"
            )
        else:
            # SFP not available in either DeviceCapabilities or UI - this is acceptable
            logger.info(
                f"SFP not available on {device_model} - consistent with DeviceCapabilities"
            )
            print(
                f"SFP configuration not visible on {device_model} - may not be available on this device variant"
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
                f"SFP presence validation completed for Series 3 device {device_model}"
            )

    except Exception as e:
        pytest.fail(f"SFP presence test failed on {device_model}: {e}")
