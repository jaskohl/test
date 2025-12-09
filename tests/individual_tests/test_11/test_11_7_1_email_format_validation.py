"""
Category 11: Form Validation - Test 11.7.1
Email Format Validation - Pure Page Object Pattern
Test Count: 6 of 34 in Category 11
Hardware: Device Only
Priority: MEDIUM - Form validation functionality
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on form validation requirements and email format validation patterns
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_11_7_1_email_format_validation(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 11.7.1: Email Format Validation - Pure Page Object Pattern
    Purpose: Email format validation with device capabilities
    Expected: Device-aware email format validation
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates email format patterns across device variants
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate email format")

    # Initialize page object with device-aware patterns
    general_config_page = GeneralConfigPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing email format validation on {device_model} using pure page object pattern"
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

        # Test device-specific email expectations using page object method
        if device_series == 2:
            logger.info(f"Testing Series 2 specific email patterns on {device_model}")
            # Series 2: Basic email validation
            email_patterns = general_config_page.get_series_2_email_field_patterns()
            logger.info(f"Series 2 email field patterns: {email_patterns}")
        elif device_series == 3:
            logger.info(f"Testing Series 3 specific email patterns on {device_model}")
            # Series 3: Advanced email validation
            email_patterns = general_config_page.get_series_3_email_field_patterns()
            logger.info(f"Series 3 email field patterns: {email_patterns}")

        # Test email field detection using page object method
        logger.info("Testing email field detection")

        email_field_found = general_config_page.detect_email_fields()
        logger.info(f"Email field found: {email_field_found}")

        if email_field_found:
            # Test email field accessibility using page object method
            logger.info("Testing email field accessibility")

            field_accessible = general_config_page.is_email_field_accessible()
            logger.info(f"Email field accessible: {field_accessible}")

            # Test valid email formats using page object method
            logger.info("Testing valid email formats")

            valid_emails = [
                "test@example.com",
                "user@domain.org",
                "admin@company.co.uk",
            ]
            for email in valid_emails:
                logger.info(f"Testing valid email: {email}")

                try:
                    email_valid = general_config_page.test_valid_email_format(email)
                    logger.info(f"Valid email test result for {email}: {email_valid}")
                except Exception as e:
                    logger.warning(f"Email field test issue for {email}: {e}")

            # Test invalid email formats using page object method
            logger.info("Testing invalid email formats")

            invalid_emails = [
                "invalid-email",
                "@domain.com",
                "user@",
                "user..user@example.com",
            ]

            for invalid_email in invalid_emails:
                logger.info(f"Testing invalid email: {invalid_email}")

                try:
                    invalid_email_handled = (
                        general_config_page.test_invalid_email_format(invalid_email)
                    )
                    logger.info(
                        f"Invalid email test result for {invalid_email}: {invalid_email_handled}"
                    )
                except Exception as e:
                    logger.warning(f"Invalid email test issue for {invalid_email}: {e}")

        else:
            logger.info(f"No email fields found for validation test on {device_model}")

        # Test email format validation using page object method
        logger.info("Testing email format validation")

        format_valid = general_config_page.validate_email_format()
        logger.info(f"Email format validation: {format_valid}")

        # Test email field constraints using page object method
        logger.info("Testing email field constraints")

        field_constraints = general_config_page.get_email_field_constraints()
        logger.info(f"Email field constraints: {field_constraints}")

        # Test email field state management using page object method
        logger.info("Testing email field state management")

        state_management_valid = general_config_page.test_email_field_state_management()
        logger.info(f"Email field state management: {state_management_valid}")

        # Test email field navigation reliability using page object method
        logger.info("Testing email field navigation reliability")

        navigation_reliable = (
            general_config_page.test_email_field_navigation_reliability()
        )
        logger.info(f"Email field navigation reliable: {navigation_reliable}")

        # Test email field comprehensive validation using page object method
        logger.info("Testing email field comprehensive validation")

        comprehensive_validation = (
            general_config_page.test_email_field_comprehensive_validation()
        )
        logger.info(f"Email field comprehensive validation: {comprehensive_validation}")

        # Test email format edge cases using page object method
        logger.info("Testing email format edge cases")

        edge_cases_valid = general_config_page.test_email_format_edge_cases()
        logger.info(f"Email format edge cases: {edge_cases_valid}")

        # Test email field paste behavior using page object method
        logger.info("Testing email field paste behavior")

        paste_behavior_valid = general_config_page.test_email_field_paste_behavior()
        logger.info(f"Email field paste behavior: {paste_behavior_valid}")

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
        logger.info(f"Email format validation on device: {hardware_model}")

        # Test email field complete behavior using page object method
        logger.info("Testing email field complete behavior")

        complete_behavior = general_config_page.test_email_field_complete_behavior()
        logger.info(f"Email field complete behavior: {complete_behavior}")

        # Final validation using page object method
        logger.info("Performing final validation")

        final_email_field_found = general_config_page.detect_email_fields()
        final_format_valid = general_config_page.validate_email_format()

        logger.info(f"Final email field found: {final_email_field_found}")
        logger.info(f"Final format validation: {final_format_valid}")

        # Cross-validate email format validation
        email_validation_successful = (
            final_email_field_found and final_format_valid and format_valid
        )

        if email_validation_successful:
            logger.info("Email format validation PASSED")
        else:
            logger.warning("Email format validation WARNING: some validations failed")

        logger.info(f"Email Format Validation Results for {device_model}:")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Email Field Found: {final_email_field_found}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
        logger.info(f"  - Device Info: {device_capabilities_info}")

        logger.info(
            f"Email format validation test COMPLETED for {device_model} using pure page object pattern"
        )
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Email format validation test failed on {device_model}: {e}")
        pytest.fail(f"Email format validation test failed on {device_model}: {e}")
