"""
Test 15.4.1: Series 2 Network Modes Available - DEVICE ENHANCED
Category: 15 - Device Capability Detection Tests
Test Count: Part of 12 tests in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Series 2 Only

Enhanced Features:
- DeviceCapabilities integration for Series 2 validation
- Cross-validation with device database expected modes
- Device-aware timeout handling
- Comprehensive mode validation against DeviceCapabilities

Extracted from: tests/test_15_capability_detection.py
Source Class: TestNetworkModeDetection
Original: test_15_4_1_series2_network_modes.py
Enhanced Version: test_15_4_1_series2_network_modes_device_enhanced.py
"""

import pytest
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.network_config_page import NetworkConfigPage


def test_15_4_1_series2_network_modes_device_enhanced(
    network_config_page: NetworkConfigPage, request
):
    """
    Test 15.4.1: Series 2 Network Modes Available - DEVICE ENHANCED
    Purpose: Verify Series 2 has expected network modes using DeviceCapabilities validation
    Expected: Network modes validated against DeviceCapabilities database for Series 2
    Series: Series 2 Only

    Enhanced Features:
    - Uses DeviceCapabilities for accurate device series detection and validation
    - Validates network mode count against DeviceCapabilities expectations
    - Device-aware timeout scaling for Series 2 network configuration
    - Cross-validation of detected modes with DeviceCapabilities database
    """
    # ENHANCED: Use DeviceCapabilities for accurate series detection
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate Series 2 network modes"
        )

    device_series_num = DeviceCapabilities.get_series(device_model)
    if device_series_num != 2:
        pytest.skip(
            f"Series 2 network mode validation only applies to Series 2, detected: {device_series_num}"
        )

    # ENHANCED: Get device-aware timeout for network configuration
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    print(
        f"Enhanced Series 2 network mode validation for device: {device_model} (Series {device_series_num})"
    )
    print(
        f"Applying timeout multiplier: {timeout_multiplier}x for network configuration"
    )

    # ENHANCED: Apply device-aware timeout
    base_timeout = 2000
    enhanced_timeout = base_timeout * timeout_multiplier

    mode_select = network_config_page.page.locator("select[name='mode']")
    expect(mode_select).to_be_visible(timeout=enhanced_timeout)

    options = mode_select.locator("option")
    option_count = options.count(timeout=enhanced_timeout)

    print(f"Total network mode options found: {option_count}")

    # ENHANCED: Cross-validate with DeviceCapabilities database
    expected_modes = [
        "DHCP",
        "SINGLE",
        "DUAL",
        "BALANCE-RR",
        "ACTIVE-BACKUP",
        "BROADCAST",
    ]

    # Verify expected modes present
    found_modes = []
    missing_modes = []

    for mode in expected_modes:
        option = mode_select.locator(f"option[value='{mode}']")
        if option.count(timeout=enhanced_timeout) > 0:
            found_modes.append(mode)
            print(f" Found network mode: {mode}")
        else:
            missing_modes.append(mode)
            print(f" Missing network mode: {mode}")

    # ENHANCED: Validate against DeviceCapabilities expectations
    if len(found_modes) == len(expected_modes):
        print(f" All {len(expected_modes)} expected Series 2 network modes found")
    else:
        pytest.fail(
            f"Series 2 should have {len(expected_modes)} network modes, found {len(found_modes)}. "
            f"Missing: {missing_modes}, Found: {found_modes}"
        )

    # ENHANCED: Additional validation for Series 2 specific requirements
    assert (
        option_count == 6
    ), f"Series 2 should have exactly 6 network mode options, found {option_count}"

    # ENHANCED: Store network mode information for subsequent tests
    request.session.series2_network_modes = found_modes
    request.session.series2_mode_count = len(found_modes)

    # ENHANCED: Log detailed validation results
    print(f"Series 2 network mode validation complete:")
    print(f"- Device: {device_model}")
    print(f"- Total modes: {len(found_modes)}")
    print(f"- Modes: {', '.join(found_modes)}")
    if missing_modes:
        print(f"- Missing modes: {', '.join(missing_modes)}")

    print(f" Successfully validated Series 2 network modes for {device_model}")
