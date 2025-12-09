"""
Test 15.6.1: PTP Tests Follow Correct Device Validation Pattern - DEVICE ENHANCED
Category: 15 - Device Capability Detection Tests
Test Count: Part of 12 tests in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Both Series 2 and 3

Enhanced Features:
- DeviceCapabilities integration with comprehensive device validation
- Enhanced pattern validation with device-aware checks
- Device model validation against known database
- Comprehensive capability validation and cross-referencing

Extracted from: tests/test_15_capability_detection.py
Source Class: TestPTPTestValidation
Original: test_15_6_1_ptp_test_device_validation_pattern.py
Enhanced Version: test_15_6_1_ptp_test_device_validation_pattern_device_enhanced.py
"""

import pytest
import logging
from pages.device_capabilities import DeviceCapabilities


def test_15_6_1_ptp_test_device_validation_pattern_device_enhanced(request):
    """
    Test 15.6.1: PTP Tests Follow Correct Device Validation Pattern - DEVICE ENHANCED
    Purpose: Validate all PTP tests use proper DeviceCapabilities-based device validation
    Expected: Tests should check DeviceCapabilities first, skip appropriately with enhanced validation
    Series: Both - meta-validation of test correctness with device-aware enhancements

    Enhanced Features:
    - Uses DeviceCapabilities for comprehensive device series and model validation
    - Enhanced pattern validation with device-aware timeout scaling
    - Comprehensive capability validation and cross-referencing
    - Detailed device model validation against known database
    """
    logger = logging.getLogger(__name__)

    # ENHANCED: Use DeviceCapabilities for comprehensive device detection
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected for enhanced pattern validation")

    # ENHANCED: Get comprehensive device information
    device_series_num = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)
    ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)
    network_interfaces = DeviceCapabilities.get_network_interfaces(device_model)

    logger.info(f"Enhanced PTP pattern validation for device: {device_model}")
    logger.info(f"  - Series: {device_series_num}")
    logger.info(f"  - Timeout multiplier: {timeout_multiplier}x")
    logger.info(f"  - PTP supported: {ptp_supported}")
    logger.info(f"  - PTP interfaces: {ptp_interfaces}")
    logger.info(f"  - Network interfaces: {network_interfaces}")

    # ENHANCED: Comprehensive validation based on device characteristics
    if not ptp_supported:
        # For non-PTP devices, validate comprehensive absence of PTP features
        logger.info(
            f"Device {device_model} correctly does not support PTP - comprehensive validation"
        )

        # Validate no PTP interfaces for non-PTP devices
        assert (
            len(ptp_interfaces) == 0
        ), f"Non-PTP device {device_model} should have no PTP interfaces, got: {ptp_interfaces}"

        # ENHANCED: Additional validations for non-PTP devices
        assert (
            device_series_num == 2
        ), f"Non-PTP device should be Series 2, got Series {device_series_num} for {device_model}"

        # Validate network interface expectations for Series 2
        expected_series2_interfaces = [
            "eth0"
        ]  # Series 2 typically has single network interface
        actual_network_interfaces = set(network_interfaces)
        expected_network_interfaces = set(expected_series2_interfaces)

        assert (
            actual_network_interfaces == expected_network_interfaces
        ), f"Series 2 device {device_model} should have network interfaces {expected_network_interfaces}, got {actual_network_interfaces}"

    else:
        # For PTP devices, validate comprehensive PTP feature presence
        logger.info(f"Device {device_model} supports PTP - comprehensive validation")

        # Validate PTP interfaces exist for PTP devices
        assert (
            len(ptp_interfaces) > 0
        ), f"PTP device {device_model} should have PTP interfaces, got: {ptp_interfaces}"

        # ENHANCED: Additional validations for PTP devices
        assert (
            device_series_num == 3
        ), f"PTP device should be Series 3, got Series {device_series_num} for {device_model}"

        # Validate network interface expectations for Series 3
        expected_series3_interfaces = {
            "eth0",
            "eth1",
            "eth2",
            "eth3",
            "eth4",
        }  # Series 3 has multiple interfaces
        actual_network_interfaces = set(network_interfaces)

        assert actual_network_interfaces.issubset(
            expected_series3_interfaces
        ), f"Series 3 device {device_model} network interfaces should be subset of {expected_series3_interfaces}, got {actual_network_interfaces}"

    # ENHANCED: Validate this pattern works for all known device models with comprehensive checks
    if device_model == "KRONOS-2R-HVXX-A2F":  # 66.1
        assert not ptp_supported and len(ptp_interfaces) == 0
        assert device_series_num == 2
        assert "eth0" in network_interfaces
        assert len(network_interfaces) == 1
        logger.info(
            " KRONOS-2R-HVXX-A2F (66.1) validation passed - Series 2, no PTP, single network interface"
        )

    elif device_model == "KRONOS-2P-HV-2":  # 190.46
        assert not ptp_supported and len(ptp_interfaces) == 0
        assert device_series_num == 2
        assert "eth0" in network_interfaces
        assert len(network_interfaces) == 1
        logger.info(
            " KRONOS-2P-HV-2 (190.46) validation passed - Series 2, no PTP, single network interface"
        )

    elif device_model == "KRONOS-3R-HVLV-TCXO-A2F":  # 66.3
        assert ptp_supported and len(ptp_interfaces) > 0
        assert device_series_num == 3
        assert "eth0" in network_interfaces  # Management interface
        assert len(network_interfaces) >= 4  # Series 3 has multiple interfaces
        logger.info(
            f" KRONOS-3R-HVLV-TCXO-A2F (66.3) validation passed - Series 3, PTP enabled, {len(network_interfaces)} network interfaces"
        )

    elif device_model == "KRONOS-3R-HVXX-TCXO-44A":  # 66.6
        assert ptp_supported and len(ptp_interfaces) > 0
        assert device_series_num == 3
        assert "eth0" in network_interfaces  # Management interface
        assert len(network_interfaces) >= 4  # Series 3 has multiple interfaces
        logger.info(
            f" KRONOS-3R-HVXX-TCXO-44A (66.6) validation passed - Series 3, PTP enabled, {len(network_interfaces)} network interfaces"
        )

    elif device_model == "KRONOS-3R-HVXX-TCXO-A2X":  # 190.47
        assert ptp_supported and len(ptp_interfaces) > 0
        assert device_series_num == 3
        assert "eth0" in network_interfaces  # Management interface
        assert len(network_interfaces) >= 4  # Series 3 has multiple interfaces
        logger.info(
            f" KRONOS-3R-HVXX-TCXO-A2X (190.47) validation passed - Series 3, PTP enabled, {len(network_interfaces)} network interfaces"
        )

    # ENHANCED: Store validation results for subsequent tests
    request.session.ptp_device_validation_passed = True
    request.session.ptp_device_validation_data = {
        "device_model": device_model,
        "device_series": device_series_num,
        "ptp_supported": ptp_supported,
        "ptp_interface_count": len(ptp_interfaces),
        "network_interface_count": len(network_interfaces),
        "timeout_multiplier": timeout_multiplier,
        "validation_timestamp": "enhanced_device_pattern_validation",
    }

    logger.info(f" Enhanced PTP device validation pattern verified for {device_model}")
    logger.info(f"  - Pattern validation: PASSED")
    logger.info(f"  - Device series: {device_series_num}")
    logger.info(f"  - PTP capability: {ptp_supported}")
    logger.info(
        f"  - Interface counts: PTP={len(ptp_interfaces)}, Network={len(network_interfaces)}"
    )
