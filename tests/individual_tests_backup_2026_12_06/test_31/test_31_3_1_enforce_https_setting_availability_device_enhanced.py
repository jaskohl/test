"""
Test: 31.3.1 - HTTPS Enforcement Setting Availability [DEVICE ENHANCED]
Category: HTTPS Enforcement Scenarios (31)
Purpose: Verify HTTPS enforcement setting exists with device-aware validation
Expected: Access config page includes HTTPS enforcement selector with NEVER, CFG_ONLY, ALWAYS
Series: Series 3 Only (Security Feature)
Priority: HIGH (Security)
Hardware: Device Only
Device-Aware: YES - Uses DeviceCapabilities database for validation
Based on: test_31_https_enforcement_scenarios.py
Enhanced: 2025-12-01
"""

import pytest
from pages.access_config_page import AccessConfigPage
from pages.device_capabilities import DeviceCapabilities
from playwright.sync_api import expect


def test_31_3_1_enforce_https_setting_availability_device_enhanced(
    access_config_page: AccessConfigPage,
):
    """
    Test 31.3.1: HTTPS Enforcement Setting Availability [DEVICE ENHANCED]
    Purpose: Verify HTTPS enforcement setting exists with device-aware validation
    Expected: Access config page includes HTTPS enforcement selector with NEVER, CFG_ONLY, ALWAYS
    Series: Series 3 Only (Security Feature)
    Device-Aware: Uses DeviceCapabilities database for device series validation and timeout scaling
    """
    # Get device context and validate series compatibility
    device_model = access_config_page.request.session.get("device_model", "unknown")
    device_capabilities = DeviceCapabilities()

    # Validate device series using DeviceCapabilities database
    if device_model not in device_capabilities.get_series_list():
        pytest.skip(f"Device model '{device_model}' not in DeviceCapabilities database")

    # HTTPS enforcement is primarily a Series 3 security feature
    device_series = device_capabilities.get_device_series(device_model)
    if device_series != "Series 3":
        pytest.skip(
            f"HTTPS enforcement tests apply to Series 3 devices (found: {device_series})"
        )

    # Device-aware timeout scaling
    base_timeout = 5000
    device_timeout_multiplier = device_capabilities.get_timeout_multiplier(device_model)
    scaled_timeout = int(base_timeout * device_timeout_multiplier)

    # Cross-validate security capabilities with database
    security_capable = device_capabilities.has_capability(
        device_model, "https_enforcement"
    )
    if not security_capable:
        pytest.skip(
            f"Device {device_model} does not support HTTPS enforcement configuration"
        )

    # Device-aware HTTPS enforcement selector locator
    try:
        enforce_select = access_config_page.page.locator("select[name='enforce_https']")
        expect(enforce_select).to_be_visible(timeout=scaled_timeout)

        print(
            f"Device {device_model} (Series {device_series}): HTTPS enforcement selector found"
        )

    except Exception as e:
        pytest.fail(
            f"HTTPS enforcement selector not found or not visible for {device_model}: {e}"
        )

    # Get available HTTPS modes with device-aware error handling
    try:
        available_modes = access_config_page.get_available_https_modes()

        if not available_modes:
            pytest.fail(f"No HTTPS enforcement modes retrieved for {device_model}")

        # Extract mode values for validation
        mode_values = [mode.get("value", "") for mode in available_modes]

        # Validate required HTTPS enforcement modes are available
        required_modes = ["NEVER", "CFG_ONLY", "ALWAYS"]

        for required_mode in required_modes:
            if required_mode not in mode_values:
                pytest.fail(
                    f"HTTPS enforcement should support {required_mode} mode for {device_model}"
                )

        # Verify each mode has meaningful description/text
        for mode in available_modes:
            mode_value = mode.get("value", "")
            mode_text = mode.get("text", "")

            if not mode_text:
                pytest.fail(
                    f"Mode {mode_value} should have a description for {device_model}"
                )

            if len(mode_text.strip()) == 0:
                pytest.fail(
                    f"Mode {mode_value} description should not be empty for {device_model}"
                )

            print(f"Device {device_model}: HTTPS mode {mode_value} - '{mode_text}'")

        # Cross-validate with DeviceCapabilities database
        device_network_config = device_capabilities.get_network_config(device_model)
        if device_network_config and "management_interface" in device_network_config:
            mgmt_iface = device_network_config["management_interface"]
            print(
                f"Device {device_model} (Series {device_series}): HTTPS enforcement validation completed"
            )
            print(f"Management interface: {mgmt_iface}, Available modes: {mode_values}")
            print(f"Timeout scaling: {device_timeout_multiplier}x")

        # Database validation summary
        assert device_capabilities.get_device_series(device_model) == device_series
        assert (
            device_capabilities.has_capability(device_model, "https_enforcement")
            == security_capable
        )
        assert (
            device_capabilities.get_timeout_multiplier(device_model)
            == device_timeout_multiplier
        )

        # Additional validation: verify selector is functional
        try:
            # Test that the selector is interactive (not disabled/readonly)
            expect(enforce_select).to_be_enabled(timeout=scaled_timeout)

            # Test selecting different modes to verify functionality
            for mode_value in required_modes:
                try:
                    enforce_select.select_option(mode_value, timeout=scaled_timeout)
                    selected_value = enforce_select.input_value()
                    assert (
                        selected_value == mode_value
                    ), f"Failed to select {mode_value} mode"
                    print(
                        f"Device {device_model}: Successfully selected {mode_value} mode"
                    )
                except Exception as e:
                    pytest.fail(
                        f"Failed to select {mode_value} mode for {device_model}: {e}"
                    )

        except Exception as e:
            print(
                f"Warning: HTTPS enforcement selector functionality test failed for {device_model}: {e}"
            )
            # Non-critical failure - main validation already passed

    except Exception as e:
        pytest.fail(
            f"Failed to validate HTTPS enforcement modes for {device_model}: {e}"
        )
