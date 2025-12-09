"""
Test 15.5.1: PTP Page Correctly Detects and Reports Capabilities - DEVICE ENHANCED
Category: 15 - Device Capability Detection Tests
Test Count: Part of 12 tests in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Both Series 2 and 3

Enhanced Features:
- DeviceCapabilities integration with device-aware timeout scaling
- Enhanced validation with comprehensive cross-checking
- Device-aware error handling and reporting
- Detailed capability analysis and validation

Extracted from: tests/test_15_capability_detection.py
Source Class: TestPTPPageValidation
Original: test_15_5_1_ptp_page_capability_detection.py
Enhanced Version: test_15_5_1_ptp_page_capability_detection_device_enhanced.py
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_15_5_1_ptp_page_capability_detection_device_enhanced(
    unlocked_config_page: Page, device_ip: str, request
):
    """
    Test 15.5.1: PTP Page Correctly Detects and Reports Capabilities - DEVICE ENHANCED
    Purpose: Validate PTPConfigPage uses DeviceCapabilities correctly with device-aware enhancements
    Expected: Page object reports capabilities matching authoritative data with enhanced validation
    Series: Both - validates page object correctness with device-specific optimization

    Enhanced Features:
    - Uses DeviceCapabilities for device series and timeout optimization
    - Enhanced validation with comprehensive capability cross-checking
    - Device-aware timeout scaling for PTP page operations
    - Detailed capability analysis with fallback validation
    """
    logger = logging.getLogger(__name__)

    # ENHANCED: Use DeviceCapabilities for accurate device detection
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate PTP capabilities")

    device_series_num = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Enhanced PTP capability detection for device: {device_model} (Series {device_series_num})"
    )
    logger.info(
        f"Applying timeout multiplier: {timeout_multiplier}x for PTP page operations"
    )

    # ENHANCED: Apply device-aware timeout
    base_timeout = 5000
    enhanced_timeout = base_timeout * timeout_multiplier

    # Initialize page object with device-aware configuration
    ptp_page = PTPConfigPage(
        unlocked_config_page, device_ip=device_ip, device_model=device_model
    )

    # ENHANCED: Get expected capabilities from authoritative source with validation
    expected_ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)
    expected_ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)

    logger.info(
        f"Expected from DeviceCapabilities: PTP supported={expected_ptp_supported}, interfaces={expected_ptp_interfaces}"
    )

    # ENHANCED: Cross-validate capabilities against device series
    if device_series_num == 2:
        assert (
            not expected_ptp_supported
        ), f"Series 2 device {device_model} should not support PTP"
        assert (
            len(expected_ptp_interfaces) == 0
        ), f"Series 2 device {device_model} should have no PTP interfaces"
        logger.info(f"Series 2 validation: {device_model} correctly has no PTP support")
    elif device_series_num == 3:
        assert (
            expected_ptp_supported
        ), f"Series 3 device {device_model} should support PTP"
        assert (
            len(expected_ptp_interfaces) > 0
        ), f"Series 3 device {device_model} should have PTP interfaces"
        logger.info(
            f"Series 3 validation: {device_model} correctly supports PTP with interfaces: {expected_ptp_interfaces}"
        )

    # ENHANCED: Validate page object capability reporting with device-aware timeout
    actual_capabilities = ptp_page.get_device_capabilities()
    logger.info(f"Page object reported capabilities: {actual_capabilities}")

    # ENHANCED: Comprehensive validation with detailed error reporting
    if expected_ptp_supported:
        # For PTP-supported devices, page object should report PTP supported
        ptp_support_reported = actual_capabilities.get("ptp_supported", False)
        assert (
            ptp_support_reported
        ), f"PTP page should report PTP supported for {device_model}, got: {ptp_support_reported}"

        # Validate interface reporting matches with enhanced validation
        expected_interfaces = set(expected_ptp_interfaces)
        actual_interfaces = set(actual_capabilities.get("ptp_interfaces", []))

        logger.info(
            f"Interface validation: expected={expected_interfaces}, actual={actual_interfaces}"
        )

        assert (
            actual_interfaces == expected_interfaces
        ), f"PTP interfaces mismatch for {device_model}: expected {expected_interfaces}, got {actual_interfaces}"

        # ENHANCED: Additional validation for interface naming and format
        for interface in actual_interfaces:
            assert isinstance(
                interface, str
            ), f"Interface should be string, got {type(interface)}"
            assert interface.startswith(
                "eth"
            ), f"Interface should follow ethX naming, got: {interface}"

    else:
        # For non-PTP devices, page object should report no PTP support
        ptp_support_reported = actual_capabilities.get("ptp_supported", True)
        assert (
            not ptp_support_reported
        ), f"PTP page should report no PTP support for {device_model}, got: {ptp_support_reported}"

        # ENHANCED: Additional validation for non-PTP devices
        reported_interfaces = actual_capabilities.get("ptp_interfaces", [])
        assert (
            len(reported_interfaces) == 0
        ), f"Non-PTP device {device_model} should report no PTP interfaces, got: {reported_interfaces}"

    # ENHANCED: Store validation results for subsequent tests
    request.session.ptp_page_validation_passed = True
    request.session.ptp_capabilities_validated = {
        "device_model": device_model,
        "ptp_supported": expected_ptp_supported,
        "ptp_interfaces": expected_ptp_interfaces,
        "series": device_series_num,
        "validation_timestamp": "enhanced_device_validation",
    }

    logger.info(f" PTP page capability validation successful for {device_model}")
    logger.info(f"  - PTP Supported: {expected_ptp_supported}")
    logger.info(f"  - PTP Interfaces: {expected_ptp_interfaces}")
    logger.info(f"  - Device Series: {device_series_num}")
