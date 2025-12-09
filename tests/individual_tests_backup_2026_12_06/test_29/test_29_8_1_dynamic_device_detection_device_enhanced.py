"""
Test 29.8.1: Dynamic Device Detection - DEVICE ENHANCED
Category: 29 - Network Configuration Series 3
Extracted from: tests/grouped/test_29_network_config_series3.py
Source Class: TestDynamicDeviceDetection.test_29_8_1_dynamic_device_detection
Original: test_29_8_1_dynamic_device_detection.py
Enhanced Version: test_29_8_1_dynamic_device_detection_device_enhanced.py

Enhanced Features:
- DeviceCapabilities integration for accurate device model detection
- Cross-validation with device database network interfaces
- Device-aware timeout handling and validation
- Series 2 vs Series 3 network interface expectations

Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page
from pages.device_capabilities import DeviceCapabilities


def test_29_8_1_dynamic_device_detection_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 29.8.1: Dynamic Device Detection - DEVICE ENHANCED

    Purpose: Test that the system correctly detects available network interfaces based on device model
    Enhanced with DeviceCapabilities integration for accurate device-aware validation

    Args:
        unlocked_config_page: Playwright page object for the network configuration page
        base_url: Base URL for the application under test
        request: pytest request object for device model detection

    Enhanced Features:
    - Uses DeviceCapabilities for accurate device series and model detection
    - Validates network interface count against DeviceCapabilities expectations
    - Device-aware timeout scaling for network interface discovery
    - Cross-validation of detected interfaces with DeviceCapabilities database

    Expected:
        - Device model detection using DeviceCapabilities
        - Network interface validation based on device capabilities
        - Series-specific interface expectations (Series 2 vs Series 3)
    """
    # ENHANCED: Use DeviceCapabilities for accurate device detection
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate network interfaces")

    device_series_num = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    print(
        f"Enhanced dynamic device detection for device: {device_model} (Series {device_series_num})"
    )
    print(
        f"Applying timeout multiplier: {timeout_multiplier}x for network interface discovery"
    )

    # ENHANCED: Apply device-aware timeout
    base_timeout = 5000
    enhanced_timeout = base_timeout * timeout_multiplier

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # ENHANCED: Get expected network interfaces from DeviceCapabilities
    expected_network_interfaces = DeviceCapabilities.get_network_interfaces(
        device_model
    )
    expected_interface_count = len(expected_network_interfaces)

    print(
        f"DeviceCapabilities expects {expected_interface_count} network interfaces: {expected_network_interfaces}"
    )

    # ENHANCED: Count available forms with device-aware timeout
    forms = (
        unlocked_config_page.locator("form").count(timeout=enhanced_timeout) - 1
    )  # Subtract session modal
    print(f"Total forms detected: {forms}")

    # ENHANCED: Cross-validate form count with DeviceCapabilities expectations
    if expected_interface_count > 0:
        # For devices with known interface configuration, validate against database
        assert (
            forms == expected_interface_count
        ), f"Form count {forms} should match expected interface count {expected_interface_count} for {device_model}"
    else:
        # Fallback validation for unknown devices
        assert forms in [
            1,
            5,
            6,
            7,
        ], f"Unexpected form count {forms} for device {device_model}"

    # ENHANCED: Check available ports with device-aware validation
    available_ports = []
    missing_ports = []

    # Test all possible network interfaces
    all_possible_interfaces = ["eth0", "eth1", "eth2", "eth3", "eth4"]

    for port in all_possible_interfaces:
        port_input = unlocked_config_page.locator(f"input[name='ip_{port}']")
        if port_input.count(timeout=enhanced_timeout) > 0:
            available_ports.append(port)
            print(f" Found network interface: {port}")
        else:
            missing_ports.append(port)
            print(f" Missing network interface: {port}")

    print(f"Available ports: {available_ports}")
    print(f"Missing ports: {missing_ports}")

    # ENHANCED: Validate against DeviceCapabilities expectations
    if expected_network_interfaces:
        expected_interface_set = set(expected_network_interfaces)
        actual_interface_set = set(available_ports)

        # Check that all expected interfaces are present
        missing_expected = expected_interface_set - actual_interface_set
        assert (
            len(missing_expected) == 0
        ), f"Expected network interfaces {expected_network_interfaces} not found, missing: {missing_expected}"

        # Check for unexpected interfaces
        unexpected_interfaces = actual_interface_set - expected_interface_set
        if unexpected_interfaces:
            print(
                f"Note: Found unexpected interfaces {unexpected_interfaces} (may be acceptable)"
            )

    # ENHANCED: Series-specific validation
    if device_series_num == 2:
        # Series 2 should have single network interface (eth0)
        assert (
            "eth0" in available_ports
        ), f"Series 2 device {device_model} should have eth0 interface"
        assert (
            len(available_ports) == 1
        ), f"Series 2 device {device_model} should have exactly 1 network interface"
        print(f" Series 2 validation passed: {device_model} has single eth0 interface")

    elif device_series_num == 3:
        # Series 3 should have multiple network interfaces
        assert (
            "eth0" in available_ports
        ), f"Series 3 device {device_model} should have eth0 management interface"
        assert (
            len(available_ports) >= 4
        ), f"Series 3 device {device_model} should have at least 4 network interfaces"
        print(
            f" Series 3 validation passed: {device_model} has {len(available_ports)} network interfaces"
        )

    # ENHANCED: Validate minimum interface requirements
    assert (
        len(available_ports) >= 1
    ), f"Device {device_model} should have at least 1 network interface, found: {len(available_ports)}"

    # ENHANCED: Store interface information for subsequent tests
    request.session.network_interface_detection_passed = True
    request.session.detected_network_interfaces = available_ports
    request.session.expected_network_interfaces = expected_network_interfaces
    request.session.network_interface_count = len(available_ports)

    print(f" Enhanced dynamic device detection successful for {device_model}")
    print(f"  - Device: {device_model} (Series {device_series_num})")
    print(f"  - Expected interfaces: {expected_network_interfaces}")
    print(f"  - Detected interfaces: {available_ports}")
    print(f"  - Interface count: {len(available_ports)}")
    print(f"  - Forms detected: {forms}")
