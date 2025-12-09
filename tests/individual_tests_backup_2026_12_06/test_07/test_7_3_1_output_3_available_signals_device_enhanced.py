"""
Test: 7.3.1 - Output 3 with Available Signals [DEVICE ENHANCED]
Category: Outputs Configuration (7)
Purpose: Test output 3 with all available signal types for device
Expected: Device-specific signals work correctly for output 3
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


def test_7_3_1_output_3_available_signals_device_enhanced(
    outputs_config_page: OutputsConfigPage, request
):
    """
    Test 7.3.1: Output 3 Available Signals [DEVICE ENHANCED]
    Purpose: Test output 3 with all available signal types for device
    Expected: Device-specific signals work correctly for output 3
    Series: Both 2 and 3
    Device-Aware: Uses DeviceCapabilities database for device validation
    """
    # Get device context and validate
    device_model = request.session.get("device_model", "unknown")
    device_capabilities = DeviceCapabilities()

    if device_model not in device_capabilities.get_series_list():
        pytest.skip(f"Device model '{device_model}' not in DeviceCapabilities database")

    device_series = device_capabilities.get_device_series(device_model)

    # Check if output 3 is available
    max_outputs = device_capabilities.get_max_outputs(device_model)
    if max_outputs < 3:
        pytest.skip(f"Device {device_model} does not support output 3")

    # Get signals available for output 3
    output_3_signals = device_capabilities.get_output_signal_types(device_model, 3)

    if not output_3_signals:
        pytest.skip(f"No signals defined for output 3 on {device_model}")

    print(f"Device {device_model}: Testing output 3 with signals: {output_3_signals}")

    # Test each available signal for output 3
    for signal_type in output_3_signals:
        test_name = f"output_3_{signal_type}"

        try:
            # Navigate to outputs config page
            outputs_config_page.navigate_to_page()
            outputs_config_page.verify_page_loaded()

            # Select signal type for output 3
            signal_select = outputs_config_page.page.locator("select[name='signal3']")
            expect(signal_select).to_be_visible()

            signal_select.select_option(value=signal_type)
            print(f"Device {device_model}: Selected {signal_type} for output 3")

            # Wait for UI updates
            time.sleep(1.5)

            # Verify expected time references are visible/hidden
            expected_time_refs = device_capabilities.get_expected_time_refs(
                device_model, signal_type
            )

            for time_ref in ["UTC", "LOCAL"]:
                time_radio = outputs_config_page.page.locator(
                    f"input[name='time3'][value='{time_ref}']"
                )

                if time_ref in expected_time_refs:
                    expect(time_radio).to_be_visible()
                else:
                    expect(time_radio).to_be_hidden()

            # Save configuration
            success = outputs_config_page.save_configuration_changes_with_modification(
                channel=3
            )
            assert success, f"Failed to save output 3 {signal_type} configuration"

            # Verify persistence
            outputs_config_page.page.reload()
            outputs_config_page.wait_for_page_load()
            outputs_config_page.verify_page_loaded()

            # Check signal persisted
            signal_select_after = outputs_config_page.page.locator(
                "select[name='signal3']"
            )
            expect(signal_select_after).to_be_visible()
            assert (
                signal_select_after.input_value() == signal_type
            ), f"Signal type did not persist"

            # Clean up - set back to OFF
            signal_select_after.select_option(value="OFF")
            outputs_config_page.save_configuration()

            print(f"Device {device_model}: Successfully tested {test_name}")

        except Exception as e:
            print(f"Device {device_model}: Failed {test_name}: {e}")
            raise

    # Cross-validate with DeviceCapabilities database
    device_network_config = device_capabilities.get_network_config(device_model)
    if device_network_config and "management_interface" in device_network_config:
        mgmt_iface = device_network_config["management_interface"]
        print(
            f"Device {device_model} (Series {device_series}): Output 3 signal testing completed"
        )
        print(f"Management interface: {mgmt_iface}, Tested signals: {output_3_signals}")
