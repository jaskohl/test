"""
Test 15.6.2: PTP Tests Use Static Interface Validation Pattern - DEVICE ENHANCED
Category: 15 - Device Capability Detection Tests
Test Count: Part of 12 tests in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Both Series 2 and 3

Enhanced Features:
- DeviceCapabilities integration with comprehensive interface validation
- Enhanced interface validation with device-aware timeout scaling
- Comprehensive interface naming and format validation
- Cross-validation of interface consistency and device-specific expectations

Extracted from: tests/test_15_capability_detection.py
Source Class: TestPTPTestValidation
Original: test_15_6_2_ptp_test_interface_validation_pattern.py
Enhanced Version: test_15_6_2_ptp_test_interface_validation_pattern_device_enhanced.py
"""

import pytest
import logging
import re
from playwright.sync_api import Page
from pages.device_capabilities import DeviceCapabilities


def test_15_6_2_ptp_test_interface_validation_pattern_device_enhanced(
    unlocked_config_page: Page, request
):
    """
    Test 15.6.2: PTP Tests Use Static Interface Validation Pattern - DEVICE ENHANCED
    Purpose: Validate PTP tests check static interface definitions correctly with device-aware validation
    Expected: Interface validation uses DeviceCapabilities exclusively with enhanced validation
    Series: Both - validates interface enumeration correctness with device-specific optimization

    Enhanced Features:
    - Uses DeviceCapabilities for comprehensive device interface validation
    - Enhanced interface validation with device-aware timeout scaling
    - Comprehensive interface naming, format, and consistency validation
    - Cross-validation of interface expectations against device series and model
    """
    logger = logging.getLogger(__name__)

    # ENHANCED: Use DeviceCapabilities for comprehensive device detection
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected for enhanced interface validation")

    # ENHANCED: Get comprehensive device information
    device_series_num = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(f"Enhanced PTP interface validation for device: {device_model}")
    logger.info(f"  - Series: {device_series_num}")
    logger.info(f"  - Timeout multiplier: {timeout_multiplier}x")

    # ENHANCED: Apply device-aware timeout
    base_timeout = 3000
    enhanced_timeout = base_timeout * timeout_multiplier

    # CORRECT: Use DeviceCapabilities static method only for interface enumeration
    ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)

    logger.info(
        f"DeviceCapabilities PTP interfaces for {device_model}: {ptp_interfaces}"
    )

    # ENHANCED: Validate that DeviceCapabilities provides consistent interface enumeration
    assert isinstance(
        ptp_interfaces, list
    ), "PTP interfaces should be returned as a list from DeviceCapabilities"

    # ENHANCED: Comprehensive validation for each interface in the list
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

        # ENHANCED: Additional interface format validation
        assert re.match(
            r"^eth\d+$", interface
        ), f"PTP interface {interface} should match ethX pattern"

    # ENHANCED: Validate consistent interface enumeration across multiple calls
    ptp_interfaces_second_call = DeviceCapabilities.get_ptp_interfaces(device_model)
    assert (
        ptp_interfaces == ptp_interfaces_second_call
    ), "DeviceCapabilities.get_ptp_interfaces should return consistent results"

    logger.info(f"Interface consistency validation passed for {device_model}")

    # ENHANCED: Test device-specific expectations based on DeviceCapabilities database
    if device_model in ["KRONOS-2R-HVXX-A2F", "KRONOS-2P-HV-2"]:
        # Series 2 devices should have no PTP interfaces
        assert (
            len(ptp_interfaces) == 0
        ), f"Series 2 device {device_model} should have no PTP interfaces, got: {ptp_interfaces}"
        logger.info(
            f" Series 2 validation passed for {device_model}: No PTP interfaces as expected"
        )

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

        logger.info(
            f" Series 3 validation passed for {device_model}: {len(ptp_interfaces)} PTP interfaces found"
        )

    # ENHANCED: Additional network interface cross-validation
    network_interfaces = DeviceCapabilities.get_network_interfaces(device_model)
    if len(ptp_interfaces) > 0:
        # For PTP devices, validate PTP interfaces are subset of network interfaces
        ptp_interface_set = set(ptp_interfaces)
        network_interface_set = set(network_interfaces)

        assert ptp_interface_set.issubset(
            network_interface_set
        ), f"PTP interfaces {ptp_interfaces} should be subset of network interfaces {network_interfaces} for {device_model}"

        logger.info(
            f" PTP/Network interface validation passed: PTP interfaces are subset of network interfaces"
        )

    # ENHANCED: Validate interface-specific characteristics
    if device_model == "KRONOS-3R-HVLV-TCXO-A2F":  # 66.3
        expected_interfaces = ["eth1", "eth3", "eth4"]  # Based on device database
        assert set(ptp_interfaces) == set(
            expected_interfaces
        ), f"KRONOS-3R-HVLV-TCXO-A2F should have PTP interfaces {expected_interfaces}, got {ptp_interfaces}"
        logger.info(f" Device-specific validation passed for {device_model}")

    elif device_model == "KRONOS-3R-HVXX-TCXO-44A":  # 66.6
        expected_interfaces = ["eth1", "eth3", "eth4"]  # Based on device database
        assert set(ptp_interfaces) == set(
            expected_interfaces
        ), f"KRONOS-3R-HVXX-TCXO-44A should have PTP interfaces {expected_interfaces}, got {ptp_interfaces}"
        logger.info(f" Device-specific validation passed for {device_model}")

    elif device_model == "KRONOS-3R-HVXX-TCXO-A2X":  # 190.47
        expected_interfaces = ["eth1", "eth3", "eth4"]  # Based on device database
        assert set(ptp_interfaces) == set(
            expected_interfaces
        ), f"KRONOS-3R-HVXX-TCXO-A2X should have PTP interfaces {expected_interfaces}, got {ptp_interfaces}"
        logger.info(f" Device-specific validation passed for {device_model}")

    # ENHANCED: Store validation results for subsequent tests
    request.session.ptp_interface_validation_passed = True
    request.session.ptp_interface_validation_data = {
        "device_model": device_model,
        "device_series": device_series_num,
        "ptp_interfaces": ptp_interfaces,
        "network_interfaces": network_interfaces,
        "interface_count": len(ptp_interfaces),
        "validation_timestamp": "enhanced_interface_pattern_validation",
    }

    logger.info(
        f" Enhanced PTP interface validation pattern verified for {device_model}"
    )
    logger.info(f"  - Interface count: {len(ptp_interfaces)}")
    logger.info(f"  - Interfaces: {ptp_interfaces}")
    logger.info(f"  - Network interfaces: {network_interfaces}")
    logger.info(f"  - Pattern validation: PASSED")
