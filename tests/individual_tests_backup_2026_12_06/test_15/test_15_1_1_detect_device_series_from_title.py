"""
Test 15.1.1: Detect Device Series from Page Title - DeviceCapabilities Enhanced
Category: 15 - Device Capability Detection Tests
Test Count: 1 of 15 in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Both Series 2 and 3
ENHANCED: Comprehensive DeviceCapabilities integration for cross-validation of detected capabilities
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_15_1_1_detect_device_series_from_title_device_enhanced(
    unlocked_config_page: Page, request
):
    """
    Test 15.1.1: Detect Device Series from Page Title - DeviceCapabilities Enhanced
    Purpose: Determine device series from page title and cross-validate with device database
    Expected: Title indicates correct series that matches device database
    ENHANCED: Cross-validation with DeviceCapabilities database for accuracy
    Series: Both - validates detection accuracy
    """
    # Get device model for database cross-validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot cross-validate series detection"
        )

    # Get expected series from device database
    expected_series = DeviceCapabilities.get_series(device_model)
    if expected_series == 0:
        pytest.fail(
            f"Unknown device model {device_model} - not in DeviceCapabilities database"
        )

    # Extract series from page title (the detection method being tested)
    title = unlocked_config_page.title()

    logger.info(f"Testing series detection on {device_model}")
    logger.info(f"Page title: {title}")
    logger.info(f"Expected series from database: {expected_series}")

    # Validate title contains expected Kronos branding
    assert "Kronos" in title, f"Title should contain 'Kronos', got: {title}"
    assert "Series" in title, f"Title should contain 'Series', got: {title}"

    # Extract detected series from title
    is_series2 = "Series 2" in title
    is_series3 = "Series 3" in title

    assert (
        is_series2 or is_series3
    ), f"Title should indicate Series 2 or 3, got: {title}"

    # Cross-validate detected series with device database
    detected_series = 2 if is_series2 else 3

    logger.info(f"Detected series from title: {detected_series}")
    logger.info(f"Expected series from database: {expected_series}")

    # CRITICAL VALIDATION: Title detection should match database
    assert (
        detected_series == expected_series
    ), f"Series detection mismatch - title shows Series {detected_series}, but device database shows Series {expected_series} for {device_model}"

    # Log successful validation
    if is_series2:
        logger.info(
            f" Series detection VALIDATED: Kronos Series 2 detected and confirmed for {device_model}"
        )
        print(f"DETECTED & VALIDATED: Kronos Series 2 ({device_model})")
    else:
        logger.info(
            f" Series detection VALIDATED: Kronos Series 3 detected and confirmed for {device_model}"
        )
        print(f"DETECTED & VALIDATED: Kronos Series 3 ({device_model})")

    # Additional device information validation
    device_info = DeviceCapabilities.get_device_info(device_model)
    logger.info(f"Device information: {device_info}")

    # Validate device info contains expected fields
    assert "hardware_model" in device_info, f"Device info should contain hardware_model"
    assert "series" in device_info, f"Device info should contain series"
    assert (
        device_info["series"] == expected_series
    ), f"Device info series should match expected"

    # Test capability detection implications
    capabilities = DeviceCapabilities.get_capabilities(device_model)
    logger.info(f"Device capabilities: {capabilities}")

    if expected_series == 2:
        # Series 2 validation
        assert (
            capabilities.get("ptp_supported") == False
        ), "Series 2 should not support PTP"
        assert (
            capabilities.get("network_interfaces") == 1
        ), "Series 2 should have 1 network interface"

        network_interfaces = DeviceCapabilities.get_network_interfaces(device_model)
        assert "eth0" in network_interfaces, "Series 2 should have eth0 interface"
        assert len(network_interfaces) == 1, "Series 2 should only have eth0 interface"

        logger.info(
            f" Series 2 capabilities validated for {device_model}: No PTP, 1 interface (eth0)"
        )

    elif expected_series == 3:
        # Series 3 validation
        assert capabilities.get("ptp_supported") == True, "Series 3 should support PTP"
        assert (
            capabilities.get("network_interfaces") >= 4
        ), "Series 3 should have 4+ network interfaces"

        network_interfaces = DeviceCapabilities.get_network_interfaces(device_model)
        ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)

        assert (
            "eth0" in network_interfaces
        ), "Series 3 should have eth0 management interface"
        assert (
            len(ptp_interfaces) >= 3
        ), f"Series 3 should have 3+ PTP interfaces, found {len(ptp_interfaces)}"

        logger.info(
            f" Series 3 capabilities validated for {device_model}: PTP supported, {len(network_interfaces)} interfaces, {len(ptp_interfaces)} PTP interfaces"
        )

    logger.info(f"Series detection test completed successfully for {device_model}")
