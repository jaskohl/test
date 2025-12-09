"""
Test 15.6.2: PTP Tests Use Static Interface Validation Pattern
Category: 15 - Device Capability Detection Tests
Test Count: Part of 12 tests in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Both Series 2 and 3

Extracted from: tests/test_15_capability_detection.py
Source Class: TestPTPTestValidation
"""

import pytest
import logging
import re
from playwright.sync_api import Page
from pages.device_capabilities import DeviceCapabilities


def test_15_6_2_ptp_test_interface_validation_pattern(
    unlocked_config_page: Page, request
):
    """
    Test 15.6.2: PTP Tests Use Static Interface Validation Pattern
    Purpose: Validate PTP tests check static interface definitions correctly
    Expected: Interface validation uses DeviceCapabilities exclusively
    Series: Both - validates interface enumeration correctness
    """
    logger = logging.getLogger(__name__)
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected for interface validation")

    # CORRECT: Use DeviceCapabilities static method only for interface enumeration
    ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)

    # Validate that DeviceCapabilities provides consistent interface enumeration
    # This should NEVER change during runtime - it's static definition
    assert isinstance(
        ptp_interfaces, list
    ), "PTP interfaces should be returned as a list from DeviceCapabilities"

    # Validate each interface in the list is a valid string
    for interface in ptp_interfaces:
        assert isinstance(
            interface, str
        ), f"Each PTP interface should be a string, got {type(interface)}: {interface}"
        assert (
            len(interface) > 0
        ), f"Each PTP interface should be non-empty, got: '{interface}'"
        # Validate interface naming convention (should be eth0, eth1, etc.)
        assert interface.startswith(
            "eth"
        ), f"PTP interface should follow ethX naming convention, got: {interface}"

    # Validate consistent interface enumeration across multiple calls
    ptp_interfaces_second_call = DeviceCapabilities.get_ptp_interfaces(device_model)
    assert (
        ptp_interfaces == ptp_interfaces_second_call
    ), "DeviceCapabilities.get_ptp_interfaces should return consistent results"

    # Log the validated interfaces for this device model
    logger.info(f" Validated PTP interfaces for {device_model}: {ptp_interfaces}")

    # Test device-specific expectations based on our device database
    if device_model in ["KRONOS-2R-HVXX-A2F", "KRONOS-2P-HV-2"]:
        # Series 2 devices should have no PTP interfaces
        assert (
            len(ptp_interfaces) == 0
        ), f"Series 2 device {device_model} should have no PTP interfaces, got: {ptp_interfaces}"
    elif device_model in [
        "KRONOS-3R-HVLV-TCXO-A2F",
        "KRONOS-3R-HVXX-TCXO-44A",
        "KRONOS-3R-HVXX-TCXO-A2X",
    ]:
        # Series 3 devices should have PTP interfaces
        assert (
            len(ptp_interfaces) > 0
        ), f"Series 3 device {device_model} should have PTP interfaces, got: {ptp_interfaces}"
        # Validate that all interfaces are valid ethernet interfaces
        for interface in ptp_interfaces:
            # Should match pattern eth0, eth1, etc.
            assert re.match(
                r"^eth\d+$", interface
            ), f"PTP interface {interface} should match ethX pattern"

    logger.info(f" Interface validation pattern verified for {device_model}")
