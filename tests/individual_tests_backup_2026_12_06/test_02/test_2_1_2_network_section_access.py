"""
Test 2.1.2: Network Section Accessible - Device-Aware
Purpose: Verify network section navigation and device-specific configuration availability

Category: 2 - Configuration Section Navigation
Test Type: Unit Test
Priority: HIGH
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect
from conftest import wait_for_satellite_loading
from pages.device_capabilities import DeviceCapabilities


def test_2_1_2_network_section_access(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 2.1.2: Network Section Accessible - Device-Aware"""
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate network configuration")

    unlocked_config_page.goto(f"{base_url}/network")
    assert "network" in unlocked_config_page.url, "Should navigate to network page"

    # MODERNIZED: Use DeviceCapabilities for device-aware network element verification
    device_series = DeviceCapabilities.get_series(device_model)
    capabilities = DeviceCapabilities.get_capabilities(device_model)

    if device_series == 2:
        # Series 2 devices: KRONOS-2R-HVXX-A2F, KRONOS-2P-HV-2
        # Single form with mode selection
        mode_select = unlocked_config_page.locator("select[name='mode']")
        expect(mode_select).to_be_visible()

        # Set network mode to DUAL to make ipaddrB visible for testing
        mode_select.select_option("DUAL")

        # Verify Series 2 specific elements
        ipaddr_field = unlocked_config_page.locator("input[name='ipaddr']")
        ipaddrB_field = unlocked_config_page.locator("input[name='ipaddrB']")
        expect(ipaddr_field).to_be_visible()
        expect(ipaddrB_field).to_be_visible()  # Now visible in DUAL mode

        print(f"Series 2 device {device_model}: Network configuration validated")

    elif device_series == 3:
        # Series 3 devices: All variations support network interfaces
        # Use DeviceCapabilities for interface detection
        ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)
        max_interfaces = capabilities.get("network_interfaces", 4)

        # Series 3 network elements (varies by hardware variant)
        eth0_ip = unlocked_config_page.locator("input[name='ip_eth0']")
        eth1_ip = unlocked_config_page.locator("input[name='ip_eth1']")
        sfp_mode = unlocked_config_page.locator("input[name='sfp_mode']")

        # Verify at least basic interface availability
        assert (
            eth0_ip.count() > 0
        ), f"Series 3 {device_model} should have eth0 configuration"
        assert (
            eth1_ip.count() > 0
        ), f"Series 3 {device_model} should have eth1 configuration"
        assert (
            sfp_mode.count() > 0
        ), f"Series 3 {device_model} should have SFP mode configuration"

        # Check for additional interfaces based on device variant
        eth2_ip = unlocked_config_page.locator("input[name='ip_eth2']")
        eth3_ip = unlocked_config_page.locator("input[name='ip_eth3']")

        if eth2_ip.count() > 0:
            print(
                f"Series 3 {device_model}: Extended interface set detected (eth0-eth2)"
            )
        if eth3_ip.count() > 0:
            print(f"Series 3 {device_model}: Full interface set detected (eth0-eth3)")

        # Verify PTP interfaces if available
        if DeviceCapabilities.is_ptp_supported(device_model):
            print(
                f"Series 3 {device_model}: PTP supported on {len(ptp_interfaces)} interfaces"
            )

        print(f"Series 3 device {device_model}: Network configuration validated")
    else:
        pytest.fail(f"Unknown device series for model {device_model}")
