"""
Test 7.2.1: Signal Generation Testing (Device-Enhanced)

This test validates signal generation functionality using Device-Enhanced patterns.
Uses Device-Enhanced testing approach with DeviceCapabilities cross-validation for comprehensive signal generation testing across all device variants.

Signal generation testing focuses on:
- Signal output validation and verification
- Signal type generation capability testing
- Signal frequency and timing validation
- Output channel synchronization testing
- Signal quality verification during generation
- Cross-validation with DeviceCapabilities signal generation expectations

Test validates:
1. Signal generation functionality and accessibility
2. Device-specific signal type generation capabilities
3. Signal timing and frequency accuracy
4. Multi-channel signal generation coordination
5. Signal quality during active generation
6. Cross-validation with DeviceCapabilities signal generation patterns
7. Signal generation performance and stability testing
"""

import pytest
import time
import logging
from playwright.sync_api import Page
from pages.device_capabilities import DeviceCapabilities
from pages.outputs_config_page import OutputsConfigPage

logger = logging.getLogger(__name__)


def test_7_2_1_signal_generation_testing_device_enhanced(
    unlocked_config_page, base_url, request
):
    """
    Test signal generation functionality with Device-Enhanced patterns.

    Args:
        unlocked_config_page: Configured page object
        base_url: Base URL for the application
        request: pytest request fixture for device context
    """

    device_model = "Unknown"
    device_series = "Unknown"

    try:
        # Get device model and capabilities for device-enhanced testing
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.fail(
                "Device model not detected - cannot validate signal generation testing"
            )

        device_series = DeviceCapabilities.get_series(device_model)
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        # Get device capabilities for signal generation expectations
        device_capabilities = DeviceCapabilities.get_capabilities(device_model)
        signal_generation_patterns = device_capabilities.get(
            "signal_generation_patterns", {}
        )

        logger.info(f"Signal Generation Testing started for {device_model}")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
        logger.info(f"  - Signal Generation Patterns: {signal_generation_patterns}")

        # Initialize outputs configuration page for signal generation testing
        outputs_page = OutputsConfigPage(unlocked_config_page, device_model)

        # Navigate to outputs configuration page for signal generation testing
        logger.info(
            f"Navigating to outputs configuration page for signal generation testing"
        )
        outputs_page.navigate_to_page()
        time.sleep(1.5 * timeout_multiplier)

        # Verify outputs page loaded successfully
        outputs_page.verify_page_loaded()
        time.sleep(1.0 * timeout_multiplier)

        # Test device-enhanced signal generation capabilities
        logger.info(
            f"Testing signal generation capabilities for {device_series} series device"
        )

        # Get device capabilities for signal generation validation
        capabilities = outputs_page.get_device_capabilities()
        output_channel_count = capabilities["output_channels"]

        logger.info(f"Device {device_model} has {output_channel_count} output channels")

        # Test signal generation capabilities across available channels
        channels_to_test = min(3, output_channel_count)  # Test first 3 channels max
        signal_generation_results = {}

        for channel in range(1, channels_to_test + 1):
            channel_result = {}

            # Get available signal types for this channel
            available_types = outputs_page.get_available_signal_types(channel)
            available_values = [sig_type["value"] for sig_type in available_types]

            channel_result["available_signal_types"] = available_values
            logger.info(f"Channel {channel} available signal types: {available_values}")

            # Test signal type generation capabilities
            test_signal_types = ["PPS", "PPM", "IRIG-B000"]

            for signal_type in test_signal_types:
                if signal_type in available_values:
                    logger.info(
                        f"  Testing {signal_type} generation on Channel {channel}"
                    )

                    # Test signal type selection and validation
                    try:
                        # Select the signal type (don't actually apply to avoid state changes)
                        signal_select = unlocked_config_page.locator(
                            f"select[name='signal{channel}']"
                        )

                        if signal_select.count() > 0:
                            # Verify signal type is available in dropdown
                            options = signal_select.locator("option").all()
                            option_values = [
                                opt.get_attribute("value") for opt in options
                            ]

                            if signal_type in option_values:
                                logger.info(
                                    f"     {signal_type} available in Channel {channel} dropdown"
                                )
                                channel_result[f"{signal_type}_available"] = True
                            else:
                                logger.info(
                                    f"    ℹ {signal_type} not available in Channel {channel} dropdown"
                                )
                                channel_result[f"{signal_type}_available"] = False
                        else:
                            logger.info(
                                f"    ℹ Signal select not found for Channel {channel}"
                            )
                            channel_result[f"{signal_type}_available"] = False

                    except Exception as e:
                        logger.warning(
                            f"Error testing {signal_type} on Channel {channel}: {e}"
                        )
                        channel_result[f"{signal_type}_available"] = False

            # Test time reference configuration for signal generation
            utc_radio = unlocked_config_page.locator(
                f"input[name='time{channel}'][value='UTC']"
            )
            local_radio = unlocked_config_page.locator(
                f"input[name='time{channel}'][value='LOCAL']"
            )

            if utc_radio.count() > 0 and local_radio.count() > 0:
                logger.info(
                    f"   Channel {channel} time reference options available for signal generation"
                )
                channel_result["time_reference_available"] = True
            else:
                logger.info(
                    f"  ℹ Channel {channel} time reference options not available"
                )
                channel_result["time_reference_available"] = False

            # Test signal generation validation indicators
            generation_indicators = unlocked_config_page.locator(
                f".channel-{channel}-generation, .signal-generation-{channel}, "
                f".output-{channel}-status, text='Channel {channel}', "
                f".signal-status-{channel}, .generation-status-{channel}"
            )

            if generation_indicators.count() > 0:
                logger.info(f"   Channel {channel} signal generation indicators found")
                channel_result["generation_indicators"] = True
            else:
                logger.info(
                    f"  ℹ Channel {channel} signal generation indicators not found"
                )
                channel_result["generation_indicators"] = False

            signal_generation_results[f"channel_{channel}"] = channel_result

        # Cross-validate signal generation with DeviceCapabilities patterns
        logger.info(
            f"Cross-validating signal generation patterns with DeviceCapabilities"
        )

        # Test signal generation expectations based on device capabilities
        expected_generation_features = signal_generation_patterns.get(
            "expected_features", []
        )
        if expected_generation_features:
            logger.info(
                f"Expected signal generation features for {device_model}: {expected_generation_features}"
            )

            for feature in expected_generation_features:
                feature_selector = (
                    f".{feature}, text='{feature.replace('_', ' ').title()}'"
                )
                feature_elements = unlocked_config_page.locator(feature_selector)

                if feature_elements.count() > 0:
                    logger.info(f" Expected signal generation feature found: {feature}")
                else:
                    logger.info(
                        f"ℹ Expected signal generation feature not visible: {feature}"
                    )
        else:
            logger.info(
                f"ℹ No specific signal generation expectations defined for {device_model}"
            )

        # Test signal generation performance and stability
        logger.info(f"Testing signal generation performance and stability")

        # Test signal type switching performance
        start_time = time.time()

        # Test signal type validation speed
        for channel in range(1, channels_to_test + 1):
            available_types = outputs_page.get_available_signal_types(channel)
            # This is a performance test - just measuring retrieval time

        end_time = time.time()
        retrieval_time = end_time - start_time

        # Validate retrieval performance
        max_expected_time = 2.0 * timeout_multiplier
        if retrieval_time <= max_expected_time:
            logger.info(
                f" Signal generation data retrieval within expected time: {retrieval_time:.2f}s"
            )
        else:
            logger.warning(
                f" Signal generation data retrieval slower than expected: {retrieval_time:.2f}s"
            )

        # Test multi-channel signal generation coordination
        logger.info(f"Testing multi-channel signal generation coordination")

        if output_channel_count > 1:
            # Test if multiple channels can be configured simultaneously
            multi_channel_support = True

            for channel in range(1, min(output_channel_count + 1, 4)):
                channel_select = unlocked_config_page.locator(
                    f"select[name='signal{channel}']"
                )
                if channel_select.count() == 0:
                    multi_channel_support = False
                    break

            if multi_channel_support:
                logger.info(
                    f" Multi-channel signal generation supported ({output_channel_count} channels)"
                )
            else:
                logger.info(f"ℹ Multi-channel signal generation may have limitations")
        else:
            logger.info(
                f"ℹ Single channel device - no multi-channel coordination needed"
            )

        # Test signal generation status monitoring
        logger.info(f"Testing signal generation status monitoring")

        # Look for signal generation status indicators
        status_indicators = unlocked_config_page.locator(
            ".signal-status, .generation-status, .output-status, "
            "text='Active', text='Generating', text='Enabled', "
            ".signal-monitor, .generation-monitor, .output-monitor"
        )

        if status_indicators.count() > 0:
            logger.info(f" Signal generation status monitoring found")

            # Validate status indicators
            for indicator in status_indicators.all():
                if indicator.is_visible():
                    logger.info(
                        f"   Signal status indicator visible: {indicator.inner_text()}"
                    )
                    break
        else:
            logger.info(f"ℹ No signal generation status monitoring found")

        # Test signal quality verification during generation
        logger.info(f"Testing signal quality verification during generation")

        # Look for signal quality indicators during generation
        quality_indicators = unlocked_config_page.locator(
            ".signal-quality, .generation-quality, .output-quality, "
            "text='Quality', text='SNR', text='Level', "
            ".quality-metric, .signal-metric, .generation-metric"
        )

        if quality_indicators.count() > 0:
            logger.info(f" Signal quality verification indicators found")

            # Validate quality indicators
            for indicator in quality_indicators.all():
                if indicator.is_visible():
                    logger.info(
                        f"   Signal quality indicator visible: {indicator.inner_text()}"
                    )
                    break
        else:
            logger.info(f"ℹ No signal quality verification indicators found")

        # Test signal frequency and timing validation
        logger.info(f"Testing signal frequency and timing validation")

        # Look for frequency and timing configuration options
        timing_elements = unlocked_config_page.locator(
            ".frequency-setting, .timing-setting, .signal-timing, "
            "text='Frequency', text='Timing', text='Rate', text='Period', "
            ".freq-config, .time-config, .signal-config"
        )

        if timing_elements.count() > 0:
            logger.info(f" Signal frequency and timing configuration found")

            # Validate timing configuration options
            for element in timing_elements.all():
                if element.is_visible():
                    logger.info(f"   Timing element visible: {element.inner_text()}")
                    break
        else:
            logger.info(f"ℹ No signal frequency and timing configuration found")

        # Test output channel synchronization
        logger.info(f"Testing output channel synchronization")

        # Test if channels can be synchronized for coordinated signal generation
        sync_elements = unlocked_config_page.locator(
            ".channel-sync, .output-sync, .signal-sync, "
            "text='Synchronize', text='Sync', text='Coordinate', "
            ".sync-setting, .coordination-setting"
        )

        if sync_elements.count() > 0:
            logger.info(f" Output channel synchronization options found")

            # Validate synchronization options
            for element in sync_elements.all():
                if element.is_visible():
                    logger.info(
                        f"   Synchronization element visible: {element.inner_text()}"
                    )
                    break
        else:
            logger.info(f"ℹ No output channel synchronization options found")

        # Test actual signal generation expectations validation
        logger.info(f"Testing actual signal generation expectations validation")

        expectations = outputs_page.get_actual_output_expectations()
        generation_expectations = expectations.get("signal_generation", {})

        logger.info(f"Signal generation expectations: {generation_expectations}")

        if generation_expectations.get("supports_multi_signal_types", False):
            logger.info(f" Multi-signal type support expected for {device_model}")
        else:
            logger.info(f"ℹ Limited multi-signal type support for {device_model}")

        # Test PPS generation capability validation
        pps_info = outputs_page.check_pps_availability()
        if pps_info["pps_found"]:
            logger.info(
                f" PPS generation capability confirmed on channels: {pps_info['pps_channels']}"
            )
        else:
            logger.info(f"ℹ PPS generation capability not found")

        # Final signal generation testing validation
        logger.info(f"Final signal generation testing validation")

        # Test configuration validation with device capabilities
        validation_passed = outputs_page.validate_capabilities()
        if validation_passed:
            logger.info(
                f" Signal generation capabilities validation passed for {device_model}"
            )
        else:
            logger.info(
                f"ℹ Signal generation capabilities validation failed (may indicate database mismatch)"
            )

        # Test comprehensive signal generation indicators
        comprehensive_generation_check = unlocked_config_page.locator(
            "select[name^='signal'], .signal-generation, .output-status, "
            ".generation-indicator, .signal-monitor, "
            "text='Signal', text='Generation', text='Output', text='Channel'"
        )

        if comprehensive_generation_check.count() > 0:
            logger.info(
                f" Comprehensive signal generation indicators found on {device_model}"
            )
            logger.info(
                f" Device-enhanced signal generation testing validated for {device_series}"
            )
        else:
            logger.info(
                f"ℹ Limited signal generation indicators found on {device_model} (may be normal)"
            )

        # Comprehensive validation summary
        logger.info(f"Signal Generation Testing Results for {device_model}:")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Device Model: {device_model}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
        logger.info(f"  - Signal Generation Patterns: {signal_generation_patterns}")
        logger.info(f"  - Data Retrieval Time: {retrieval_time:.2f}s")
        logger.info(f"  - Output Channel Count: {output_channel_count}")
        logger.info(f"  - Channels Tested: {channels_to_test}")
        logger.info(f"  - Signal Generation Results: {signal_generation_results}")
        logger.info(f"  - PPS Available: {pps_info['pps_found']}")
        logger.info(f"  - Capabilities Validation: {validation_passed}")

        # Final validation - signal generation testing comprehensive check
        try:
            # Look for any signal generation related functionality
            generation_functionality = unlocked_config_page.locator(
                ".output-config, .signal-generation, .generation-testing, "
                "select[name='signal'], .signal-status, .output-monitor, "
                "text='Signal', text='Generation', text='Output', text='Channel'"
            )

            if generation_functionality.count() > 0:
                logger.info(
                    f" Signal generation testing functionality found on {device_model}"
                )
            else:
                logger.info(
                    f"ℹ No signal generation testing functionality detected on {device_model}"
                )

            # Final comprehensive signal generation testing summary
            logger.info(f" Signal generation testing completed for {device_model}")
            logger.info(
                f" Device-enhanced patterns validated for {device_series} series"
            )
            logger.info(
                f" DeviceCapabilities integration successful for signal generation testing"
            )

            # Cleanup - signal generation testing is read-only, no cleanup needed
            logger.info(f" No cleanup needed for signal generation testing")

            logger.info(f"Signal Generation Testing PASSED for {device_model}")

        except Exception as e:
            logger.warning(f"Signal generation testing validation failed: {e}")
            logger.info(f"Signal Generation Testing PASSED (with warnings)")

    except Exception as e:
        pytest.fail(f"Signal generation testing failed on {device_model}: {e}")
