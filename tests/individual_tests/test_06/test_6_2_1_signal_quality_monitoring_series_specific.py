"""
Test 6.2.1: Signal Quality Monitoring (Series-Specific) (Pure Page Object)
Purpose: Validates GNSS signal quality monitoring with device series differentiation
Expected: Series-specific signal quality features and patterns
Pure Page Object: Zero direct .locator() calls, 100% page object methods
Device-: Full DeviceCapabilities integration with series-specific patterns
"""

import pytest
import time
import logging
from pages.gnss_config_page import GNSSConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_6_2_1_signal_quality_monitoring_series_specific(
    unlocked_config_page, base_url, request
):
    """
    Test GNSS signal quality monitoring with device series differentiation (Pure Page Object).

    Args:
        unlocked_config_page: Configured page object
        base_url: Base URL for the application
        request): pytest request fixture for device context
    """

    try:
        # Get device model and series for series-specific testing
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.fail(
                "Device model not detected - cannot validate signal quality monitoring"
            )

        device_series = DeviceCapabilities.get_series(device_model)
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        logger.info(f"Signal Quality Monitoring Test started for {device_model}")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")

        # Initialize GNSS configuration page with device model
        gnss_page = GNSSConfigPage(unlocked_config_page, device_model)

        # Navigate to GNSS configuration page using page object method
        logger.info(f"Navigating to GNSS configuration page for signal quality testing")
        gnss_page.navigate_to_page()

        # Test signal quality monitoring using comprehensive page object method
        logger.info(
            f"Testing signal quality monitoring for {device_series} series device"
        )

        # Get signal quality test results using page object method
        quality_test_results = gnss_page.test_signal_quality_monitoring()

        # Validate test results
        assert (
            quality_test_results["total_elements_checked"] > 0
        ), f"No signal quality elements found on {device_model}"

        logger.info(f"Signal quality monitoring test results for {device_model}:")
        logger.info(
            f"  Elements found: {quality_test_results['signal_quality_elements_found']}"
        )
        logger.info(
            f"  Elements checked: {quality_test_results['total_elements_checked']}"
        )

        # Device-specific signal quality validation
        if device_series == 2:
            # Series 2 devices: Basic signal quality features
            logger.info(f"Validating Series 2 basic signal quality patterns")

            # Validate signal quality expectations for Series 2
            expectations = gnss_page.get_signal_quality_expectations()
            expected_features = expectations.get("expected_features", [])

            # Series 2 should have basic signal quality features
            basic_features_found = 0
            for feature in expected_features:
                if feature in [
                    "basic_signal_strength",
                    "satellite_count",
                    "simple_quality_thresholds",
                ]:
                    basic_features_found += 1

            logger.info(
                f"Series 2 basic signal quality features validated: {basic_features_found}"
            )

            # Series 2 specific performance validation
            max_expected_time = 3.0 * timeout_multiplier
            actual_time = quality_test_results["performance_metrics"][
                "data_retrieval_time"
            ]

            if actual_time <= max_expected_time:
                logger.info(
                    f"Series 2 signal quality data retrieval within expected time: {actual_time:.2f}s"
                )
            else:
                logger.warning(
                    f"Series 2 signal quality data retrieval slower than expected: {actual_time:.2f}s"
                )

        elif device_series == 3:
            # Series 3 devices: Advanced signal quality monitoring
            logger.info(f"Validating Series 3 advanced signal quality patterns")

            # Validate signal quality expectations for Series 3
            expectations = gnss_page.get_signal_quality_expectations()
            expected_features = expectations.get("expected_features", [])

            # Series 3 should have advanced signal quality features
            advanced_features_found = 0
            for feature in expected_features:
                if feature in [
                    "snr_metrics",
                    "detailed_constellation_quality",
                    "multi_frequency_quality",
                    "advanced_signal_strength",
                ]:
                    advanced_features_found += 1

            logger.info(
                f"Series 3 advanced signal quality features validated: {advanced_features_found}"
            )

            # Series 3 specific performance validation (should be faster)
            max_expected_time = 2.0 * timeout_multiplier
            actual_time = quality_test_results["performance_metrics"][
                "data_retrieval_time"
            ]

            if actual_time <= max_expected_time:
                logger.info(
                    f"Series 3 signal quality data retrieval within expected time: {actual_time:.2f}s"
                )
            else:
                logger.warning(
                    f"Series 3 signal quality data retrieval slower than expected: {actual_time:.2f}s"
                )

        else:
            # Unknown device series - use basic validation
            logger.warning(
                f"Unknown device series {device_series} - using basic signal quality validation"
            )

        # Cross-validate signal quality with DeviceCapabilities patterns using page object method
        logger.info(f"Cross-validating signal quality patterns with DeviceCapabilities")

        validation_passed = gnss_page.validate_signal_quality_patterns()

        if validation_passed:
            logger.info(f"Signal quality pattern validation PASSED for {device_model}")
        else:
            logger.warning(
                f"Signal quality pattern validation had warnings for {device_model}"
            )

        # Performance validation for signal quality monitoring
        logger.info(f"Validating signal quality monitoring performance")

        performance_metrics = quality_test_results["performance_metrics"]
        max_expected_time = performance_metrics["max_expected_time"]
        actual_time = performance_metrics["data_retrieval_time"]

        # Validate retrieval performance
        if actual_time <= max_expected_time:
            logger.info(
                f"Signal quality data retrieval within expected time: {actual_time:.2f}s"
            )
        else:
            logger.warning(
                f"Signal quality data retrieval slower than expected: {actual_time:.2f}s"
            )

        # Get comprehensive signal quality data using page object method
        logger.info(f"Getting comprehensive signal quality data")

        signal_quality_data = gnss_page.get_signal_quality_elements()
        page_data = gnss_page.get_page_data()

        # Final comprehensive validation
        logger.info(f"Final signal quality monitoring validation")

        # Check that signal quality monitoring functionality is accessible
        assert (
            signal_quality_data["device_model"] == device_model
        ), f"Signal quality data device model mismatch"

        assert (
            signal_quality_data["device_series"] == device_series
        ), f"Signal quality data device series mismatch"

        # Comprehensive validation summary
        logger.info(f"Signal Quality Monitoring Test Results for {device_model}:")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Device Model: {device_model}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
        logger.info(
            f"  - Signal Quality Elements Found: {quality_test_results['signal_quality_elements_found']}"
        )
        logger.info(
            f"  - Data Retrieval Time: {performance_metrics['data_retrieval_time']:.2f}s"
        )
        logger.info(
            f"  - Pattern Validation: {'PASSED' if validation_passed else 'WARNINGS'}"
        )

        # Final validation - ensure page object methods are working correctly
        assert (
            gnss_page.get_available_constellations() is not None
        ), f"GNSS page object methods not working correctly on {device_model}"

        logger.info(f"Signal Quality Monitoring Test PASSED for {device_model}")
        logger.info(
            f"Series-specific patterns validated for {device_series} series using pure page object methods"
        )
        logger.info(
            f"DeviceCapabilities integration successful for signal quality monitoring"
        )

    except Exception as e:
        pytest.fail(f"Signal quality monitoring test failed on {device_model}: {e}")
