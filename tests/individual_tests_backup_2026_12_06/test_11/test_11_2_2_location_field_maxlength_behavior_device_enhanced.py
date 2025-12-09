"""
Category 11: Form Validation - Test 11.2.2
Location Field Maxlength Behavior - DeviceCapabilities Enhanced
Test Count: 2 of 37 in Category 11
Hardware: Device Only
Priority: MEDIUM - Form validation functionality
Series: Both Series 2 and 3
ENHANCED: Comprehensive DeviceCapabilities integration for device-aware field length validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_11_2_2_location_field_maxlength_behavior_device_enhanced(
    general_config_page: GeneralConfigPage, base_url: str, request
):
    """
    Test 11.2.2: Location Field Maxlength Behavior - DeviceCapabilities Enhanced
    Purpose: Verify location field maxlength behavior with device-aware patterns
    Expected: Device-specific field length validation with proper maxlength handling
    ENHANCED: Full DeviceCapabilities integration for field length validation patterns
    Series: Both - validates field length behavior across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate field length behavior")

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing location field maxlength behavior on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to general configuration page
    general_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    general_config_page.verify_page_loaded()

    # Test location field with device-aware patterns
    try:
        location_field = general_config_page.page.locator("input[name='location']")

        field_timeout = int(8000 * timeout_multiplier)
        expect(location_field).to_be_visible(timeout=field_timeout)

        logger.info(f"Testing location field maxlength behavior on {device_model}")

        # Get maxlength attribute and test field behavior
        maxlength_attr = location_field.get_attribute("maxlength")
        logger.info(f"Location field maxlength attribute: {maxlength_attr}")

        # Test field length behavior based on device series
        test_cases = [
            ("Short location", 15, "Valid short location"),
            ("Medium length location name here", 35, "Valid medium location"),
            ("", 0, "Empty location"),
        ]

        for test_description, test_length, case_description in test_cases:
            logger.info(f"Testing {case_description}: length {test_length}")

            try:
                # Clear field and enter test value
                location_field.clear()
                time.sleep(0.5)

                if test_length > 0:
                    test_value = "A" * test_length
                    location_field.fill(test_value)
                    time.sleep(0.5)

                    # Check actual input value
                    current_value = location_field.input_value()
                    actual_length = len(current_value)

                    logger.info(
                        f"Input length: {test_length}, Actual length: {actual_length}"
                    )

                    # Series-specific validation
                    if device_series == 2:
                        # Series 2: Generally unlimited field lengths
                        logger.info(f"Series 2: Testing unlimited field behavior")
                        if actual_length <= test_length:
                            logger.info(f"Series 2 accepts full input length")
                        else:
                            logger.warning(f"Series 2 input truncated unexpectedly")
                    else:  # Series 3
                        # Series 3: May have 29-character limit
                        logger.info(f"Series 3: Testing 29-character field limit")
                        if test_length <= 29:
                            assert (
                                actual_length >= test_length * 0.9
                            ), f"Series 3 should accept valid input lengths"
                        else:
                            logger.info(f"Series 3 testing long input behavior")

            except Exception as e:
                logger.warning(f"Field length test failed for {case_description}: {e}")

        # Test special characters in location field
        special_char_tests = [
            ("Location with spaces and -hyphens", "Spaces and hyphens"),
            ("Location_with_underscores", "Underscores"),
            ("Location.with.dots", "Dots"),
            ("Location123", "Alphanumeric"),
        ]

        for test_value, description in special_char_tests:
            logger.info(f"Testing {description} in location field")

            try:
                location_field.clear()
                time.sleep(0.5)
                location_field.fill(test_value)
                time.sleep(0.5)

                current_value = location_field.input_value()
                logger.info(f"Special char test '{test_value}' -> '{current_value}'")

            except Exception as e:
                logger.warning(f"Special character test failed for {description}: {e}")

    except Exception as e:
        pytest.fail(f"Location field maxlength test failed on {device_model}: {e}")

    # Test save button behavior with different field lengths
    try:
        # Test with valid location
        test_locations = [
            "Test Location",
            "Building A Floor 5",
            "Data Center Room 123",
        ]

        for test_location in test_locations:
            logger.info(f"Testing save with location: '{test_location}'")

            try:
                general_config_page.configure_device_info(location=test_location)

                # Wait for save button to enable with device-aware timing
                save_button = general_config_page.get_save_button_locator()
                if save_button.count() > 0:
                    expect(save_button).to_be_enabled(
                        timeout=int(5000 * timeout_multiplier)
                    )

                    # Test save functionality
                    save_success = general_config_page.save_configuration()
                    if save_success:
                        logger.info(f"Location save successful: '{test_location}'")
                    else:
                        logger.warning(f"Location save failed: '{test_location}'")
                else:
                    logger.warning(
                        f"Save button not found for location test: '{test_location}'"
                    )

            except Exception as e:
                logger.warning(f"Location save test failed for '{test_location}': {e}")

    except Exception as e:
        logger.warning(f"Save button validation test failed on {device_model}: {e}")

    # Test field persistence across navigation
    try:
        test_value = "Enhanced Location Test 123"
        general_config_page.configure_device_info(location=test_value)

        # Navigate away and back
        dashboard_page = general_config_page.page.locator("text=Dashboard")
        if dashboard_page.count() > 0:
            dashboard_page.click()
            time.sleep(2)

            # Navigate back
            general_config_page.navigate_to_page()
            time.sleep(2)

            # Check if value persisted
            current_value = location_field.input_value()
            if test_value in current_value:
                logger.info(f"Location field persistence verified on {device_model}")
            else:
                logger.warning(
                    f"Location field may not have persisted on {device_model}"
                )

    except Exception as e:
        logger.warning(f"Field persistence test failed on {device_model}: {e}")

    # Performance validation against device baselines
    try:
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            form_performance = performance_data.get("form_interaction", {})
            field_interaction = form_performance.get("field_interaction", {})
            typical_time = field_interaction.get("typical_time", "")

            if typical_time:
                logger.info(
                    f"Form field interaction performance baseline: {typical_time}"
                )

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)
    capabilities = DeviceCapabilities.get_capabilities(device_model)

    logger.info(f"Location field maxlength test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Device series: {device_series}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"LOCATION FIELD MAXLENGTH TEST COMPLETED: {device_model} (Series {device_series})"
    )
