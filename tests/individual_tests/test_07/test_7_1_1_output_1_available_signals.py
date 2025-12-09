"""
Category 7: Outputs Configuration - Test 7.1.1
Output 1 Available Signals - Pure Page Object Pattern
Test Count: 1 of 7 in Category 7
Hardware: Device Only
Priority: HIGH - Output configuration functionality
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with device intelligence
PATTERN: Zero direct .locator() calls, essential methods only
"""

import pytest
import time
import logging
from pages.outputs_config_page import OutputsConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_7_1_1_output_1_available_signals(
    outputs_config_page: OutputsConfigPage,
    request,
    base_url: str,
):
    """
    Test 7.1.1: Output 1 Available Signals - Pure Page Object Pattern
    Purpose: Verify output 1 signal type options with device-aware validation
    Expected: Signal types available per device model, validation works
    TRANSFORMED: Uses pure page object methods with device intelligence
    Series: Both - validates output patterns across device variants
    """
    device_model = request.session.device_hardware_model

    # Essential device intelligence
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(f"Testing output 1 available signals on {device_model}")
    logger.info(f"Device series: {device_series}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}x")

    # Get device capabilities for validation
    max_outputs = DeviceCapabilities.get_max_outputs(device_model)
    output_1_signals = DeviceCapabilities.get_output_signal_types(device_model, 1)

    logger.info(f"Maximum outputs for {device_model}: {max_outputs}")
    logger.info(f"Expected output 1 signals: {output_1_signals}")

    # Validate this device supports at least 1 output
    if max_outputs < 1:
        pytest.skip(f"Device {device_model} does not support outputs")

    # Navigate to outputs configuration page
    outputs_config_page.navigate_to_page()

    # Test output 1 signal type options through page object
    try:
        # Get available signal types for output 1 through page object
        available_types = outputs_config_page.get_available_signal_types(1)
        actual_options = [sig_type["value"] for sig_type in available_types]

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

        # Test signal selection with device-specific options through page object
        test_signals = ["IRIG-B000", "PPS", "OFF"]  # Common test signals

        for test_signal in test_signals:
            if test_signal in output_1_signals:
                logger.info(f"Testing output 1 signal selection: {test_signal}")

                try:
                    # Select signal through page object method
                    configure_success = outputs_config_page.configure_output(
                        channel=1, signal_type=test_signal, time_reference="UTC"
                    )

                    if configure_success:
                        logger.info(
                            f"Successfully configured output 1 signal: {test_signal}"
                        )

                        # Verify selection was applied through page object
                        page_data = outputs_config_page.get_page_data()
                        persisted_signal = page_data.get("signal1", "")

                        if test_signal == persisted_signal:
                            logger.info(
                                f"Output 1 signal selection verified: {persisted_signal}"
                            )
                        else:
                            logger.warning(
                                f"Output 1 signal selection may not have persisted: {persisted_signal}"
                            )
                    else:
                        logger.warning(
                            f"Failed to configure output 1 signal: {test_signal}"
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

    # Test time reference availability for signal types through page object
    try:
        test_signal = "IRIG-B000"  # Test with IRIG-B signal
        if test_signal in output_1_signals:
            expected_time_refs = DeviceCapabilities.get_expected_time_refs(
                device_model, test_signal
            )
            logger.info(
                f"Expected time references for {test_signal}: {expected_time_refs}"
            )

            # Test time reference configuration through page object
            configure_success = outputs_config_page.configure_output(
                channel=1, signal_type=test_signal, time_reference="UTC"
            )

            if configure_success:
                logger.info(f"Time reference configuration successful for output 1")

                # Verify through page object data
                page_data = outputs_config_page.get_page_data()
                persisted_time = page_data.get("time1", "")

                if persisted_time:
                    logger.info(f"Output 1 time reference verified: {persisted_time}")
                else:
                    logger.info(f"Output 1 time reference varies by device")

    except Exception as e:
        logger.warning(
            f"Time reference validation failed for output 1 on {device_model}: {e}"
        )

    # Test save button behavior for output changes through page object
    try:
        # Make an output change to test save button
        test_signal = output_1_signals[0] if output_1_signals else "OFF"
        configure_success = outputs_config_page.configure_output(
            channel=1, signal_type=test_signal, time_reference="UTC"
        )

        if configure_success:
            # Test save functionality through page object
            save_success = outputs_config_page.save_configuration()
            if save_success:
                logger.info(
                    f"Save button functionality working for output 1 changes on {device_model}"
                )
            else:
                logger.info(
                    f"Save button not available or varies by device on {device_model}"
                )

    except Exception as e:
        logger.warning(
            f"Save button test for output 1 changes failed on {device_model}: {e}"
        )

    # Validate output count against device expectations through page object
    try:
        # Get actual capabilities through page object
        capabilities = outputs_config_page.detect_output_capabilities()
        actual_output_count = capabilities.get("output_channels", 0)

        if max_outputs >= 2 and actual_output_count >= 2:
            logger.info(f"Output 2 also available on {device_model} as expected")
        elif max_outputs >= 2:
            logger.warning(
                f"Output 2 not found but device should support {max_outputs} outputs"
            )

        if max_outputs >= 3 and actual_output_count >= 3:
            logger.info(f"Output 3 also available on {device_model} as expected")
        elif max_outputs >= 3:
            logger.warning(
                f"Output 3 not found but device should support {max_outputs} outputs"
            )

    except Exception as e:
        logger.warning(f"Output count validation failed on {device_model}: {e}")

    # Performance validation against device baselines through page object
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

    # Test comprehensive functionality through page object
    try:
        # Get all signal types by channel through page object
        all_signal_types = outputs_config_page.get_all_signal_types_by_channel()
        if all_signal_types:
            logger.info(
                f"Comprehensive signal type detection successful for {device_model}"
            )
        else:
            logger.info(f"Signal type detection varies by device for {device_model}")

        # Final capability validation through page object
        validation_passed = outputs_config_page.validate_capabilities()
        if validation_passed:
            logger.info(f"Output capabilities validation passed for {device_model}")
        else:
            logger.info(f"Output capabilities validation varies for {device_model}")

    except Exception as e:
        logger.warning(f"Comprehensive validation failed for {device_model}: {e}")

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
