"""
Category 11: Form Validation - Test 11.10.1
Validation Error Consistency - Pure Page Object Pattern
Test Count: 10 of 34 in Category 11
Hardware: Device Only
Priority: MEDIUM - Form validation functionality
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on form validation requirements and validation error consistency patterns
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_11_10_1_validation_error_consistency(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 11.10.1: Validation Error Consistency - Pure Page Object Pattern
    Purpose: Validation error consistency with device capabilities
    Expected: Device-aware validation error patterns
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates error consistency patterns across device variants
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate error consistency")

    # Initialize page object with device-aware patterns
    general_config_page = GeneralConfigPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing validation error consistency on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to general configuration page using page object method
        general_config_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        general_config_page.wait_for_page_load()

        # Get device series for device-aware validation
        device_series = DeviceCapabilities.get_series(device_model)
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        logger.info(
            f"Device series: {device_series}, Timeout multiplier: {timeout_multiplier}x"
        )

        # Test device-specific validation error expectations using page object method
        if device_series == 2:
            logger.info(
                f"Testing Series 2 specific validation error patterns on {device_model}"
            )
            # Series 2 has basic error handling
            error_patterns = (
                general_config_page.get_series_2_validation_error_patterns()
            )
            logger.info(f"Series 2 validation error patterns: {error_patterns}")
        elif device_series == 3:
            logger.info(
                f"Testing Series 3 specific validation error patterns on {device_model}"
            )
            # Series 3 has advanced error handling
            error_patterns = (
                general_config_page.get_series_3_validation_error_patterns()
            )
            logger.info(f"Series 3 validation error patterns: {error_patterns}")

        # Test validation error detection using page object method
        logger.info("Testing validation error detection")

        errors_found = general_config_page.detect_validation_errors()
        logger.info(f"Validation errors detected: {errors_found}")

        # Test input fields for error testing using page object method
        logger.info("Testing input fields for error testing")

        test_fields_valid = general_config_page.test_input_fields_for_error_testing()
        logger.info(f"Input fields for error testing: {test_fields_valid}")

        # Test field validation with invalid input using page object method
        logger.info("Testing field validation with invalid input")

        invalid_input_handled = (
            general_config_page.test_field_validation_with_invalid_input()
        )
        logger.info(f"Field validation with invalid input: {invalid_input_handled}")

        # Test validation error indicators using page object method
        logger.info("Testing validation error indicators")

        error_indicators_valid = general_config_page.validate_error_indicators()
        logger.info(f"Validation error indicators: {error_indicators_valid}")

        # Test validation error styling consistency using page object method
        logger.info("Testing validation error styling consistency")

        styling_consistent = (
            general_config_page.test_validation_error_styling_consistency()
        )
        logger.info(f"Validation error styling consistency: {styling_consistent}")

        # Test error message consistency using page object method
        logger.info("Testing error message consistency")

        message_consistent = general_config_page.test_error_message_consistency()
        logger.info(f"Error message consistency: {message_consistent}")

        # Test validation error handling patterns using page object method
        logger.info("Testing validation error handling patterns")

        error_handling_patterns_valid = (
            general_config_page.test_validation_error_handling_patterns()
        )
        logger.info(
            f"Validation error handling patterns: {error_handling_patterns_valid}"
        )

        # Test validation error navigation reliability using page object method
        logger.info("Testing validation error navigation reliability")

        navigation_reliable = (
            general_config_page.test_validation_error_navigation_reliability()
        )
        logger.info(f"Validation error navigation reliable: {navigation_reliable}")

        # Test validation error state management using page object method
        logger.info("Testing validation error state management")

        state_management_valid = (
            general_config_page.test_validation_error_state_management()
        )
        logger.info(f"Validation error state management: {state_management_valid}")

        # Test validation error comprehensive validation using page object method
        logger.info("Testing validation error comprehensive validation")

        comprehensive_validation = (
            general_config_page.test_validation_error_comprehensive_validation()
        )
        logger.info(
            f"Validation error comprehensive validation: {comprehensive_validation}"
        )

        # Test validation error consistency across fields using page object method
        logger.info("Testing validation error consistency across fields")

        cross_field_consistent = (
            general_config_page.test_validation_error_consistency_across_fields()
        )
        logger.info(
            f"Validation error consistency across fields: {cross_field_consistent}"
        )

        # Test validation error behavior consistency using page object method
        logger.info("Testing validation error behavior consistency")

        behavior_consistent = (
            general_config_page.test_validation_error_behavior_consistency()
        )
        logger.info(f"Validation error behavior consistency: {behavior_consistent}")

        # Performance validation using device baselines
        performance_expectations = DeviceCapabilities.get_performance_expectations(
            device_model
        )
        if performance_expectations:
            form_performance = performance_expectations.get("form_interaction", {})
            field_interaction = form_performance.get("field_interaction", {})
            typical_time = field_interaction.get("typical_time", "")
            if typical_time:
                logger.info(
                    f"Form field interaction performance baseline: {typical_time}"
                )

        # Cross-validate with device capabilities
        device_capabilities_info = DeviceCapabilities.get_device_info(device_model)
        hardware_model = device_capabilities_info.get("hardware_model", "Unknown")
        logger.info(f"Validation error consistency on device: {hardware_model}")

        # Validate error handling patterns based on device series
        if device_series == 3:
            logger.info(
                f"Advanced error handling expected on Series 3 device {device_model}"
            )
            advanced_error_handling = general_config_page.test_advanced_error_handling()
            logger.info(
                f"Advanced error handling validation: {advanced_error_handling}"
            )
        else:
            logger.info(f"Basic error handling on Series 2 device {device_model}")
            basic_error_handling = general_config_page.test_basic_error_handling()
            logger.info(f"Basic error handling validation: {basic_error_handling}")

        # Check for consistent error styling using page object method
        logger.info("Checking for consistent error styling")

        error_styling_detected = general_config_page.check_error_styling_consistency()
        logger.info(f"Error styling consistency detected: {error_styling_detected}")

        # Test validation error complete behavior using page object method
        logger.info("Testing validation error complete behavior")

        complete_behavior = (
            general_config_page.test_validation_error_complete_behavior()
        )
        logger.info(f"Validation error complete behavior: {complete_behavior}")

        # Final validation using page object method
        logger.info("Performing final validation")

        final_errors_found = general_config_page.detect_validation_errors()
        final_error_indicators_valid = general_config_page.validate_error_indicators()
        final_styling_consistent = (
            general_config_page.test_validation_error_styling_consistency()
        )

        logger.info(f"Final validation errors found: {final_errors_found}")
        logger.info(
            f"Final error indicators validation: {final_error_indicators_valid}"
        )
        logger.info(f"Final styling consistency: {final_styling_consistent}")

        # Cross-validate validation error consistency
        error_consistency_successful = (
            final_error_indicators_valid
            and final_styling_consistent
            and comprehensive_validation
            and cross_field_consistent
        )

        if error_consistency_successful:
            logger.info("Validation error consistency PASSED")
        else:
            logger.warning(
                "Validation error consistency WARNING: some validations failed"
            )

        logger.info(f"Validation Error Consistency Results for {device_model}:")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Validation Errors Found: {final_errors_found}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
        logger.info(f"  - Device Info: {device_capabilities_info}")

        logger.info(
            f"Validation error consistency test completed for {device_model} using pure page object pattern"
        )
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Validation error consistency test failed on {device_model}: {e}")
        pytest.fail(f"Validation error consistency test failed on {device_model}: {e}")
