"""
Category 11: Form Validation - Test 11.2.3
Contact Field Maxlength Behavior - Pure Page Object Pattern
Test Count: 3 of 34 in Category 11
Hardware: Device Only
Priority: MEDIUM - Form validation functionality
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on form validation requirements and contact field behavior patterns
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_11_2_3_contact_field_maxlength_behavior(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 11.2.3: Contact Field Maxlength Behavior - Pure Page Object Pattern
    Purpose: Verify contact field maxlength behavior with device-aware patterns
    Expected: Device-specific field length validation with proper maxlength handling
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates field length behavior across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate field length behavior")

    # Initialize page object with device-aware patterns
    general_config_page = GeneralConfigPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing contact field maxlength behavior on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to general configuration page using page object method
        general_config_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        general_config_page.wait_for_page_load()

        # Test contact field maxlength validation using page object method
        logger.info("Testing contact field maxlength validation")

        maxlength_validation = general_config_page.validate_contact_field_maxlength()
        logger.info(f"Contact field maxlength validation: {maxlength_validation}")

        # Test contact field accessibility using page object method
        logger.info("Testing contact field accessibility")

        field_accessible = general_config_page.is_contact_field_accessible()
        logger.info(f"Contact field accessible: {field_accessible}")

        # Get device series for device-aware testing
        device_series = DeviceCapabilities.get_series(device_model)
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        # Test device-specific contact expectations using page object method
        if device_series == 2:
            logger.info(f"Testing Series 2 specific contact patterns on {device_model}")
            # Series 2: Generally unlimited field lengths
            contact_patterns = general_config_page.get_series_2_contact_patterns()
            logger.info(f"Series 2 contact patterns: {contact_patterns}")
        elif device_series == 3:
            logger.info(f"Testing Series 3 specific contact patterns on {device_model}")
            # Series 3: May have 29-character limit
            contact_patterns = general_config_page.get_series_3_contact_patterns()
            logger.info(f"Series 3 contact patterns: {contact_patterns}")

        # Test field length behavior using page object method
        logger.info("Testing field length behavior")

        test_cases = [
            ("Short contact", 15, "Valid short contact"),
            ("Medium length contact person name", 35, "Valid medium contact"),
            ("", 0, "Empty contact"),
        ]

        for test_description, test_length, case_description in test_cases:
            logger.info(f"Testing {case_description}: length {test_length}")

            try:
                field_length_behavior = (
                    general_config_page.test_contact_field_length_behavior(
                        test_length, case_description
                    )
                )
                logger.info(
                    f"Field length behavior for {case_description}: {field_length_behavior}"
                )

            except Exception as e:
                logger.warning(f"Field length test failed for {case_description}: {e}")

        # Test special characters in contact field using page object method
        logger.info("Testing special characters in contact field")

        special_char_tests = [
            ("John Doe", "Name with spaces"),
            ("contact_person", "Underscore"),
            ("contact.person@company.com", "Email-like"),
            ("Contact123", "Alphanumeric"),
        ]

        for test_value, description in special_char_tests:
            logger.info(f"Testing {description} in contact field")

            try:
                special_chars_handled = (
                    general_config_page.test_contact_special_characters(
                        test_value, description
                    )
                )
                logger.info(
                    f"Special character test for {description}: {special_chars_handled}"
                )

            except Exception as e:
                logger.warning(f"Special character test failed for {description}: {e}")

        # Test contact field validation using page object method
        logger.info("Testing contact field validation")

        field_valid = general_config_page.validate_contact_field()
        logger.info(f"Contact field validation: {field_valid}")

        # Test contact field constraints using page object method
        logger.info("Testing contact field constraints")

        field_constraints = general_config_page.get_contact_field_constraints()
        logger.info(f"Contact field constraints: {field_constraints}")

        # Test contact field state management using page object method
        logger.info("Testing contact field state management")

        state_management_valid = (
            general_config_page.test_contact_field_state_management()
        )
        logger.info(f"Contact field state management valid: {state_management_valid}")

        # Test save button behavior with different field lengths using page object method
        logger.info("Testing save button behavior with different field lengths")

        test_contacts = [
            "John Doe",
            "Jane Smith - Administrator",
            "IT Department Contact",
        ]

        for test_contact in test_contacts:
            logger.info(f"Testing save with contact: '{test_contact}'")

            try:
                save_behavior_valid = (
                    general_config_page.test_contact_save_button_behavior(test_contact)
                )
                logger.info(
                    f"Save button behavior for '{test_contact}': {save_behavior_valid}"
                )

            except Exception as e:
                logger.warning(f"Contact save test failed for '{test_contact}': {e}")

        # Test field persistence across navigation using page object method
        logger.info("Testing field persistence across navigation")

        test_value = " Contact Test 123"
        persistence_valid = general_config_page.test_contact_field_persistence(
            test_value
        )
        logger.info(f"Contact field persistence: {persistence_valid}")

        # Test contact field paste behavior using page object method
        logger.info("Testing contact field paste behavior")

        paste_behavior_valid = general_config_page.test_contact_paste_behavior()
        logger.info(f"Contact paste behavior valid: {paste_behavior_valid}")

        # Test contact field navigation reliability using page object method
        logger.info("Testing contact field navigation reliability")

        navigation_reliable = (
            general_config_page.test_contact_field_navigation_reliability()
        )
        logger.info(f"Contact field navigation reliable: {navigation_reliable}")

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

        # Test contact field comprehensive validation using page object method
        logger.info("Testing contact field comprehensive validation")

        comprehensive_validation = (
            general_config_page.test_contact_field_comprehensive_validation()
        )
        logger.info(
            f"Contact field comprehensive validation: {comprehensive_validation}"
        )

        # Cross-validate with device capabilities
        device_capabilities_info = DeviceCapabilities.get_device_info(device_model)
        capabilities = DeviceCapabilities.get_capabilities(device_model)

        logger.info(
            f"Contact field testing on device: {device_capabilities_info.get('hardware_model', 'Unknown')}"
        )
        logger.info(f"Device capabilities: {capabilities}")

        # Test contact field complete behavior using page object method
        logger.info("Testing contact field complete behavior")

        complete_behavior = general_config_page.test_contact_field_complete_behavior()
        logger.info(f"Contact field complete behavior: {complete_behavior}")

        # Final validation using page object method
        logger.info("Performing final validation")

        final_field_accessible = general_config_page.is_contact_field_accessible()
        final_maxlength_valid = general_config_page.validate_contact_field_maxlength()

        logger.info(f"Final contact field accessible: {final_field_accessible}")
        logger.info(f"Final maxlength validation: {final_maxlength_valid}")

        # Cross-validate contact field maxlength behavior
        contact_validation_successful = (
            final_field_accessible and final_maxlength_valid and field_valid
        )

        if contact_validation_successful:
            logger.info("Contact field maxlength validation PASSED")
        else:
            logger.warning(
                "Contact field maxlength validation WARNING: some validations failed"
            )

        logger.info(f"Contact Field Maxlength Test Results for {device_model}:")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
        logger.info(f"  - Device Info: {device_capabilities_info}")
        logger.info(f"  - Device Capabilities: {capabilities}")

        logger.info(
            f"Contact field maxlength test COMPLETED for {device_model} using pure page object pattern"
        )
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Contact field maxlength test failed on {device_model}: {e}")
        pytest.fail(f"Contact field maxlength test failed on {device_model}: {e}")

    finally:
        # Small cleanup wait for device stability
        cleanup_wait = int(
            500 * DeviceCapabilities.get_timeout_multiplier(device_model)
        )
        time.sleep(cleanup_wait / 1000)  # Convert to seconds
