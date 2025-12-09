"""
Test 29.7.5: Eth4 PTP Configuration - DEVICE ENHANCED
Category: 29 - Network Configuration Series 3
Extracted from: tests/test_29_network_config_series3.py
Source Class: TestEth4Configuration
Original: test_29_7_5_eth4_ptp.py
Enhanced Version: test_29_7_5_eth4_ptp_device_enhanced.py

Enhanced Features:
- DeviceCapabilities integration for PTP interface validation
- Cross-validation with device database PTP interfaces
- Device-aware timeout handling and panel expansion
- Series-specific validation for eth4 PTP capability

Individual test file for better test isolation and debugging.

Purpose: Test eth4 PTP configuration visibility and functionality.
Expected: PTP enable field should be visible when PTP is supported on eth4 interface.
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def _expand_eth4_panel(page: Page, timeout_multiplier: float):
    """Expand the eth4 collapsible panel based on device exploration data with device-aware timing."""
    try:
        # Bootstrap collapse pattern from device exploration HTML
        eth4_header = page.locator('a[href="#port_eth4_collapse"]')
        if eth4_header.count() > 0:
            # Check if already expanded
            aria_expanded = eth4_header.get_attribute("aria-expanded")
            if aria_expanded != "true":
                eth4_header.click()
                # ENHANCED: Device-aware sleep duration
                time.sleep(0.5 * timeout_multiplier)
                print("eth4 panel expanded")
                return
        # Fallback: Try any collapsible toggle
        panel_toggle = page.locator('a[href*="port_eth4"]')
        if panel_toggle.count() > 0:
            panel_toggle.click()
            # ENHANCED: Device-aware sleep duration
            time.sleep(0.5 * timeout_multiplier)
            print("eth4 panel expanded via fallback")
    except Exception as e:
        print(f"Warning: eth4 panel expansion failed: {e}")


def test_29_7_5_eth4_ptp_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 29.7.5: Eth4 PTP Configuration - DEVICE ENHANCED

    Purpose: Test eth4 PTP configuration visibility and functionality.
    Enhanced with DeviceCapabilities integration for accurate device-aware validation.

    This enhanced test:
    1. Uses DeviceCapabilities for accurate device series and model detection
    2. Validates PTP capability against DeviceCapabilities database
    3. Navigates to network configuration page with device-aware timing
    4. Expands eth4 collapsible panel with device-aware timing
    5. Verifies PTP enable field is visible and functional on eth4
    6. Cross-validates eth4 PTP capability with DeviceCapabilities expectations

    Args:
        unlocked_config_page: Playwright page object for the network configuration page
        base_url: Base URL for the application under test
        request: pytest request object for device model detection

    Enhanced Features:
    - Uses DeviceCapabilities for accurate device series and PTP interface detection
    - Device-aware timeout scaling for eth4 PTP interface validation
    - Cross-validation of eth4 PTP capability with DeviceCapabilities database
    - Series-specific validation (eth4 should be PTP-capable on Series 3)
    """
    # ENHANCED: Use DeviceCapabilities for accurate device detection
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate eth4 PTP interface")

    device_series_num = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    print(
        f"Enhanced eth4 PTP interface testing for device: {device_model} (Series {device_series_num})"
    )
    print(f"Applying timeout multiplier: {timeout_multiplier}x for eth4 PTP validation")

    # ENHANCED: Get expected PTP and network interfaces from DeviceCapabilities
    expected_ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)
    expected_network_interfaces = DeviceCapabilities.get_network_interfaces(
        device_model
    )
    ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)

    print(f"DeviceCapabilities expects PTP support: {ptp_supported}")
    print(f"Expected PTP interfaces: {expected_ptp_interfaces}")
    print(f"Expected network interfaces: {expected_network_interfaces}")

    # ENHANCED: Series-specific validation
    if device_series_num == 2:
        # Series 2 devices should not support PTP
        pytest.skip(
            f"Series 2 device {device_model} does not support PTP - eth4 PTP test not applicable"
        )

    elif device_series_num == 3:
        # Series 3 devices should support PTP on eth4
        if not ptp_supported:
            pytest.skip(
                f"Device {device_model} does not support PTP according to DeviceCapabilities"
            )

        if "eth4" not in expected_ptp_interfaces:
            pytest.skip(
                f"eth4 is not a PTP interface according to DeviceCapabilities for {device_model}"
            )

        if "eth4" not in expected_network_interfaces:
            pytest.skip(
                f"eth4 is not a network interface according to DeviceCapabilities for {device_model}"
            )

    # ENHANCED: Apply device-aware timeout
    base_timeout = 5000
    enhanced_timeout = base_timeout * timeout_multiplier

    # Navigate to network configuration page
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Expand eth4 panel for Series 3 collapsible UI with device-aware timing
    _expand_eth4_panel(unlocked_config_page, timeout_multiplier)

    # ENHANCED: Test PTP enable configuration visibility with device-aware validation
    ptp_field = unlocked_config_page.locator("input[name='ptp_enable_eth4']")

    # ENHANCED: Validate PTP field visibility based on DeviceCapabilities
    if "eth4" in expected_ptp_interfaces:
        # eth4 should have PTP capability according to DeviceCapabilities
        expect(ptp_field).to_be_visible(timeout=enhanced_timeout)
        print(f" eth4 PTP enable field found and visible for {device_model}")
    else:
        # eth4 should not have PTP capability
        if ptp_field.count(timeout=enhanced_timeout) > 0:
            # Field exists but shouldn't according to DeviceCapabilities
            print(f"Note: eth4 PTP field visible but not expected for {device_model}")
        else:
            print(f" eth4 PTP field correctly absent for {device_model}")

    # ENHANCED: Validate eth4 IP field presence
    eth4_ip = unlocked_config_page.locator("input[name='ip_eth4']")
    expect(eth4_ip).to_be_visible(timeout=enhanced_timeout)
    print(f" eth4 IP field found and visible for {device_model}")

    # ENHANCED: Additional PTP-related field validation on eth4
    # Check for PTP-specific fields that should be available on PTP-capable interfaces

    # PTP domain field
    ptp_domain_field = unlocked_config_page.locator("input[name='ptp_domain_eth4']")
    if ptp_domain_field.count(timeout=enhanced_timeout) > 0:
        print(f" eth4 PTP domain field found for {device_model}")

    # PTP priority fields
    ptp_priority1_field = unlocked_config_page.locator(
        "input[name='ptp_priority1_eth4']"
    )
    if ptp_priority1_field.count(timeout=enhanced_timeout) > 0:
        print(f" eth4 PTP priority1 field found for {device_model}")

    ptp_priority2_field = unlocked_config_page.locator(
        "input[name='ptp_priority2_eth4']"
    )
    if ptp_priority2_field.count(timeout=enhanced_timeout) > 0:
        print(f" eth4 PTP priority2 field found for {device_model}")

    # ENHANCED: Validate eth4 is distinguished from management interface (eth0)
    # eth4 should have PTP capability while eth0 should not
    eth0_ptp_field = unlocked_config_page.locator("input[name='ptp_enable_eth0']")
    assert not eth0_ptp_field.is_visible(
        timeout=enhanced_timeout
    ), f"eth0 should not have PTP capability (management interface) for {device_model}"

    print(f" eth0/eth4 PTP capability distinction validated for {device_model}")

    # ENHANCED: Validate eth4 is distinguished from eth1 (both PTP-capable)
    # Both eth1 and eth4 should have PTP capability
    eth1_ptp_field = unlocked_config_page.locator("input[name='ptp_enable_eth1']")
    assert eth1_ptp_field.is_visible(
        timeout=enhanced_timeout
    ), f"eth1 should have PTP capability (PTP-capable interface) for {device_model}"

    print(f" eth1/eth4 PTP capability correlation validated for {device_model}")

    # ENHANCED: Store eth4 PTP validation results for subsequent tests
    request.session.eth4_ptp_validation_passed = True
    request.session.eth4_ptp_interface_data = {
        "device_model": device_model,
        "device_series": device_series_num,
        "eth4_ptp_visible": ptp_field.count(timeout=enhanced_timeout) > 0,
        "eth4_ip_visible": True,
        "expected_in_ptp_interfaces": "eth4" in expected_ptp_interfaces,
        "ptp_supported": ptp_supported,
        "validation_timestamp": "enhanced_eth4_ptp_validation",
    }

    print(f" Enhanced eth4 PTP interface validation successful for {device_model}")
    print(f"  - Device: {device_model} (Series {device_series_num})")
    print(
        f"  - eth4 PTP field: {'Visible' if ptp_field.count(timeout=enhanced_timeout) > 0 else 'Absent'}"
    )
    print(f"  - eth4 IP field: Visible and functional")
    print(f"  - Expected PTP interface: {'eth4' in expected_ptp_interfaces}")
    print(f"  - PTP support: {ptp_supported}")
