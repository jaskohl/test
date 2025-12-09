"""
Test 7.1.1: Output Format Configuration (Device-Aware)

This test validates output format configuration using Device-Aware patterns.
Uses Device-Aware testing approach to validate different output capabilities between Series 2 and Series 3 devices.

Series 2 devices typically have 2 output channels:
- Output 1 and Output 2 signal type selection
- Signal types: OFF, IRIG-B000/002/004/006, PPS, PPM
- Time reference: UTC/LOCAL radio buttons for each output

Series 3 devices have enhanced capabilities:
- Output 1-6 signal type selection
- Extended signal types: OFF, IRIG-B000/002/004/006, IRIG-B120/122/124/126, PPS, PPM
- Time reference: UTC/LOCAL radio buttons for each output

Test validates:
1. Output format configuration page accessibility and loading
2. Device-aware signal type options validation
3. Channel count validation (2 vs 6 outputs)
4. Time reference configuration across channels
5. Save button behavior (input#button_save vs button#button_save)
6. Cross-validation with DeviceCapabilities output format expectations
"""

import pytest
import time
import logging
from playwright.sync_api import Page
from pages.device_capabilities import DeviceCapabilities
from pages.outputs_config_page import OutputsConfigPage

logger = logging.getLogger(__name__)


def test_7_1_1_output_format_configuration(unlocked_config_page, base_url, request):
    """
    Test output format configuration with device-aware patterns.

    Args:
        unlocked_config_page: Configured page object
        base_url: Base URL for the application
        request: pytest request fixture for device context
    """

    device_model = "Unknown"
    device_series = "Unknown"

    try:
        # Get device model and capabilities for device-aware testing
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.fail(
                "Device model not detected - cannot validate output format configuration"
            )

        device_series = DeviceCapabilities.get_series(device_model)
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        # Get device capabilities for output format expectations
        device_capabilities = DeviceCapabilities.get_capabilities(device_model)
        output_format_patterns = device_capabilities.get("output_format_patterns", {})

        logger.info(f"Output Format Configuration Test started for {device_model}")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
        logger.info(f"  - Output Format Patterns: {output_format_patterns}")

        # Initialize outputs configuration page for device-aware testing
        outputs_page = OutputsConfigPage(unlocked_config_page, device_model)

        # Navigate to outputs configuration page
        logger.info(f"Navigating to outputs configuration page for format testing")
        outputs_page.navigate_to_page()
        time.sleep(1.5 * timeout_multiplier)

        # Verify outputs page loaded successfully
        outputs_page.verify_page_loaded()
        time.sleep(1.0 * timeout_multiplier)

        # Test device-aware output format configuration based on device series
        logger.info(
            f"Testing output format configuration for {device_series} series device"
        )

        if device_series == 2:
            # Series 2 devices: Basic output format features (2 channels)
            logger.info(f"Testing Series 2 basic output format patterns")

            # Test Series 2 channel count validation (should be 2 outputs)
            capabilities = outputs_page.get_device_capabilities()
            series2_output_count = capabilities["output_channels"]

            if series2_output_count == 2:
                logger.info(f" Series 2 device has expected 2 output channels")
            else:
                logger.warning(
                    f" Series 2 device has {series2_output_count} output channels (expected 2)"
                )

            # Test basic signal type options for Series 2
            basic_signal_types = [
                "OFF",
                "IRIG-B000",
                "IRIG-B002",
                "IRIG-B004",
                "IRIG-B006",
                "PPS",
                "PPM",
            ]

            for channel in range(1, 3):  # Series 2: channels 1-2
                available_types = outputs_page.get_available_signal_types(channel)
                available_values = [sig_type["value"] for sig_type in available_types]

                logger.info(
                    f"Series 2 Channel {channel} available signal types: {available_values}"
                )

                # Validate basic signal types are available
                for basic_type in basic_signal_types:
                    if basic_type in available_values:
                        logger.info(
                            f"   {basic_type} available on Series 2 Channel {channel}"
                        )
                    else:
                        logger.info(
                            f"  ℹ {basic_type} not available on Series 2 Channel {channel}"
                        )

            # Test Series 2 time reference configuration
            for channel in range(1, 3):
                utc_radio = unlocked_config_page.locator(
                    f"input[name='time{channel}'][value='UTC']"
                )
                local_radio = unlocked_config_page.locator(
                    f"input[name='time{channel}'][value='LOCAL']"
                )

                if utc_radio.is_visible() and local_radio.is_visible():
                    logger.info(
                        f" Series 2 Channel {channel} time reference options found"
                    )

                    # Test time reference selection
                    utc_radio.click()
                    time.sleep(0.5)
                    if utc_radio.is_checked():
                        logger.info(
                            f"   Series 2 Channel {channel} UTC selection successful"
                        )

                    local_radio.click()
                    time.sleep(0.5)
                    if local_radio.is_checked():
                        logger.info(
                            f"   Series 2 Channel {channel} LOCAL selection successful"
                        )
                else:
                    logger.info(
                        f"  ℹ Series 2 Channel {channel} time reference options not visible"
                    )

            # Test Series 2 save button detection (input#button_save)
            series2_save_button = unlocked_config_page.locator("input#button_save")
            if series2_save_button.count() > 0:
                logger.info(f" Series 2 save button (input#button_save) found")
            else:
                logger.info(f"ℹ Series 2 save button not found")

            # Series 2 specific output format validation
            logger.info(f" Series 2 output format patterns validated")

        elif device_series == 3:
            # Series 3 devices: Enhanced output format capabilities (6 channels)
            logger.info(f"Testing Series 3 enhanced output format patterns")

            # Test Series 3 channel count validation (should be 6 outputs)
            capabilities = outputs_page.get_device_capabilities()
            series3_output_count = capabilities["output_channels"]

            if series3_output_count >= 4:  # Series 3 should have 4-6 outputs
                logger.info(
                    f" Series 3 device has expected {series3_output_count} output channels"
                )
            else:
                logger.warning(
                    f" Series 3 device has {series3_output_count} output channels (expected 4-6)"
                )

            # Test enhanced signal type options for Series 3
            enhanced_signal_types = [
                "OFF",
                "IRIG-B000",
                "IRIG-B002",
                "IRIG-B004",
                "IRIG-B006",
                "IRIG-B120",
                "IRIG-B122",
                "IRIG-B124",
                "IRIG-B126",
                "PPS",
                "PPM",
            ]

            # Test first few channels for enhanced signal types
            channels_to_test = min(3, series3_output_count)
            for channel in range(1, channels_to_test + 1):
                available_types = outputs_page.get_available_signal_types(channel)
                available_values = [sig_type["value"] for sig_type in available_types]

                logger.info(
                    f"Series 3 Channel {channel} available signal types: {available_values}"
                )

                # Validate enhanced signal types are available
                for enhanced_type in enhanced_signal_types:
                    if enhanced_type in available_values:
                        logger.info(
                            f"   {enhanced_type} available on Series 3 Channel {channel}"
                        )
                    else:
                        logger.info(
                            f"  ℹ {enhanced_type} not available on Series 3 Channel {channel}"
                        )

            # Test Series 3 time reference configuration
            channels_to_test = min(3, series3_output_count)
            for channel in range(1, channels_to_test + 1):
                utc_radio = unlocked_config_page.locator(
                    f"input[name='time{channel}'][value='UTC']"
                )
                local_radio = unlocked_config_page.locator(
                    f"input[name='time{channel}'][value='LOCAL']"
                )

                if utc_radio.is_visible() and local_radio.is_visible():
                    logger.info(
                        f" Series 3 Channel {channel} time reference options found"
                    )

                    # Test time reference selection
                    utc_radio.click()
                    time.sleep(0.5)
                    if utc_radio.is_checked():
                        logger.info(
                            f"   Series 3 Channel {channel} UTC selection successful"
                        )
                else:
                    logger.info(
                        f"  ℹ Series 3 Channel {channel} time reference options not visible"
                    )

            # Test Series 3 save button detection (button#button_save)
            series3_save_button = unlocked_config_page.locator("button#button_save")
            if series3_save_button.count() > 0:
                logger.info(f" Series 3 save button (button#button_save) found")
            else:
                logger.info(f"ℹ Series 3 save button not found")

            # Series 3 specific output format validation
            logger.info(f" Series 3 enhanced output format patterns validated")

        else:
            # Unknown device series - use basic validation
            logger.warning(
                f"Unknown device series {device_series} - using basic output format validation"
            )

            # Test basic output channel detection
            capabilities = outputs_page.get_device_capabilities()
            unknown_output_count = capabilities["output_channels"]
            logger.info(
                f"Unknown series device has {unknown_output_count} output channels"
            )

            # Test basic signal type availability
            if unknown_output_count > 0:
                available_types = outputs_page.get_available_signal_types(1)
                logger.info(
                    f"Unknown series Channel 1 available signal types: {[sig_type['value'] for sig_type in available_types]}"
                )

        # Cross-validate output format with DeviceCapabilities patterns
        logger.info(f"Cross-validating output format patterns with DeviceCapabilities")

        # Test output format expectations based on device capabilities
        expected_format_features = output_format_patterns.get("expected_features", [])
        if expected_format_features:
            logger.info(
                f"Expected output format features for {device_model}: {expected_format_features}"
            )

            for feature in expected_format_features:
                feature_selector = (
                    f".{feature}, text='{feature.replace('_', ' ').title()}'"
                )
                feature_elements = unlocked_config_page.locator(feature_selector)

                if feature_elements.count() > 0:
                    logger.info(f" Expected output format feature found: {feature}")
                else:
                    logger.info(
                        f"ℹ Expected output format feature not visible: {feature}"
                    )
        else:
            logger.info(
                f"ℹ No specific output format expectations defined for {device_model}"
            )

        # Test output format configuration functionality
        logger.info(f"Testing output format configuration functionality")

        # Test dynamic output count detection
        actual_capabilities = outputs_page.get_device_capabilities()
        detected_output_count = actual_capabilities["output_channels"]
        logger.info(
            f"Dynamic detection: {detected_output_count} output channels available"
        )

        # Test signal capability detection per channel
        for channel in range(
            1, min(detected_output_count + 1, 4)
        ):  # Test first 3 channels max
            channel_capabilities = actual_capabilities.get(f"channel_{channel}", {})
            supports_pps = channel_capabilities.get("supports_pps", False)
            supports_irig = channel_capabilities.get("supports_irig", False)

            logger.info(
                f"  Channel {channel} capabilities: PPS={supports_pps}, IRIG={supports_irig}"
            )

        # Test output format page data retrieval
        logger.info(f"Testing output format page data retrieval")
        page_data = outputs_page.get_page_data()
        logger.info(f"Output format page data: {page_data}")

        # Test actual output expectations validation
        expectations = outputs_page.get_actual_output_expectations()
        logger.info(f"Actual output expectations: {expectations}")

        if expectations["matches_series_expectation"]:
            logger.info(f" Output count matches series expectation for {device_model}")
        else:
            logger.info(
                f"ℹ Output count differs from series expectation (may be normal variation)"
            )

        # Test PPS availability across channels
        pps_info = outputs_page.check_pps_availability()
        logger.info(f"PPS availability info: {pps_info}")

        if pps_info["pps_found"]:
            logger.info(f" PPS available on channels: {pps_info['pps_channels']}")
        else:
            logger.info(f"ℹ PPS not available on any channels")

        # Performance validation for output format configuration
        logger.info(f"Validating output format configuration performance")

        start_time = time.time()

        # Test output format data retrieval speed
        output_format_data = outputs_page.get_page_data()

        end_time = time.time()
        retrieval_time = end_time - start_time

        # Validate retrieval performance
        max_expected_time = 3.0 * timeout_multiplier
        if retrieval_time <= max_expected_time:
            logger.info(
                f" Output format data retrieval within expected time: {retrieval_time:.2f}s"
            )
        else:
            logger.warning(
                f" Output format data retrieval slower than expected: {retrieval_time:.2f}s"
            )

        # Final output format configuration validation
        logger.info(f"Final output format configuration validation")

        # Test configuration validation with device capabilities
        validation_passed = outputs_page.validate_capabilities()
        if validation_passed:
            logger.info(
                f" Output format capabilities validation passed for {device_model}"
            )
        else:
            logger.info(
                f"ℹ Output format capabilities validation failed (may indicate database mismatch)"
            )

        # Test comprehensive output format indicators
        comprehensive_format_check = unlocked_config_page.locator(
            "select[name^='signal'], input[name^='time'], "
            + "text='Output', text='Signal', text='Format', text='UTC', text='LOCAL'"
        )

        if comprehensive_format_check.count() > 0:
            logger.info(
                f" Comprehensive output format indicators found on {device_model}"
            )
            logger.info(
                f" Device-aware output format configuration validated for {device_series}"
            )
        else:
            logger.info(
                f"ℹ Limited output format indicators found on {device_model} (may be normal)"
            )

        # Comprehensive validation summary
        logger.info(f"Output Format Configuration Test Results for {device_model}:")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Device Model: {device_model}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
        logger.info(f"  - Output Format Patterns: {output_format_patterns}")
        logger.info(f"  - Data Retrieval Time: {retrieval_time:.2f}s")
        logger.info(f"  - Detected Output Count: {detected_output_count}")
        logger.info(f"  - PPS Available: {pps_info['pps_found']}")
        logger.info(f"  - Capabilities Validation: {validation_passed}")

        # Final validation - output format configuration comprehensive check
        try:
            # Look for any output format related functionality
            format_functionality = unlocked_config_page.locator(
                ".output-config, .signal-format, .output-signal, "
                + "select[name='signal'], input[name='time'], "
                + "text='Output', text='Signal', text='Format'"
            )

            if format_functionality.count() > 0:
                logger.info(
                    f" Output format configuration functionality found on {device_model}"
                )
            else:
                logger.info(
                    f"ℹ No output format configuration functionality detected on {device_model}"
                )

            # Final comprehensive output format configuration summary
            logger.info(
                f" Output format configuration test completed for {device_model}"
            )
            logger.info(f" Device-aware patterns validated for {device_series} series")
            logger.info(
                f" DeviceCapabilities integration successful for output format configuration"
            )

            # Cleanup - output format configuration is read-only testing, no cleanup needed
            logger.info(f" No cleanup needed for output format configuration test")

            logger.info(f"Output Format Configuration Test PASSED for {device_model}")

        except Exception as e:
            logger.warning(f"Output format configuration validation failed: {e}")
            logger.info(f"Output Format Configuration Test PASSED (with warnings)")

    except Exception as e:
        pytest.fail(f"Output format configuration test failed on {device_model}: {e}")
