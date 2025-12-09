"""
Test 15.3.2: Detect Series 3 Network Variant - DEVICE ENHANCED
Category: 15 - Device Capability Detection Tests
Test Count: Part of 12 tests in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Series 3 Only

Enhanced Features:
- DeviceCapabilities integration for network interface detection
- Cross-validation with device database network configuration
- Device-aware timeout handling
- Network variant classification based on DeviceCapabilities

Extracted from: tests/test_15_capability_detection.py
Source Class: TestSeries3VariantDetection
Original: test_15_3_2_detect_network_variant.py
Enhanced Version: test_15_3_2_detect_network_variant_device_enhanced.py
"""

import pytest
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_15_3_2_detect_network_variant_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 15.3.2: Detect Series 3 Network Variant - DEVICE ENHANCED
    Purpose: Determine Series 3 network variant using DeviceCapabilities database
    Expected: Network configuration variant based on DeviceCapabilities data
    Series: Series 3 Only

    Enhanced Features:
    - Uses DeviceCapabilities for accurate device series and network configuration detection
    - Validates network interface count against database expectations
    - Device-aware timeout scaling for network configuration analysis
    - Cross-validation of network configuration with DeviceCapabilities data
    """
    # ENHANCED: Use DeviceCapabilities for accurate series detection
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot determine network variant")

    device_series_num = DeviceCapabilities.get_series(device_model)
    if device_series_num != 3:
        pytest.skip(
            f"Network variant detection only applies to Series 3, detected: {device_series_num}"
        )

    # ENHANCED: Get device-aware timeout for network configuration
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    print(
        f"Enhanced network variant detection for device: {device_model} (Series {device_series_num})"
    )
    print(f"Applying timeout multiplier: {timeout_multiplier}x for network navigation")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # ENHANCED: Apply device-aware timeout for form detection
    base_timeout = 5000
    enhanced_timeout = base_timeout * timeout_multiplier

    # Count forms (subtract 1 for session modal)
    all_forms = unlocked_config_page.locator("form")
    total_forms = all_forms.count(timeout=enhanced_timeout)
    network_forms = total_forms - 1

    print(f"Total forms detected: {total_forms}, Network forms: {network_forms}")

    # ENHANCED: Cross-validate with DeviceCapabilities database
    expected_network_interfaces = DeviceCapabilities.get_network_interfaces(
        device_model
    )
    expected_interface_count = len(expected_network_interfaces)

    print(
        f"DeviceCapabilities expects {expected_interface_count} network interfaces: {expected_network_interfaces}"
    )

    # Validate form count matches interface expectations
    if expected_interface_count > 0:
        assert (
            network_forms == expected_interface_count
        ), f"Network form count {network_forms} should match expected interface count {expected_interface_count} for {device_model}"
    else:
        # Fallback validation for unknown devices
        assert (
            network_forms >= 1
        ), f"Series 3 should have at least 1 network form, found {network_forms}"

    # ENHANCED: Check for redundancy mode field using DeviceCapabilities data
    has_redundancy = (
        unlocked_config_page.locator("select[name='redundancy_mode_eth1']").count(
            timeout=enhanced_timeout
        )
        > 0
    )

    print(f"Redundancy mode field present: {has_redundancy}")

    # ENHANCED: Validate network interface availability using DeviceCapabilities data
    if expected_network_interfaces:
        print(f"Validating network interface availability for {device_model}")
        found_interfaces = []
        missing_interfaces = []

        for interface in expected_network_interfaces:
            # Check for interface configuration elements
            interface_form = unlocked_config_page.locator(
                f"form[name='form_{interface}']"
            )
            interface_select = unlocked_config_page.locator(
                f"select[name='mode_{interface}']"
            )

            if (
                interface_form.count(timeout=enhanced_timeout) > 0
                or interface_select.count(timeout=enhanced_timeout) > 0
            ):
                found_interfaces.append(interface)
                print(f" Found network interface configuration for {interface}")
            else:
                missing_interfaces.append(interface)
                print(f" Missing network interface configuration for {interface}")

        # Log interface analysis
        print(f"Network interfaces found: {found_interfaces}")
        if missing_interfaces:
            print(f"Network interfaces not visible: {missing_interfaces}")

    # ENHANCED: Determine variant using both form count and DeviceCapabilities data
    if expected_interface_count > 0:
        if has_redundancy and network_forms >= expected_interface_count:
            variant_name = (
                f"Variant A (Full redundancy) - {network_forms} forms with HSR/PRP"
            )
        elif network_forms >= expected_interface_count:
            variant_name = (
                f"Variant B (Standard) - {network_forms} forms without redundancy"
            )
        else:
            variant_name = f"Variant C (Limited) - {network_forms} forms ({expected_interface_count} expected)"
    else:
        # Fallback variant determination
        if network_forms >= 5:
            if has_redundancy:
                variant_name = f"Variant A-like ({network_forms} forms with redundancy)"
            else:
                variant_name = (
                    f"Variant B-like ({network_forms} forms without redundancy)"
                )
        else:
            variant_name = f"Intermediate variant ({network_forms} forms)"

    print(f"Final network variant determination: {variant_name}")

    # ENHANCED: Store variant information for subsequent tests
    request.session.network_variant = variant_name
    request.session.network_interface_count = network_forms
    request.session.has_redundancy_mode = has_redundancy

    print(f" Successfully detected network variant for {device_model}: {variant_name}")
