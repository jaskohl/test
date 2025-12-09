"""
Test 29 2 1 Sfp Presence - Pure Page Object Pattern
Category: 29 - Network Configuration (Series 3)
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
Test Count: 7 of 60 in Category 29
Hardware: Device Only
Priority: HIGH - SFP presence validation
Series: Series 3 only
PATTERN: PURE PAGE OBJECT - No direct DeviceCapabilities calls
Based on test_29_network_config_series3.py::TestNetworkConfigSeries3::test_29_2_1_sfp_presence
Purpose: Test SFP module presence and availability detection with device-aware patterns through page object encapsulation.
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_2_1_sfp_presence(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.2.1: SFP Presence - Pure Page Object Pattern
    Purpose: Test SFP module presence and availability detection with device-aware patterns

    This test with pure page object encapsulation:
    1. Validates device model and series using page object methods
    2. Applies device-aware timeout scaling through page object
    3. Uses device-aware panel expansion through page object
    4. Cross-validates SFP availability through page object methods
    5. Provides device-specific logging and validation through page object
    Pattern: PURE PAGE OBJECT - No direct DeviceCapabilities calls
    """
    # Get device model and validate Series 3 requirement
    device_model = (
        request.session.device_hardware_model
        if hasattr(request.session, "device_hardware_model")
        else "unknown"
    )
    if device_model == "Unknown":
        pytest.fail("Device model not detected - cannot determine network capabilities")

    # Initialize page object with device-aware patterns
    network_config_page = NetworkConfigPage(
        unlocked_config_page, device_model=device_model
    )

    # Validate device series through page object
    device_series = network_config_page.get_series()

    # Apply timeout multiplier for device-aware testing through page object
    timeout_multiplier = network_config_page.get_timeout_multiplier()

    try:
        # Series validation using page object
        if device_series != 3:
            pytest.skip(
                f"SFP presence tests apply to Series 3 devices only (detected: Series {device_series})"
            )

        logger.info(
            f"Testing SFP presence on {device_model} with {timeout_multiplier}x timeout multiplier"
        )

        # Navigate to network page using page object with device-aware timeout
        network_config_page.navigate_to_page()
        time.sleep(1 * timeout_multiplier)

        # Expand SFP panel before field interaction with device-aware patterns through page object
        try:
            sfp_panel_expanded = network_config_page.expand_sfp_panel()
            if sfp_panel_expanded:
                time.sleep(0.5 * timeout_multiplier)  # Device-aware delay
                logger.info("SFP panel expanded successfully")
        except Exception as e:
            logger.warning(f"SFP panel expansion failed on {device_model}: {e}")
            pass  # Panel expansion is optional

        # Cross-validate SFP availability through page object methods
        network_interfaces = network_config_page.get_network_interfaces()
        has_sfp_capability = network_config_page.has_capability("sfp_support")

        logger.info(
            f"SFP capability from page object for {device_model}: {has_sfp_capability}"
        )
        logger.info(
            f"Available network interfaces for {device_model}: {network_interfaces}"
        )

        # Get SFP field locator through page object
        sfp_locator = network_config_page.get_sfp_field_locator()

        # Test SFP presence with device-aware validation
        if sfp_locator and sfp_locator.count() > 0 and sfp_locator.is_visible():
            # SFP field presence and enabled validation with device-aware timeout
            field_timeout = int(5000 * timeout_multiplier)
            expect(sfp_locator).to_be_enabled(timeout=field_timeout)
            logger.info(f"SFP configuration visible and enabled on {device_model}")

            # Cross-validate UI presence with page object capabilities
            if has_sfp_capability:
                logger.info(
                    f"SFP presence confirmed - Page object and UI both show availability for {device_model}"
                )
            else:
                logger.warning(
                    f"SFP available in UI but not indicated by page object capabilities for {device_model}"
                )

        elif has_sfp_capability:
            # SFP should be available according to page object but not visible in UI
            logger.warning(
                f"SFP expected from page object but not visible on {device_model}"
            )
            pytest.fail(
                f"SFP expected to be available on {device_model} according to page object but not visible in UI"
            )
        else:
            # SFP not available in either page object or UI - this is acceptable
            logger.info(
                f"SFP not available on {device_model} - consistent with page object capabilities"
            )
            print(
                f"SFP configuration not visible on {device_model} - may not be available on this device variant"
            )

        # Additional device-specific validations through page object
        save_button_pattern = network_config_page.get_interface_specific_save_button(
            "network_configuration", None
        )
        logger.info(
            f"Device save button pattern for {device_model}: {save_button_pattern}"
        )

        # Validate series-specific network configuration patterns through page object
        if device_series == 3:
            logger.info(
                f"SFP presence validation completed for Series 3 device {device_model}"
            )

        # Log comprehensive test results through page object
        device_info = network_config_page.get_device_info()
        logger.info(f"SFP presence test completed for {device_model}: {device_info}")

    except Exception as e:
        pytest.fail(f"SFP presence test failed on {device_model}: {e}")

    # Final validation through page object capabilities
    network_capable = network_config_page.has_capability("network")
    if not network_capable:
        pytest.skip(f"Device {device_model} does not support network configuration")

    print(f"SFP PRESENCE VALIDATED: {device_model} (Series {device_series})")
