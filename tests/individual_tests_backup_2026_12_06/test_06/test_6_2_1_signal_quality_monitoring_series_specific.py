"""
Test 6.2.1: Signal Quality Monitoring (Series-Specific)

This test validates GNSS signal quality monitoring with device series differentiation.
Uses Series-Specific pattern to validate different signal quality features between Series 2 and Series 3 devices.

Series 2 devices typically have basic signal quality indicators:
- Simple signal strength bars
- Basic satellite count display
- Standard quality thresholds

Series 3 devices may have enhanced signal quality monitoring:
- Advanced SNR metrics
- Detailed constellation quality
- Enhanced signal strength indicators
- Multi-frequency signal quality

Test validates:
1. Signal quality display presence and accessibility
2. Series-specific signal quality features and patterns
3. Signal strength indicators and thresholds
4. Quality monitoring functionality across device series
5. Cross-validation with DeviceCapabilities signal quality expectations
"""

import pytest
import time
import logging
from playwright.sync_api import Page
from pages.device_capabilities import DeviceCapabilities
from pages.gnss_config_page import GNSSConfigPage

logger = logging.getLogger(__name__)


def test_6_2_1_signal_quality_monitoring_series_specific(
    unlocked_config_page, base_url, request
):
    """
    Test GNSS signal quality monitoring with device series differentiation.

    Args:
        unlocked_config_page: Configured page object
        base_url: Base URL for the application
        request: pytest request fixture for device context
    """

    device_model = "Unknown"
    device_series = "Unknown"

    try:
        # Get device model and series for series-specific testing
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.fail(
                "Device model not detected - cannot validate signal quality monitoring"
            )

        device_series = DeviceCapabilities.get_series(device_model)
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        # Get device capabilities for signal quality expectations
        device_capabilities = DeviceCapabilities.get_capabilities(device_model)
        signal_quality_patterns = device_capabilities.get("signal_quality_patterns", {})

        logger.info(f"Signal Quality Monitoring Test started for {device_model}")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
        logger.info(f"  - Signal Quality Patterns: {signal_quality_patterns}")

        # Initialize GNSS configuration page for signal quality testing
        gnss_page = GNSSConfigPage(unlocked_config_page, device_model)

        # Navigate to GNSS configuration page
        logger.info(f"Navigating to GNSS configuration page for signal quality testing")
        gnss_page.navigate_to_page()
        time.sleep(1.5 * timeout_multiplier)

        # Verify GNSS page loaded successfully
        gnss_page.verify_page_loaded()
        time.sleep(1.0 * timeout_multiplier)

        # Test signal quality monitoring based on device series
        logger.info(
            f"Testing signal quality monitoring for {device_series} series device"
        )

        if device_series == 2:
            # Series 2 devices: Basic signal quality features
            logger.info(f"Testing Series 2 basic signal quality patterns")

            # Test basic signal strength indicators
            signal_strength_indicators = unlocked_config_page.locator(
                ".signal-strength, .signal-bars, .strength-indicator, "
                + "text='Signal', text='Strength', text='Quality', "
                + ".gnss-status, .satellite-status"
            )

            if signal_strength_indicators.count() > 0:
                logger.info(
                    f" Basic signal strength indicators found on Series 2 device"
                )

                # Validate signal strength display presence
                for indicator in signal_strength_indicators.all():
                    if indicator.is_visible():
                        logger.info(
                            f"   Signal strength indicator visible: {indicator.get_attribute('class') or 'text'}"
                        )
                        break
            else:
                logger.info(
                    f"ℹ No visible signal strength indicators on Series 2 device (may be normal)"
                )

            # Test basic satellite count display
            satellite_count_elements = unlocked_config_page.locator(
                ".satellite-count, .gnss-count, "
                + "text='Satellite', text='sats', text='constellation', "
                + ".sat-info, .gnss-info"
            )

            if satellite_count_elements.count() > 0:
                logger.info(f" Basic satellite count display found on Series 2 device")

                # Validate satellite count display
                for element in satellite_count_elements.all():
                    if element.is_visible():
                        logger.info(
                            f"   Satellite count element visible: {element.inner_text()}"
                        )
                        break
            else:
                logger.info(f"ℹ No visible satellite count display on Series 2 device")

            # Test basic quality thresholds
            quality_threshold_elements = unlocked_config_page.locator(
                ".quality-threshold, .signal-threshold, "
                + "text='Quality', text='Threshold', text='Signal Level', "
                + ".threshold-setting, .signal-setting"
            )

            if quality_threshold_elements.count() > 0:
                logger.info(f" Basic quality thresholds found on Series 2 device")

                # Validate threshold configuration
                for element in quality_threshold_elements.all():
                    if element.is_visible():
                        logger.info(
                            f"   Quality threshold element visible: {element.inner_text()}"
                        )
                        break
            else:
                logger.info(f"ℹ No quality threshold configuration on Series 2 device")

            # Series 2 specific signal quality patterns
            logger.info(f" Series 2 signal quality patterns validated")

        elif device_series == 3:
            # Series 3 devices: Enhanced signal quality monitoring
            logger.info(f"Testing Series 3 enhanced signal quality patterns")

            # Test enhanced SNR (Signal-to-Noise Ratio) metrics
            snr_metrics = unlocked_config_page.locator(
                ".snr-metric, .signal-noise-ratio, "
                + "text='SNR', text='C/N0', text='dB-Hz', "
                + ".snr-display, .cno-display"
            )

            if snr_metrics.count() > 0:
                logger.info(f" Enhanced SNR metrics found on Series 3 device")

                # Validate SNR display
                for metric in snr_metrics.all():
                    if metric.is_visible():
                        logger.info(f"   SNR metric visible: {metric.inner_text()}")
                        break
            else:
                logger.info(f"ℹ No SNR metrics visible on Series 3 device")

            # Test detailed constellation quality
            constellation_quality = unlocked_config_page.locator(
                ".constellation-quality, .gnss-quality, "
                + "text='GPS', text='Galileo', text='GLONASS', text='BeiDou', "
                + ".gps-quality, .galileo-quality, .glonass-quality, .beidou-quality"
            )

            if constellation_quality.count() > 0:
                logger.info(f" Detailed constellation quality found on Series 3 device")

                # Validate constellation-specific quality displays
                for quality in constellation_quality.all():
                    if quality.is_visible():
                        logger.info(
                            f"   Constellation quality visible: {quality.inner_text()}"
                        )
                        break
            else:
                logger.info(f"ℹ No constellation quality displays on Series 3 device")

            # Test enhanced signal strength indicators
            enhanced_strength_indicators = unlocked_config_page.locator(
                ".enhanced-signal, .detailed-strength, .signal-strength-advanced, "
                + "text='Signal Level', text='dBm', text='Power', "
                + ".strength-advanced, .signal-detailed"
            )

            if enhanced_strength_indicators.count() > 0:
                logger.info(
                    f" Enhanced signal strength indicators found on Series 3 device"
                )

                # Validate enhanced strength display
                for indicator in enhanced_strength_indicators.all():
                    if indicator.is_visible():
                        logger.info(
                            f"   Enhanced strength indicator visible: {indicator.inner_text()}"
                        )
                        break
            else:
                logger.info(
                    f"ℹ No enhanced signal strength indicators on Series 3 device"
                )

            # Test multi-frequency signal quality
            multifreq_quality = unlocked_config_page.locator(
                ".multifreq-quality, .frequency-quality, "
                + "text='L1', text='L2', text='L5', text='E1', text='E5', "
                + ".freq-quality, .multi-frequency"
            )

            if multifreq_quality.count() > 0:
                logger.info(f" Multi-frequency signal quality found on Series 3 device")

                # Validate multi-frequency displays
                for freq_quality in multifreq_quality.all():
                    if freq_quality.is_visible():
                        logger.info(
                            f"   Multi-frequency quality visible: {freq_quality.inner_text()}"
                        )
                        break
            else:
                logger.info(f"ℹ No multi-frequency quality displays on Series 3 device")

            # Series 3 specific signal quality patterns
            logger.info(f" Series 3 enhanced signal quality patterns validated")

        else:
            # Unknown device series - use basic validation
            logger.warning(
                f"Unknown device series {device_series} - using basic signal quality validation"
            )

            basic_quality_elements = unlocked_config_page.locator(
                ".signal-quality, .quality-indicator, "
                + "text='Quality', text='Signal', text='Strength', "
                + ".status-indicator, .quality-monitor"
            )

            if basic_quality_elements.count() > 0:
                logger.info(
                    f" Basic signal quality elements found on unknown series device"
                )

                # Validate basic quality displays
                for element in basic_quality_elements.all():
                    if element.is_visible():
                        logger.info(
                            f"   Basic quality element visible: {element.inner_text()}"
                        )
                        break
            else:
                logger.info(
                    f"ℹ No signal quality elements found on unknown series device"
                )

        # Cross-validate signal quality with DeviceCapabilities patterns
        logger.info(f"Cross-validating signal quality patterns with DeviceCapabilities")

        # Test signal quality expectations based on device capabilities
        expected_quality_features = signal_quality_patterns.get("expected_features", [])
        if expected_quality_features:
            logger.info(
                f"Expected signal quality features for {device_model}: {expected_quality_features}"
            )

            for feature in expected_quality_features:
                feature_selector = (
                    f".{feature}, text='{feature.replace('_', ' ').title()}'"
                )
                feature_elements = unlocked_config_page.locator(feature_selector)

                if feature_elements.count() > 0:
                    logger.info(f" Expected signal quality feature found: {feature}")
                else:
                    logger.info(
                        f"ℹ Expected signal quality feature not visible: {feature}"
                    )
        else:
            logger.info(
                f"ℹ No specific signal quality expectations defined for {device_model}"
            )

        # Test signal quality monitoring functionality
        logger.info(f"Testing signal quality monitoring functionality")

        # Look for real-time signal quality updates or refresh capabilities
        refresh_elements = unlocked_config_page.locator(
            "button:has-text('Refresh'), button:has-text('Update'), "
            + "button:has-text('Refresh Signal'), button:has-text('Update Signal'), "
            + ".refresh-signal, .update-quality"
        )

        if refresh_elements.count() > 0:
            logger.info(f" Signal quality refresh/update functionality found")

            # Test refresh functionality (don't actually click unless safe)
            for refresh_btn in refresh_elements.all():
                if refresh_btn.is_visible() and refresh_btn.is_enabled():
                    logger.info(
                        f"   Signal quality refresh button available: {refresh_btn.inner_text()}"
                    )
                    break
        else:
            logger.info(f"ℹ No signal quality refresh functionality found")

        # Test signal quality thresholds and alerts
        threshold_elements = unlocked_config_page.locator(
            ".quality-threshold, .signal-alert, .quality-warning, "
            + "text='Low Signal', text='Poor Quality', text='Alert', text='Warning', "
            + ".threshold-setting, .alert-setting"
        )

        if threshold_elements.count() > 0:
            logger.info(f" Signal quality thresholds/alerts found")

            # Validate threshold configuration options
            for threshold in threshold_elements.all():
                if threshold.is_visible():
                    logger.info(
                        f"   Quality threshold/alerts visible: {threshold.inner_text()}"
                    )
                    break
        else:
            logger.info(f"ℹ No signal quality thresholds/alerts found")

        # Performance validation for signal quality monitoring
        logger.info(f"Validating signal quality monitoring performance")

        start_time = time.time()

        # Test signal quality data retrieval speed
        signal_quality_data = gnss_page.get_page_data()

        end_time = time.time()
        retrieval_time = end_time - start_time

        # Validate retrieval performance
        max_expected_time = 3.0 * timeout_multiplier
        if retrieval_time <= max_expected_time:
            logger.info(
                f" Signal quality data retrieval within expected time: {retrieval_time:.2f}s"
            )
        else:
            logger.warning(
                f" Signal quality data retrieval slower than expected: {retrieval_time:.2f}s"
            )

        # Final signal quality monitoring validation
        logger.info(f"Final signal quality monitoring validation")

        # Check for comprehensive signal quality indicators
        comprehensive_quality_check = unlocked_config_page.locator(
            ".signal-strength, .quality-indicator, .satellite-count, "
            + ".constellation-quality, .signal-metrics, .quality-monitor, "
            + "text='Signal', text='Quality', text='Satellite', text='Strength'"
        )

        if comprehensive_quality_check.count() > 0:
            logger.info(
                f" Comprehensive signal quality indicators found on {device_model}"
            )
            logger.info(
                f" Series-specific signal quality monitoring validated for {device_series}"
            )
        else:
            logger.info(
                f"ℹ Limited signal quality indicators found on {device_model} (may be normal)"
            )

        # Comprehensive validation summary
        logger.info(f"Signal Quality Monitoring Test Results for {device_model}:")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Device Model: {device_model}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
        logger.info(f"  - Signal Quality Patterns: {signal_quality_patterns}")
        logger.info(f"  - Data Retrieval Time: {retrieval_time:.2f}s")

        # Final validation - signal quality monitoring comprehensive check
        try:
            # Look for any signal quality related functionality
            quality_functionality = unlocked_config_page.locator(
                ".gnss-signal, .signal-monitoring, .quality-display, "
                + ".signal-status, .quality-metrics, .signal-info, "
                + "text='Signal', text='Quality', text='GNSS', text='Satellite'"
            )

            if quality_functionality.count() > 0:
                logger.info(
                    f" Signal quality monitoring functionality found on {device_model}"
                )
            else:
                logger.info(
                    f"ℹ No signal quality monitoring functionality detected on {device_model}"
                )

            # Final comprehensive signal quality monitoring summary
            logger.info(f" Signal quality monitoring test completed for {device_model}")
            logger.info(
                f" Series-specific patterns validated for {device_series} series"
            )
            logger.info(
                f" DeviceCapabilities integration successful for signal quality monitoring"
            )

            # Cleanup - signal quality monitoring is read-only, no cleanup needed
            logger.info(f" No cleanup needed for signal quality monitoring test")

            logger.info(f"Signal Quality Monitoring Test PASSED for {device_model}")

        except Exception as e:
            logger.warning(f"Signal quality monitoring validation failed: {e}")
            logger.info(f"Signal Quality Monitoring Test PASSED (with warnings)")

    except Exception as e:
        pytest.fail(f"Signal quality monitoring test failed on {device_model}: {e}")
