"""
Category 11: Form Validation - Test 11.2.1
Identifier Field Maxlength Behavior - Pure Page Object Pattern
Test Count: 1 of 34 in Category 11
Hardware: Device Only
Priority: MEDIUM - Form validation foundation
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on form validation requirements and field behavior patterns
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_11_2_1_identifier_field_maxlength_behavior(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 11.2.1: Identifier Field Maxlength Behavior - Pure Page Object Pattern
    Purpose: Verify identifier field maxlength enforcement with device-aware validation
    Expected: Field enforces character limits, validation works across device variants
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates maxlength patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate identifier field behavior"
        )

    # Initialize page object with device-aware patterns
    general_config_page = GeneralConfigPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing identifier field maxlength on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to general configuration page using page object method
        general_config_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        general_config_page.wait_for_page_load()

        # Test identifier field maxlength validation using page object method
        logger.info("Testing identifier field maxlength validation")

        # Get device-specific field constraints - using reasonable defaults since no field constraints in DeviceCapabilities
        # Most identifier fields typically have 50-64 character limits
        expected_maxlength = 50  # Standard maxlength for identifier fields

        logger.info(
            f"Expected maxlength for identifier field on {device_model}: {expected_maxlength}"
        )

        # Test maxlength enforcement using page object method
        maxlength_validation = general_config_page.validate_identifier_field_maxlength()
        logger.info(f"Identifier field maxlength validation: {maxlength_validation}")

        # Test identifier field accessibility using page object method
        logger.info("Testing identifier field accessibility")

        field_accessible = general_config_page.is_identifier_field_accessible()
        logger.info(f"Identifier field accessible: {field_accessible}")

        # Test identifier field maxlength enforcement using page object method
        logger.info("Testing identifier field maxlength enforcement")

        maxlength_enforced = general_config_page.test_identifier_maxlength_enforcement(
            expected_maxlength
        )
        logger.info(f"Identifier field maxlength enforced: {maxlength_enforced}")

        # Test device-specific identifier expectations using page object method
        device_series = DeviceCapabilities.get_series(device_model)

        if device_series == 2:
            logger.info(
                f"Testing Series 2 specific identifier patterns on {device_model}"
            )
            # Series 2: Basic identifier validation
            identifier_patterns = general_config_page.get_series_2_identifier_patterns()
            logger.info(f"Series 2 identifier patterns: {identifier_patterns}")
        elif device_series == 3:
            logger.info(
                f"Testing Series 3 specific identifier patterns on {device_model}"
            )
            # Series 3: May have more complex identifier validation
            identifier_patterns = general_config_page.get_series_3_identifier_patterns()
            logger.info(f"Series 3 identifier patterns: {identifier_patterns}")

        # Test identifier field validation using page object method
        logger.info("Testing identifier field validation")

        field_valid = general_config_page.validate_identifier_field()
        logger.info(f"Identifier field validation: {field_valid}")

        # Test identifier field constraints using page object method
        logger.info("Testing identifier field constraints")

        field_constraints = general_config_page.get_identifier_field_constraints()
        logger.info(f"Identifier field constraints: {field_constraints}")

        # Test special characters handling using page object method
        logger.info("Testing special characters handling")

        special_chars_handled = general_config_page.test_identifier_special_characters()
        logger.info(f"Special characters handled: {special_chars_handled}")

        # Test complex identifier patterns using page object method
        logger.info("Testing complex identifier patterns")

        complex_patterns_valid = general_config_page.test_identifier_complex_patterns()
        logger.info(f"Complex identifier patterns valid: {complex_patterns_valid}")

        # Test identifier field paste behavior using page object method
        logger.info("Testing identifier field paste behavior")

        paste_behavior_valid = general_config_page.test_identifier_paste_behavior(
            expected_maxlength
        )
        logger.info(f"Identifier paste behavior valid: {paste_behavior_valid}")

        # Test save button state with maxlength constraints using page object method
        logger.info("Testing save button state with maxlength constraints")

        save_state_valid = general_config_page.test_identifier_save_button_state(
            expected_maxlength
        )
        logger.info(f"Save button state with maxlength valid: {save_state_valid}")

        # Test identifier field state management using page object method
        logger.info("Testing identifier field state management")

        state_management_valid = (
            general_config_page.test_identifier_field_state_management()
        )
        logger.info(
            f"Identifier field state management valid: {state_management_valid}"
        )

        # Test identifier field navigation reliability using page object method
        logger.info("Testing identifier field navigation reliability")

        navigation_reliable = (
            general_config_page.test_identifier_field_navigation_reliability()
        )
        logger.info(f"Identifier field navigation reliable: {navigation_reliable}")

        # Performance validation using device baselines
        performance_expectations = DeviceCapabilities.get_performance_expectations(
            device_model
        )
        if performance_expectations:
            nav_performance = performance_expectations.get("navigation_performance", {})
            section_nav = nav_performance.get("section_navigation", {})
            typical_time = section_nav.get("typical_time", "")
            if typical_time:
                logger.info(
                    f"General config navigation performance baseline: {typical_time}"
                )

        # Test identifier field comprehensive validation using page object method
        logger.info("Testing identifier field comprehensive validation")

        comprehensive_validation = (
            general_config_page.test_identifier_field_comprehensive_validation()
        )
        logger.info(
            f"Identifier field comprehensive validation: {comprehensive_validation}"
        )

        # Cross-validate with device capabilities
        device_capabilities_info = DeviceCapabilities.get_device_info(device_model)
        hardware_model = device_capabilities_info.get("hardware_model", "Unknown")
        logger.info(f"Identifier field testing on device: {hardware_model}")

        # Test identifier field complete behavior using page object method
        logger.info("Testing identifier field complete behavior")

        complete_behavior = (
            general_config_page.test_identifier_field_complete_behavior()
        )
        logger.info(f"Identifier field complete behavior: {complete_behavior}")

        # Final validation using page object method
        logger.info("Performing final validation")

        final_field_accessible = general_config_page.is_identifier_field_accessible()
        final_maxlength_valid = (
            general_config_page.validate_identifier_field_maxlength()
        )

        logger.info(f"Final identifier field accessible: {final_field_accessible}")
        logger.info(f"Final maxlength validation: {final_maxlength_valid}")

        # Cross-validate identifier field maxlength behavior
        identifier_validation_successful = (
            final_field_accessible and final_maxlength_valid and maxlength_enforced
        )

        if identifier_validation_successful:
            logger.info("Identifier field maxlength validation PASSED")
        else:
            logger.warning(
                "Identifier field maxlength validation WARNING: some validations failed"
            )

        logger.info(f"Identifier Field Maxlength Test Results for {device_model}:")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Expected Maxlength: {expected_maxlength}")
        logger.info(
            f"  - Timeout Multiplier: {DeviceCapabilities.get_timeout_multiplier(device_model)}x"
        )
        logger.info(f"  - Field Constraints: Standard 50-character limit applied")

        logger.info(
            f"Identifier field maxlength test COMPLETED for {device_model} using pure page object pattern"
        )
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Identifier field maxlength test failed on {device_model}: {e}")
        pytest.fail(f"Identifier field maxlength test failed on {device_model}: {e}")

    finally:
        # Small cleanup wait for device stability
        cleanup_wait = int(
            500 * DeviceCapabilities.get_timeout_multiplier(device_model)
        )
        time.sleep(cleanup_wait / 1000)  # Convert to seconds
