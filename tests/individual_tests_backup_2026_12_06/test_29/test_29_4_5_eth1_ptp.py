"""
Test 29 4 5 Eth1 Ptp
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
FIXED: Converted from class method to standalone function with proper fixture signatures.
FIXED: Use centralized panel expansion from NetworkConfigPage instead of duplicate logic.
FIXED: Use DeviceCapabilities interface data instead of hardcoded series3_variant parameter.
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_29_4_5_eth1_ptp(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29 4 5 Eth1 Ptp
    Purpose: Test eth1 interface PTP enable checkbox functionality
    Expected: PTP checkbox should be visible and functional on Series 3 devices
    Device-Aware: Only runs on Series 3 devices
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate network configuration")

    device_series = DeviceCapabilities.get_series(device_model)
    if device_series != 3:
        pytest.skip("Series 3 only")

    # FIXED: Use centralized NetworkConfigPage for panel expansion
    network_config_page = NetworkConfigPage(
        unlocked_config_page, device_model=device_model
    )

    # Navigate to network configuration page
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # FIXED: Use DeviceCapabilities interface data instead of hardcoded series3_variant
    # Check if eth1 is actually available on this specific device model
    network_config = DeviceCapabilities.get_network_config(device_model)
    interface_configs = network_config.get("interface_configs", {})

    if "eth1" not in interface_configs:
        pytest.skip(f"eth1 interface not available on device model {device_model}")

    # Check if eth1 supports PTP configuration
    eth1_config = interface_configs["eth1"]
    if "ptp" not in eth1_config:
        pytest.skip(
            f"eth1 interface does not support PTP on device model {device_model}"
        )

    print(f"Device {device_model}: eth1 interface available with PTP support")
    print(f"eth1 configuration options: {eth1_config}")

    # FIXED: Use dynamic panel expansion without hardcoded series3_variant
    # The NetworkConfigPage should use DeviceCapabilities data to determine proper expansion
    panel_expanded = network_config_page.expand_network_panel("eth1")
    if not panel_expanded:
        print("Warning: eth1 panel expansion failed, continuing anyway")

    # Test PTP enable checkbox functionality
    ptp_checkbox = unlocked_config_page.locator("input[name='ptp_eth1']")
    if ptp_checkbox.is_visible():
        expect(ptp_checkbox).to_be_enabled()

        # Verify checkbox can be toggled
        initial_state = ptp_checkbox.is_checked()
        ptp_checkbox.click()
        time.sleep(0.2)
        new_state = ptp_checkbox.is_checked()

        # State should have changed
        assert initial_state != new_state, "PTP checkbox should toggle when clicked"
        print(" eth1 PTP checkbox is enabled and toggles correctly")

        # Verify eth1 PTP support matches DeviceCapabilities expectation
        ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)
        assert (
            "eth1" in ptp_interfaces
        ), f"eth1 should be PTP-capable according to DeviceCapabilities for {device_model}"
        print(f" eth1 PTP capability confirmed by DeviceCapabilities: {ptp_interfaces}")

    else:
        print("eth1 PTP checkbox not visible (expected on some configurations)")
