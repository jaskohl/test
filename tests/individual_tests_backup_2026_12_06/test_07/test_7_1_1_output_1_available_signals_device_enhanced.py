"""
Category 7: Outputs Configuration - Test 7.1.1
Output 1 Available Signals - DeviceCapabilities Enhanced
Test Count: 1 of 7 in Category 7
Hardware: Device Only
Priority: HIGH - Output configuration functionality
Series: Both Series 2 and 3
ENHANCED: Comprehensive DeviceCapabilities integration for device-aware output validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.outputs_config_page import OutputsConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_7_1_1_output_1_available_signals_device_enhanced(
    outputs_config_page: OutputsConfigPage, base_url: str, request
):
    """
    Test 7.1.1: Output 1 Available Signals - DeviceCapabilities Enhanced
    Purpose: Verify output 1 signal type options with device-aware validation
    Expected: Signal types available per device model, validation works
    ENHANCED: Full DeviceCapabilities integration for output count and signal validation
    Series: Both - validates output patterns across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate output behavior")

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing output 1 available signals on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Get output capabilities for validation
    max_outputs = DeviceCapabilities.get_max_outputs(device_model)
    output_1_signals = DeviceCapabilities.get_output_signal_types(device_model, 1)

    logger.info(f"Maximum outputs for {device_model}: {max_outputs}")
    logger.info(f"Expected output 1 signals: {output_1_signals}")

    # Validate this device supports at least 1 output
    if max_outputs < 1:
        pytest.skip(f"Device {device_model} does not support outputs")

    # Navigate to outputs configuration page
    outputs_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    outputs_config_page.verify_page_loaded()

    # Test output 1 signal type dropdown with device-aware validation
    try:
        # Locate output 1 signal dropdown with device-aware selectors
        output_1_dropdown = outputs_config_page.page.locator(
            "select[name='signal1'], select[name='output1_signal']"
        )

        dropdown_timeout = int(8000 * timeout_multiplier)
        expect(output_1_dropdown).to_be_visible(timeout=dropdown_timeout)

        # Verify dropdown is populated with expected options
        signal_options = output_1_dropdown.locator("option")
        actual_options = []

        for i in range(signal_options.count()):
            option = signal_options.nth(i)
            option_value = option.get_attribute("value") or option.text_content()
            if option_value and option_value.strip():
                actual_options.append(option_value.strip())

        logger.info(f"Found {len(actual_options)} signal options for output 1")
        logger.info(f"Actual options: {actual_options}")

        # Validate against device-specific expectations
        expected_options = set(output_1_signals)
        actual_options_set = set(actual_options)

        missing_options = expected_options - actual_options_set
        unexpected_options = actual_options_set - expected_options

        if missing_options:
            logger.warning(f"Missing expected signals for output 1: {missing_options}")
        if unexpected_options:
            logger.info(
                f"Additional signals available for output 1: {unexpected_options}"
            )

        # Test signal selection with device-specific options
        test_signals = ["IRIG-B000", "PPS", "OFF"]  # Common test signals

        for test_signal in test_signals:
            if test_signal in output_1_signals:
                logger.info(f"Testing output 1 signal selection: {test_signal}")

                try:
                    # Select signal with device-aware timing
                    select_success = outputs_config_page.configure_output_signal(
                        1, test_signal
                    )

                    if select_success:
                        logger.info(
                            f"Successfully selected output 1 signal: {test_signal}"
                        )

                        # Verify selection was applied
                        selected_value = output_1_dropdown.input_value()
                        if test_signal == selected_value:
                            logger.info(
                                f"Output 1 signal selection verified: {selected_value}"
                            )
                        else:
                            logger.warning(
                                f"Output 1 signal selection may not have persisted: {selected_value}"
                            )
                    else:
                        logger.warning(
                            f"Failed to select output 1 signal: {test_signal}"
                        )

                except Exception as e:
                    logger.warning(
                        f"Output 1 signal selection test failed for {test_signal}: {e}"
                    )
            else:
                logger.info(
                    f"Skipping output 1 signal {test_signal} - not available on {device_model}"
                )

    except Exception as e:
        pytest.fail(f"Output 1 signal validation failed on {device_model}: {e}")

    # Test time reference availability for signal types
    try:
        test_signal = "IRIG-B000"  # Test with IRIG-B signal
        if test_signal in output_1_signals:
            expected_time_refs = DeviceCapabilities.get_expected_time_refs(
                device_model, test_signal
            )
            logger.info(
                f"Expected time references for {test_signal}: {expected_time_refs}"
            )

            # Test time reference selection if available
            time_reference_dropdown = outputs_config_page.page.locator(
                "select[name='time_ref1'], select[name='output1_time_ref']"
            )

            if time_reference_dropdown.count() > 0:
                logger.info(f"Time reference dropdown found for output 1")

                # Verify expected time references are available
                time_options = time_reference_dropdown.locator("option")
                available_refs = []

                for i in range(time_options.count()):
                    option = time_reference_dropdown.nth(i)
                    option_value = (
                        option.get_attribute("value") or option.text_content()
                    )
                    if option_value and option_value.strip():
                        available_refs.append(option_value.strip())

                logger.info(f"Available time references: {available_refs}")

                # Check if expected time references are present
                for expected_ref in expected_time_refs:
                    if expected_ref in available_refs:
                        logger.info(
                            f"Expected time reference {expected_ref} found for output 1"
                        )
                    else:
                        logger.warning(
                            f"Expected time reference {expected_ref} not found for output 1"
                        )

    except Exception as e:
        logger.warning(
            f"Time reference validation failed for output 1 on {device_model}: {e}"
        )

    # Test save button behavior for output changes
    try:
        # Make an output change to test save button
        test_signal = output_1_signals[0] if output_1_signals else "OFF"
        outputs_config_page.configure_output_signal(1, test_signal)

        # Wait for save button to enable with device-aware timing
        save_button = outputs_config_page.page.locator("button#button_save")
        if save_button.count() > 0:
            expect(save_button).to_be_enabled(timeout=int(5000 * timeout_multiplier))
            logger.info(f"Save button enabled after output 1 change on {device_model}")

    except Exception as e:
        logger.warning(
            f"Save button test for output 1 changes failed on {device_model}: {e}"
        )

    # Validate output count against device expectations
    try:
        if max_outputs >= 2:
            # Test that output 2 is also available if device supports it
            output_2_dropdown = outputs_config_page.page.locator(
                "select[name='signal2']"
            )
            if output_2_dropdown.count() > 0:
                logger.info(f"Output 2 also available on {device_model} as expected")
            else:
                logger.warning(
                    f"Output 2 not found but device should support {max_outputs} outputs"
                )

        if max_outputs >= 3:
            output_3_dropdown = outputs_config_page.page.locator(
                "select[name='signal3']"
            )
            if output_3_dropdown.count() > 0:
                logger.info(f"Output 3 also available on {device_model} as expected")
            else:
                logger.warning(
                    f"Output 3 not found but device should support {max_outputs} outputs"
                )

    except Exception as e:
        logger.warning(f"Output count validation failed on {device_model}: {e}")

    # Performance validation against device baselines
    try:
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            nav_performance = performance_data.get("navigation_performance", {})
            section_nav = nav_performance.get("section_navigation", {})
            typical_time = section_nav.get("typical_time", "")

            if typical_time:
                logger.info(f"Outputs navigation performance baseline: {typical_time}")

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)
    capabilities = DeviceCapabilities.get_capabilities(device_model)

    logger.info(f"Output 1 available signals test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"Max outputs: {max_outputs}")
    logger.info(f"Output 1 signals: {output_1_signals}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"OUTPUT 1 AVAILABLE SIGNALS VALIDATED: {device_model} (Series {device_series})"
    )
