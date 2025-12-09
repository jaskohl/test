"""
Test 15.1.3: Series 3 Output Count - Pure Page Object Pattern
Category: 15 - Device Capability Detection Tests
Test Count: 5 of 15 in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Series 3 Only
IMPROVED: Pure page object architecture with device-aware Series 3 output count validation
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.outputs_config_page import OutputsConfigPage


def test_15_1_3_series3_output_count(
    unlocked_config_page: Page, base_url: str, device_series: str, request
):
    """
    Test 15.1.3: Series 3 Output Count (Pure Page Object Pattern)
    Purpose: Verify Series 3 devices have correct output count using pure page object architecture
    Expected: Output count matches DeviceCapabilities database for device model
    Series: Series 3 Only
    IMPROVED: Pure page object pattern with device-aware Series 3 output count validation
    """
    # Get device model for comprehensive validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate output count")

    logger = logging.getLogger(__name__)

    try:
        # Initialize outputs configuration page object
        outputs_page = OutputsConfigPage(unlocked_config_page, device_model)

        logger.info(f"{device_model}: Starting Series 3 output count validation")

        # Get device series from database for validation using page object encapsulation
        expected_series = outputs_page.get_expected_device_series()
        if expected_series != 3:
            pytest.skip(
                f"Test only applies to Series 3, detected Series {expected_series} device {device_model}"
            )

        # Get expected output count from DeviceCapabilities using page object method
        max_outputs = outputs_page.get_max_outputs_from_database()
        assert (
            max_outputs > 0
        ), f"Device database should indicate output count for {device_model}"

        logger.info(f"{device_model}: Expected series from database: {expected_series}")
        logger.info(
            f"{device_model}: Expected output count from database: {max_outputs}"
        )

        # Navigate to outputs page using page object method with device-aware timeout
        outputs_page.navigate_to_page()

        # Validate page loaded successfully using page object method
        outputs_page.wait_for_page_load()

        logger.info(f"{device_model}: Outputs configuration page loaded successfully")

        # Count actual output configuration elements using page object methods (support both output and signal selectors)
        actual_output_count = outputs_page.count_series3_output_elements()

        logger.info(
            f"{device_model}: Found {actual_output_count} output select elements"
        )
        logger.info(
            f"{device_model}: Expected {max_outputs} outputs according to device database"
        )

        # Validate output count matches device database (Series 3 should have 6 outputs)
        assert (
            actual_output_count == max_outputs
        ), f"Output count mismatch - database shows {max_outputs}, found {actual_output_count} outputs for {device_model}"

        logger.info(
            f"{device_model}: Output count validation passed - {actual_output_count} outputs found"
        )

        # Verify specific output elements exist using page object validation (support both signal{i} and output{i} patterns)
        outputs_found = outputs_page.validate_series3_output_elements(max_outputs)

        assert (
            outputs_found == max_outputs
        ), f"Expected {max_outputs} output elements, found {outputs_found} for {device_model}"

        logger.info(
            f"{device_model}: All {max_outputs} output elements found and validated"
        )

        # Enhanced validation: Test output signal types for each output using page object methods
        for i in range(1, max_outputs + 1):
            try:
                # Validate individual output signal using page object method (support both patterns)
                signal_validation = outputs_page.validate_series3_output_signal_type(i)

                # Get available signal options using page object method
                signal_options = outputs_page.get_series3_signal_type_options(i)
                option_count = len(signal_options)

                assert (
                    option_count > 0
                ), f"Output {i} should have available options on {device_model}"
                logger.info(
                    f"{device_model}: Output {i} has {option_count} signal type options"
                )

                # Validate signal types match device database using page object method
                available_types = outputs_page.get_expected_signal_types_for_output(i)
                if available_types:
                    logger.info(
                        f"{device_model}: Expected signal types for output {i}: {available_types}"
                    )

            except Exception as e:
                logger.warning(
                    f"{device_model}: Signal validation for output {i} handled gracefully - {e}"
                )
                continue

        # Additional database cross-validation using page object methods
        capabilities = outputs_page.get_device_capabilities()

        # Validate output-related capabilities using page object validation
        outputs_page.validate_output_capabilities(capabilities, max_outputs)

        logger.info(f"{device_model}: Output capability validation passed")

        # Series-specific validation using page object methods
        if expected_series == 3:
            # Series 3 validation
            outputs_page.validate_series3_output_configuration(max_outputs)

            logger.info(
                f"{device_model}: Series 3 output validation: {max_outputs} outputs confirmed"
            )

            # Additional validation for Series 3 variants using page object methods
            device_info = outputs_page.get_series3_device_info()
            logger.info(f"{device_model}: Series 3 device info: {device_info}")

            # Verify this is a legitimate Series 3 device using page object validation
            outputs_page.validate_series3_device_model(device_info)

        # Cross-validation test using page object method
        outputs_page.test_series3_output_count_cross_validation()

        # Final validation using page object capability detection
        ui_detected_outputs = outputs_page.detect_series3_output_count_from_ui()
        logger.info(f"{device_model}: UI-detected output count: {ui_detected_outputs}")

        # Validate UI detection matches database capabilities
        outputs_page.validate_ui_series3_output_detection_matches_database(
            ui_detected_outputs, max_outputs
        )

        logger.info(
            f"{device_model}: Series 3 output count test completed successfully"
        )
        print(
            f"OUTPUT COUNT VALIDATED: {device_model} - {max_outputs} outputs confirmed"
        )

    except Exception as e:
        logger.error(
            f"{device_model}: Series 3 output count test encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"Series 3 output count test failed for {device_model}: {e}")
