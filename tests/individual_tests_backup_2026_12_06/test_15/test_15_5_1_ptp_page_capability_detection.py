"""
Test 15.5.1: PTP Page Correctly Detects and Reports Capabilities
Category: 15 - Device Capability Detection Tests
Test Count: Part of 12 tests in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Both Series 2 and 3

Extracted from: tests/test_15_capability_detection.py
Source Class: TestPTPPageValidation
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_15_5_1_ptp_page_capability_detection(
    unlocked_config_page: Page, device_ip: str, request
):
    """
    Test 15.5.1: PTP Page Correctly Detects and Reports Capabilities
    Purpose: Validate PTPConfigPage uses DeviceCapabilities correctly
    Expected: Page object reports capabilities matching authoritative data
    Series: Both - validates page object correctness
    """
    logger = logging.getLogger(__name__)
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected")

    logger.info(f"Testing PTP capability detection for {device_model} at {device_ip}")

    # Initialize page object
    ptp_page = PTPConfigPage(
        unlocked_config_page, device_ip=device_ip, device_model=device_model
    )

    # Get expected capabilities from authoritative source
    expected_ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)
    expected_ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)

    logger.info(
        f"Expected: PTP supported={expected_ptp_supported}, interfaces={expected_ptp_interfaces}"
    )

    # Validate page object capability reporting matches authoritative data
    actual_capabilities = ptp_page.get_device_capabilities()
    logger.info(f"Page object reported: {actual_capabilities}")

    if expected_ptp_supported:
        # For PTP-supported devices, page object should report PTP supported
        assert (
            actual_capabilities.get("ptp_supported") == expected_ptp_supported
        ), f"PTP page should report PTP supported for {device_model}"
        # Validate interface reporting matches
        expected_interfaces = set(expected_ptp_interfaces)
        actual_interfaces = set(actual_capabilities.get("ptp_interfaces", []))
        assert (
            actual_interfaces == expected_interfaces
        ), f"PTP interfaces mismatch for {device_model}: expected {expected_interfaces}, got {actual_interfaces}"
    else:
        # For non-PTP devices, page object should report no PTP support
        assert not actual_capabilities.get(
            "ptp_supported", True
        ), f"PTP page should report no PTP support for {device_model}"
