"""
Test: 7.1.1.1 - Output 1 PPS Signal [DEVICE ENHANCED]
Category: Outputs Configuration (7)
Purpose: Test output 1 with PPS signal using DeviceCapabilities validation
Expected: PPS signal works correctly for output 1
Series: Both Series 2 and 3 (device-aware)
Priority: HIGH
Hardware: Device Only
Device-Aware: YES - Uses DeviceCapabilities database
Based on: test_07_outputs_config.py
Enhanced: 2025-12-01
"""

import pytest
import time
from playwright.sync_api import expect
from pages.outputs_config_page import OutputsConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_7_1_1_1_output_1_pps_device_enhanced(
    outputs_config_page: OutputsConfigPage, request
):
    """
    Test 7.1.1.1: Output 1 PPS Signal [DEVICE ENHANCED]
    Purpose: Test output 1 with PPS signal using DeviceCapabilities validation
    Expected: PPS signal works correctly for output 1
    Series: Both 2 and 3
    Device-Aware: Uses DeviceCapabilities database for device validation
    """
    # Get device context and validate
    device_model = request.session.get("device_model", "unknown")
    device_capabilities = DeviceCapabilities()

    if device_model not in device_capabilities.get_series_list():
        pytest.skip(f"Device model '{device_model}' not in DeviceCapabilities database")

    device_series = device_capabilities.get_device_series(device_model)

    # Check if output 1 is available
    max_outputs = device_capabilities.get_max_outputs(device_model)
    if max_outputs < 1:
        pytest.skip(f"Device {device_model} does not support output 1")

    # Check if PPS is available for output 1
    output_1_signals = device_capabilities.get_output_signal_types(device_model, 1)
    if "PPS" not in output_1_signals:
        pytest.skip(f"PPS signal not available for output 1 on {device_model}")

    print(f"Device {device_model}: Testing output 1 PPS signal")

    try:
        # Navigate to outputs config page
        outputs_config_page.navigate_to_page()
        outputs_config_page.verify_page_loaded()

        # Select PPS signal for output 1
        signal_select = outputs_config_page.page.locator("select[name='signal1']")
        expect(signal_select).to_be_visible()

        signal_select.select_option(value="PPS")
        print(f"Device {device_model}: Selected PPS for output 1")

        # Wait for UI updates
        time.sleep(1.5)

        # Verify expected time references for PPS
        expected_time_refs = device_capabilities.get_expected_time_refs(
            device_model, "PPS"
        )

        for time_ref in ["UTC", "LOCAL"]:
            time_radio = outputs_config_page.page.locator(
                f"input[name='time1'][value='{time_ref}']"
            )

            if time_ref in expected_time_refs:
                expect(time_radio).to_be_visible()
            else:
                expect(time_radio).to_be_hidden()

        # Save configuration
        success = outputs_config_page.save_configuration_changes_with_modification(
            channel=1
        )
        assert success, f"Failed to save output 1 PPS configuration"

        # Verify persistence
        outputs_config_page.page.reload()
        outputs_config_page.wait_for_page_load()
        outputs_config_page.verify_page_loaded()

        # Check signal persisted
        signal_select_after = outputs_config_page.page.locator("select[name='signal1']")
        expect(signal_select_after).to_be_visible()
        assert (
            signal_select_after.input_value() == "PPS"
        ), "PPS signal type did not persist"

        # Clean up - set back to OFF
        signal_select_after.select_option(value="OFF")
        outputs_config_page.save_configuration()

        print(f"Device {device_model}: Successfully tested output 1 PPS")

    except Exception as e:
        pytest.fail(f"Output 1 PPS test failed for {device_model}: {e}")

    # Cross-validate with DeviceCapabilities database
    device_network_config = device_capabilities.get_network_config(device_model)
    if device_network_config and "management_interface" in device_network_config:
        mgmt_iface = device_network_config["management_interface"]
        print(
            f"Device {device_model} (Series {device_series}): Output 1 PPS test completed"
        )
        print(f"Management interface: {mgmt_iface}")
