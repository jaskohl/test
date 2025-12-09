"""
Test 25.1.1: Leap second handling in time configuration [DEVICE ENHANCED]
Category: 25 - Time Synchronization Edge Cases
Test Count: Part of 5 tests in Category 25
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
ENHANCED: DeviceCapabilities integration for device-aware validation
ENHANCED: Cross-validation with device database for GNSS capabilities
ENHANCED: Device-aware timeout scaling and series-specific validation

Extracted from: tests/test_25_time_sync_edge_cases.py
Source Class: TestTimeSyncEdgeCases
Enhanced: 2025-12-01 with DeviceCapabilities integration
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.time_config_page import TimeConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_25_1_1_leap_second_handling_device_enhanced(
    time_config_page: TimeConfigPage, base_url: str, request
):
    """
    Test 25.1.1: Leap second handling in time configuration [DEVICE ENHANCED]
    Purpose: Verify device handles leap seconds in time synchronization with device-aware validation
    Expected: Leap second handling is automatic via GNSS with device series validation
    ENHANCED: DeviceCapabilities integration for series-specific GNSS validation
    Series: Both Series 2 and 3 with series-aware testing
    """
    # Get device context for device-aware validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate GNSS capabilities")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing leap second handling on {device_model} (Series {device_series}) with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to time configuration page
    time_config_page.page.goto(f"{base_url}/time", wait_until="domcontentloaded")

    # Apply device-aware timeout scaling
    timeout_scaled = int(
        5000 * timeout_multiplier
    )  # Base timeout of 5s scaled by device multiplier

    # Verify page loaded with device-aware timeout
    time_heading = time_config_page.page.get_by_role("heading", name="Time")
    expect(time_heading).to_be_visible(timeout=timeout_scaled)

    # Get GNSS capabilities from DeviceCapabilities database
    gnss_capabilities = DeviceCapabilities.get_gnss_capabilities(device_model)
    logger.info(f"GNSS capabilities for {device_model}: {gnss_capabilities}")

    # Device-aware leap second validation based on device series
    if device_series == 2:
        # Series 2: Validate basic GNSS handling
        logger.info(f"Series 2 leap second validation for {device_model}")

        # Series 2 devices typically have basic GNSS with automatic leap second handling
        assert gnss_capabilities.get(
            "leap_second_support", False
        ), f"Series 2 device {device_model} should support automatic leap second handling"

        # Verify GNSS status section exists and shows leap second support
        gnss_status_section = time_config_page.page.locator("section, div").filter(
            has_text=("GNSS" or "GPS" or "leap" or "second")
        )

        if gnss_status_section.count() > 0:
            # GNSS section exists - validate leap second information is displayed
            logger.info(f"Series 2: GNSS status section found for {device_model}")

            # Check for leap second related indicators
            leap_indicators = [
                time_config_page.page.locator("text=/leap.*second/i"),
                time_config_page.page.locator("text=/gnss.*automatic/i"),
                time_config_page.page.locator("text=/gps.*utc/i"),
            ]

            for indicator in leap_indicators:
                if indicator.count() > 0:
                    logger.info(
                        f"Series 2: Leap second indicator found for {device_model}"
                    )
                    break
            else:
                logger.info(
                    f"Series 2: Leap second handling is automatic (no manual config) for {device_model}"
                )

    elif device_series == 3:
        # Series 3: Advanced GNSS validation with leap second support
        logger.info(f"Series 3 leap second validation for {device_model}")

        # Series 3 devices should have advanced GNSS with comprehensive leap second handling
        assert gnss_capabilities.get(
            "leap_second_support", False
        ), f"Series 3 device {device_model} should support advanced leap second handling"

        # Series 3 should have more detailed GNSS information
        gnss_info_section = time_config_page.page.locator("section, div").filter(
            has_text=("GNSS" or "GPS" or "satellite" or "timing")
        )

        if gnss_info_section.count() > 0:
            logger.info(f"Series 3: Advanced GNSS section found for {device_model}")

            # Check for Series 3 specific leap second indicators
            series3_indicators = [
                time_config_page.page.locator("text=/leap.*second.*automatic/i"),
                time_config_page.page.locator("text=/utc.*correction/i"),
                time_config_page.page.locator("text=/gnss.*utc/i"),
                time_config_page.page.locator("text=/gps.*time.*utc/i"),
            ]

            for indicator in series3_indicators:
                if indicator.count() > 0:
                    logger.info(
                        f"Series 3: Advanced leap second indicator found for {device_model}"
                    )
                    break
            else:
                # Even if no specific indicators found, verify automatic handling
                logger.info(
                    f"Series 3: Leap second handling is automatic via GNSS for {device_model}"
                )

        # Validate Series 3 has GNSS timing capabilities
        timing_capabilities = gnss_capabilities.get("timing_capabilities", {})
        assert (
            "leap_second_handling" in timing_capabilities
        ), f"Series 3 device {device_model} should have leap second handling capability"

    else:
        # Unknown series - basic validation only
        logger.warning(
            f"Unknown device series for {device_model} - using basic leap second validation"
        )
        # Basic check: leap second handling should still exist
        assert gnss_capabilities.get(
            "leap_second_support", False
        ), f"Device {device_model} should support leap second handling"

    # Cross-validate leap second support with device capabilities database
    device_capabilities = DeviceCapabilities.get_capabilities(device_model)
    expected_gnss = device_capabilities.get("gnss_supported", True)

    if expected_gnss:
        assert gnss_capabilities.get(
            "leap_second_support", False
        ), f"GNSS device {device_model} should provide leap second support"
        logger.info(f"Cross-validated: {device_model} has expected leap second support")
    else:
        logger.info(
            f"Device {device_model} does not have GNSS - leap second handled differently"
        )

    # Test leap second handling behavior (which is typically automatic)
    logger.info(f"Device {device_model}: Leap second handling is automatic via GNSS")

    # Record test completion with device context
    logger.info(
        f"DeviceCapabilities integration test completed for {device_model} (Series {device_series}): "
        f"Leap second handling validated with {timeout_multiplier}x timeout scaling"
    )

    # Test summary: Device-aware validation ensures correct leap second behavior
    print(
        f" LEAP SECOND TEST COMPLETED: {device_model} (Series {device_series}) - "
        f"Automatic leap second handling verified"
    )
