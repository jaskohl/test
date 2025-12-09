"""
Test 29.8.1 Dynamic Device Detection - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test that the system correctly detects available network interfaces based on device model.
Expected: Device model detection using page object, network interface validation based on device capabilities.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_8_1_dynamic_device_detection(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 29.8.1: Dynamic Device Detection - Pure Page Object Pattern

    Purpose: Test that the system correctly detects available network interfaces based on device model.
    """
    # Get device model from session
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate network interfaces")

    # Create page object with device_model
    network_page = NetworkConfigPage(unlocked_config_page, device_model=device_model)

    print(f"Dynamic device detection for device: {device_model}")

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    # Get expected network interfaces from page object
    expected_network_interfaces = network_page.get_network_interfaces()
    expected_interface_count = len(expected_network_interfaces)

    print(
        f"Page object expects {expected_interface_count} network interfaces: {expected_network_interfaces}"
    )

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Count available forms with device-aware timeout
    forms = (
        unlocked_config_page.locator("form").count(timeout=device_timeout) - 1
    )  # Subtract session modal
    print(f"Total forms detected: {forms}")

    # Cross-validate form count with page object expectations
    if expected_interface_count > 0:
        # For devices with known interface configuration, validate against page object
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

    # Check available ports with device-aware validation
    available_ports = []
    missing_ports = []

    # Test all possible network interfaces
    all_possible_interfaces = ["eth0", "eth1", "eth2", "eth3", "eth4"]

    for port in all_possible_interfaces:
        if network_page.has_element(f"input[name='ip_{port}']", timeout=device_timeout):
            available_ports.append(port)
            print(f"Found network interface: {port}")
        else:
            missing_ports.append(port)
            print(f"Missing network interface: {port}")

    print(f"Available ports: {available_ports}")
    print(f"Missing ports: {missing_ports}")

    # Validate against page object expectations
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

    # Series-specific validation using page object method
    device_series = network_page.get_series()
    if device_series == 2:
        # Series 2 should have single network interface (eth0)
        assert (
            "eth0" in available_ports
        ), f"Series 2 device {device_model} should have eth0 interface"
        assert (
            len(available_ports) == 1
        ), f"Series 2 device {device_model} should have exactly 1 network interface"
        print(f"Series 2 validation passed: {device_model} has single eth0 interface")

    elif device_series == 3:
        # Series 3 should have multiple network interfaces
        assert (
            "eth0" in available_ports
        ), f"Series 3 device {device_model} should have eth0 management interface"
        assert (
            len(available_ports) >= 4
        ), f"Series 3 device {device_model} should have at least 4 network interfaces"
        print(
            f"Series 3 validation passed: {device_model} has {len(available_ports)} network interfaces"
        )

    # Validate minimum interface requirements
    assert (
        len(available_ports) >= 1
    ), f"Device {device_model} should have at least 1 network interface, found: {len(available_ports)}"

    # Store interface information for subsequent tests
    request.session.network_interface_detection_passed = True
    request.session.detected_network_interfaces = available_ports
    request.session.expected_network_interfaces = expected_network_interfaces
    request.session.network_interface_count = len(available_ports)

    print(f"Dynamic device detection successful for {device_model}")
    print(f"- Device: {device_model} (Series {device_series})")
    print(f"- Expected interfaces: {expected_network_interfaces}")
    print(f"- Detected interfaces: {available_ports}")
    print(f"- Interface count: {len(available_ports)}")
    print(f"- Forms detected: {forms}")

    print(f"DYNAMIC DEVICE DETECTION TEST COMPLETED: {device_model}")
