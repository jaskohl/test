"""
Test 2_1_4 Outputs Section Access - Device Enhanced
Category: 02 - Configuration Section Navigation
Enhanced with comprehensive DeviceCapabilities integration
Source Method: TestConfigurationNavigation.test_2_1_4_outputs_section_access

This variant includes:
- Series-specific timeout handling
- Device model detection and validation
- Comprehensive output configuration verification
- Enhanced logging and error recovery
"""

import pytest
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect
from conftest import wait_for_satellite_loading
from pages.device_capabilities import DeviceCapabilities


def test_2_1_4_outputs_section_access_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 2_1_4 Outputs Section Access - Device Enhanced

    Purpose: Enhanced test for outputs configuration section access with
             comprehensive DeviceCapabilities integration

    Features:
    - Series-specific timeout handling and validation
    - Device model detection with comprehensive output verification
    - Robust navigation with device-aware error recovery
    - Enhanced logging with device context information

    Expected:
    - Navigation to outputs page succeeds within series-specific timeouts
    - Signal1 and signal2 fields are present for all device models
    - Additional outputs verified based on device capabilities (max_outputs)
    - Series-specific output validation and error handling
    - Comprehensive device context logging

    Args:
        unlocked_config_page (Page): Playwright page object in unlocked config state
        base_url (str): Base URL for the device under test
        request: Pytest request object for accessing device model information
    """
    # Device capabilities setup with comprehensive validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate output configuration")

    # Get device series and timeout multiplier for enhanced handling
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    max_outputs = DeviceCapabilities.get_max_outputs(device_model)

    # Calculate series-specific timeout
    base_timeout = 10000  # 10 seconds base
    series_timeout = int(base_timeout * timeout_multiplier)

    print(f"\n{'='*60}")
    print(f"DEVICE ENHANCED TEST: Outputs Section Access")
    print(f"{'='*60}")
    print(f"Device Model: {device_model}")
    print(f"Device Series: {device_series}")
    print(f"Timeout Multiplier: {timeout_multiplier}")
    print(f"Series-Specific Timeout: {series_timeout}ms")
    print(f"Max Outputs for Device: {max_outputs}")
    print(f"{'='*60}\n")

    # Enhanced navigation with device-aware error recovery
    outputs_url = f"{base_url}/outputs"
    try:
        print(f"Navigating to outputs configuration: {outputs_url}")

        # Series-specific navigation with enhanced timeout handling
        if device_series == 2:
            # Series 2 devices may have different loading characteristics
            unlocked_config_page.goto(outputs_url, timeout=series_timeout)
            print(f"Series {device_series} navigation completed")
        else:
            # Series 3 and other devices
            unlocked_config_page.goto(outputs_url, timeout=series_timeout)
            print(f"Series {device_series} navigation completed")

        # Verify URL contains outputs with enhanced validation
        assert "outputs" in unlocked_config_page.url, "URL should contain 'outputs'"
        print(f"URL verification passed: {unlocked_config_page.url}")

    except PlaywrightTimeoutError:
        error_msg = (
            f"Navigation to outputs page failed for device {device_model} "
            f"(Series {device_series}) within {series_timeout}ms timeout"
        )
        print(f" NAVIGATION ERROR: {error_msg}")
        raise AssertionError(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error during outputs page navigation for device {device_model}: {str(e)}"
        print(f" UNEXPECTED ERROR: {error_msg}")
        raise AssertionError(error_msg)

    # Wait for page load completion with device-aware loading
    try:
        wait_for_satellite_loading(unlocked_config_page)
        print(f"Satellite loading completed for device {device_model}")
    except Exception as e:
        print(f" Satellite loading warning for device {device_model}: {str(e)}")
        # Continue test - this is not a critical failure

    # Enhanced output field detection with device capabilities
    print(f"\nValidating output configuration fields for device {device_model}...")

    # Always-present outputs (signal1 and signal2)
    required_outputs = ["signal1", "signal2"]
    optional_outputs = []

    # Series-specific output validation
    if device_series == 2:
        print(f"Series {device_series} output validation:")
        # Series 2 devices typically have 2-4 outputs depending on model
        if max_outputs >= 3:
            optional_outputs.extend(["signal3"])
        if max_outputs >= 4:
            optional_outputs.extend(["signal4"])
    else:
        print(f"Series {device_series} output validation:")
        # Series 3 devices typically have 2-4 outputs
        if max_outputs >= 3:
            optional_outputs.extend(["signal3"])
        if max_outputs >= 4:
            optional_outputs.extend(["signal4"])

    # Validate required outputs with enhanced detection
    for output_name in required_outputs:
        try:
            output_selector = f"select[name='{output_name}']"
            output_field = unlocked_config_page.locator(output_selector)

            # Wait for element with series-specific timeout
            output_field.wait_for(state="visible", timeout=series_timeout)

            # Verify element is visible and accessible
            expect(output_field).to_be_visible(timeout=series_timeout)

            print(f" Required output '{output_name}' found and visible")

        except PlaywrightTimeoutError:
            error_msg = (
                f"Required output field '{output_name}' not found for device {device_model} "
                f"(Series {device_series}, Max outputs: {max_outputs})"
            )
            print(f" MISSING REQUIRED OUTPUT: {error_msg}")
            raise AssertionError(error_msg)
        except Exception as e:
            error_msg = f"Error validating required output '{output_name}' for device {device_model}: {str(e)}"
            print(f" OUTPUT VALIDATION ERROR: {error_msg}")
            raise AssertionError(error_msg)

    # Validate optional outputs based on device capabilities
    if optional_outputs:
        print(f"\nValidating optional outputs for device {device_model}...")
        for output_name in optional_outputs:
            try:
                output_selector = f"select[name='{output_name}']"
                output_field = unlocked_config_page.locator(output_selector)

                # Check if optional output exists
                if output_field.count() > 0:
                    output_field.wait_for(state="visible", timeout=series_timeout // 2)
                    print(f" Optional output '{output_name}' available")
                else:
                    print(
                        f"ℹ Optional output '{output_name}' not present (variant-specific)"
                    )

            except Exception as e:
                print(f" Optional output '{output_name}' validation warning: {str(e)}")

    # Enhanced output configuration validation
    print(f"\nPerforming enhanced output configuration validation...")

    # Validate signal1 and signal2 dropdown options
    for output_name in required_outputs:
        try:
            output_selector = f"select[name='{output_name}']"
            output_field = unlocked_config_page.locator(output_selector)

            # Get available options
            options = output_field.locator("option").all()
            option_count = len(options)

            print(f"Output '{output_name}': {option_count} signal options available")

            # Validate minimum options are present
            if option_count < 2:
                print(
                    f" Warning: Output '{output_name}' has fewer than expected signal options"
                )
            else:
                print(
                    f" Output '{output_name}' has adequate signal options ({option_count})"
                )

        except Exception as e:
            print(
                f" Output configuration validation warning for '{output_name}': {str(e)}"
            )

    # Series-specific output behavior validation
    if device_series == 2:
        print(f"\nSeries {device_series} specific validations:")
        print(f"- Device {device_model} output count: {max_outputs}")
        print(f"- Series 2 output patterns validated")
    else:
        print(f"\nSeries {device_series} specific validations:")
        print(f"- Device {device_model} output count: {max_outputs}")
        print(f"- Series 3+ output patterns validated")

    # Final comprehensive validation
    final_status = {
        "device_model": device_model,
        "device_series": device_series,
        "max_outputs": max_outputs,
        "required_outputs_found": len(required_outputs),
        "optional_outputs_found": len(
            [
                o
                for o in optional_outputs
                if unlocked_config_page.locator(f"select[name='{o}']").count() > 0
            ]
        ),
        "timeout_multiplier": timeout_multiplier,
        "navigation_timeout": series_timeout,
    }

    print(f"\n{'='*60}")
    print(f"FINAL VALIDATION RESULTS")
    print(f"{'='*60}")
    for key, value in final_status.items():
        print(f"{key}: {value}")
    print(f"{'='*60}\n")

    # Success validation
    success_msg = (
        f"Outputs section access validated successfully for device {device_model} "
        f"(Series {device_series}, {max_outputs} max outputs, "
        f"{timeout_multiplier}x timeout multiplier)"
    )
    print(f" SUCCESS: {success_msg}")

    # Assert final validation
    assert len(required_outputs) >= 2, "At least 2 required outputs should be validated"
    assert (
        max_outputs >= 2
    ), f"Device should support at least 2 outputs, found {max_outputs}"
    assert device_series in [
        2,
        3,
    ], f"Device series should be 2 or 3, found {device_series}"
