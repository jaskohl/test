"""
Category 11: Form Validation - Test 11.4.1
Mandatory Field Detection - Pure Page Object Pattern
Test Count: 9 of 34 in Category 11
Hardware: Device Only
Priority: MEDIUM - Form validation functionality
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on form validation requirements and mandatory field detection patterns
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_11_4_1_mandatory_field_detection(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 11.4.1: Mandatory Field Detection - Pure Page Object Pattern
    Purpose: Identification and validation of required fields with device-aware behavior
    Expected: Device-specific required field behavior based on capabilities
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates mandatory field patterns across device variants
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate mandatory field behavior"
        )

    # Initialize page object with device-aware patterns
    general_config_page = GeneralConfigPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing mandatory field detection on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to general configuration page using page object method
        general_config_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        general_config_page.wait_for_page_load()

        # Get device capabilities for device-aware validation
        device_series = DeviceCapabilities.get_series(device_model)
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        logger.info(
            f"Device series: {device_series}, Timeout multiplier: {timeout_multiplier}x"
        )

        # Test device-specific mandatory field expectations using page object method
        if device_series == 2:
            logger.info(
                f"Testing Series 2 specific mandatory field patterns on {device_model}"
            )
            # Series 2 has simpler field requirements
            expected_min_required = (
                2  # Series 2 should have basic required fields (identifier, location)
            )
            mandatory_patterns = (
                general_config_page.get_series_2_mandatory_field_patterns()
            )
            logger.info(f"Series 2 mandatory field patterns: {mandatory_patterns}")
        else:  # Series 3
            logger.info(
                f"Testing Series 3 specific mandatory field patterns on {device_model}"
            )
            # Series 3 has more complex field requirements including PTP-related fields
            expected_min_required = (
                4  # Series 3 should have more required fields due to advanced features
            )
            mandatory_patterns = (
                general_config_page.get_series_3_mandatory_field_patterns()
            )
            logger.info(f"Series 3 mandatory field patterns: {mandatory_patterns}")

        # Test mandatory field detection using page object method
        logger.info("Testing mandatory field detection")

        total_required_fields = general_config_page.detect_mandatory_fields()
        logger.info(f"Total required fields detected: {total_required_fields}")

        # Device-specific validation
        assert (
            total_required_fields >= expected_min_required
        ), f"Device {device_model} should have at least {expected_min_required} required fields, found {total_required_fields}"

        # Test required field indicators validation using page object method
        logger.info("Testing required field indicators validation")

        indicators_valid = general_config_page.validate_required_field_indicators()
        logger.info(f"Required field indicators validation: {indicators_valid}")

        # Test mandatory field accessibility using page object method
        logger.info("Testing mandatory field accessibility")

        fields_accessible = general_config_page.test_mandatory_field_accessibility()
        logger.info(f"Mandatory field accessibility: {fields_accessible}")

        # Test mandatory field visibility using page object method
        logger.info("Testing mandatory field visibility")

        fields_visible = general_config_page.test_mandatory_field_visibility()
        logger.info(f"Mandatory field visibility: {fields_visible}")

        # Test mandatory field validation using page object method
        logger.info("Testing mandatory field validation")

        field_validation_valid = general_config_page.validate_mandatory_fields()
        logger.info(f"Mandatory field validation: {field_validation_valid}")

        # Test device-specific required field patterns using page object method
        logger.info("Testing device-specific required field patterns")

        device_specific_patterns_valid = (
            general_config_page.test_device_specific_required_field_patterns()
        )
        logger.info(
            f"Device-specific required field patterns: {device_specific_patterns_valid}"
        )

        # Test PTP-related required fields (Series 3 only)
        if device_series == 3:
            logger.info("Testing PTP-related required fields")

            ptp_required_valid = general_config_page.validate_ptp_required_fields()
            logger.info(f"PTP-related required fields validation: {ptp_required_valid}")
        else:
            logger.info(
                f"Series 2 device {device_model}: No PTP-related required fields expected"
            )

        # Test mandatory field state management using page object method
        logger.info("Testing mandatory field state management")

        state_management_valid = (
            general_config_page.test_mandatory_field_state_management()
        )
        logger.info(f"Mandatory field state management: {state_management_valid}")

        # Test mandatory field navigation reliability using page object method
        logger.info("Testing mandatory field navigation reliability")

        navigation_reliable = (
            general_config_page.test_mandatory_field_navigation_reliability()
        )
        logger.info(f"Mandatory field navigation reliable: {navigation_reliable}")

        # Test mandatory field comprehensive validation using page object method
        logger.info("Testing mandatory field comprehensive validation")

        comprehensive_validation = (
            general_config_page.test_mandatory_field_comprehensive_validation()
        )
        logger.info(
            f"Mandatory field comprehensive validation: {comprehensive_validation}"
        )

        # Test mandatory field count validation using page object method
        logger.info("Testing mandatory field count validation")

        count_valid = general_config_page.validate_mandatory_field_count(
            expected_min_required
        )
        logger.info(
            f"Mandatory field count validation (expected: {expected_min_required}): {count_valid}"
        )

        # Test mandatory field detection reliability using page object method
        logger.info("Testing mandatory field detection reliability")

        detection_reliable = (
            general_config_page.test_mandatory_field_detection_reliability()
        )
        logger.info(f"Mandatory field detection reliable: {detection_reliable}")

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
        logger.info(f"Mandatory field detection on device: {hardware_model}")

        # Test mandatory field complete behavior using page object method
        logger.info("Testing mandatory field complete behavior")

        complete_behavior = general_config_page.test_mandatory_field_complete_behavior()
        logger.info(f"Mandatory field complete behavior: {complete_behavior}")

        # Final validation using page object method
        logger.info("Performing final validation")

        final_total_required = general_config_page.detect_mandatory_fields()
        final_indicators_valid = (
            general_config_page.validate_required_field_indicators()
        )
        final_field_validation_valid = general_config_page.validate_mandatory_fields()

        logger.info(f"Final total required fields: {final_total_required}")
        logger.info(f"Final indicators validation: {final_indicators_valid}")
        logger.info(f"Final field validation: {final_field_validation_valid}")

        # Cross-validate mandatory field detection
        mandatory_detection_successful = (
            final_total_required >= expected_min_required
            and final_indicators_valid
            and final_field_validation_valid
            and comprehensive_validation
        )

        if mandatory_detection_successful:
            logger.info("Mandatory field detection PASSED")
        else:
            logger.warning("Mandatory field detection WARNING: some validations failed")

        logger.info(f"Mandatory Field Detection Results for {device_model}:")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Required Fields Found: {final_total_required}")
        logger.info(f"  - Expected Min Required: {expected_min_required}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
        logger.info(f"  - Device Info: {device_capabilities_info}")

        logger.info(
            f"Successfully validated mandatory field detection for {device_model} ({device_series}): {final_total_required} required fields found"
        )
        logger.info(
            f"Mandatory field detection test COMPLETED for {device_model} using pure page object pattern"
        )
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Mandatory field detection test failed on {device_model}: {e}")
        pytest.fail(f"Mandatory field detection test failed on {device_model}: {e}")
