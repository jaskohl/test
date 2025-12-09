"""
Test 15.4.1: Series 2 Network Modes Available - Pure Page Object Pattern
Category: 15 - Device Capability Detection Tests
Test Count: Part of 12 tests in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Series 2 Only
IMPROVED: Pure page object architecture with device-aware Series 2 network mode validation
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.network_config_page import NetworkConfigPage


def test_15_4_1_series2_network_modes(unlocked_config_page: Page, request):
    """
    Test 15.4.1: Series 2 Network Modes Available (Pure Page Object Pattern)
    Purpose: Verify Series 2 has expected network modes using pure page object architecture
    Expected: Network modes validated against DeviceCapabilities database for Series 2
    Series: Series 2 Only
    IMPROVED: Pure page object pattern with device-aware Series 2 network mode validation
    """
    # Use DeviceCapabilities for accurate series detection
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate Series 2 network modes"
        )

    logger = logging.getLogger(__name__)

    try:
        # Initialize network configuration page object
        network_page = NetworkConfigPage(unlocked_config_page, device_model)

        logger.info(f"{device_model}: Starting Series 2 network mode validation")

        device_series_num = network_page.get_expected_device_series()
        if device_series_num != 2:
            pytest.skip(
                f"Series 2 network mode validation only applies to Series 2, detected: {device_series_num}"
            )

        # Get device-aware timeout using page object method
        timeout_multiplier = network_page.get_timeout_multiplier()

        logger.info(
            f"{device_model}: Series {device_series_num} network mode validation"
        )
        logger.info(
            f"{device_model}: Applying timeout multiplier: {timeout_multiplier}x"
        )

        # Navigate to network page using page object method
        network_page.navigate_to_page()

        # Validate page loaded successfully using page object method
        network_page.wait_for_page_load()

        logger.info(f"{device_model}: Network configuration page loaded successfully")

        # Apply device-aware timeout using page object method
        base_timeout = 2000
        device_timeout = network_page.calculate_timeout(base_timeout)

        # Validate network mode selector using page object method
        network_page.validate_network_mode_selector_visibility(device_timeout)

        # Get network mode options using page object method
        network_modes_result = network_page.get_network_mode_options(device_timeout)
        option_count = network_modes_result["option_count"]
        found_modes = network_modes_result["found_modes"]

        logger.info(f"{device_model}: Total network mode options found: {option_count}")

        # Cross-validate with DeviceCapabilities database using page object method
        expected_modes = network_page.get_expected_series2_network_modes()

        # Validate expected modes presence using page object validation
        validation_result = network_page.validate_expected_network_modes_present(
            expected_modes, found_modes
        )

        found_modes = validation_result["found_modes"]
        missing_modes = validation_result["missing_modes"]

        # Log mode detection results
        for mode in found_modes:
            logger.info(f"{device_model}: Found network mode: {mode}")
        for mode in missing_modes:
            logger.warning(f"{device_model}: Missing network mode: {mode}")

        # Validate against DeviceCapabilities expectations using page object validation
        network_page.validate_series2_network_mode_completeness(
            found_modes, expected_modes
        )

        # Additional validation for Series 2 specific requirements using page object validation
        network_page.validate_series2_exact_mode_count(option_count)

        # Store network mode information for subsequent tests using page object method
        network_page.store_series2_network_modes_in_session(request, found_modes)

        # Log detailed validation results
        logger.info(f"{device_model}: Series 2 network mode validation complete:")
        logger.info(f"{device_model}: - Device: {device_model}")
        logger.info(f"{device_model}: - Total modes: {len(found_modes)}")
        logger.info(f"{device_model}: - Modes: {', '.join(found_modes)}")
        if missing_modes:
            logger.info(f"{device_model}: - Missing modes: {', '.join(missing_modes)}")

        # Cross-validation test using page object method
        network_page.test_series2_network_mode_cross_validation()

        logger.info(f"{device_model}: Successfully validated Series 2 network modes")
        print(f"Series 2 network mode validation completed for {device_model}")

    except Exception as e:
        logger.error(
            f"{device_model}: Series 2 network mode validation encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"Series 2 network mode validation failed for {device_model}: {e}")
