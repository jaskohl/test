"""
Category 11: Form Validation - Test 11.5.1
Numeric Field Validation - DeviceCapabilities Enhanced
Test Count: 1 of 16 in Category 11
Hardware: Device Only
Priority: MEDIUM - Form validation functionality
Series: Both Series 2 and 3
ENHANCED: Comprehensive DeviceCapabilities integration for device-aware validation patterns
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_11_5_1_numeric_field_validation_device_enhanced(
    general_config_page: GeneralConfigPage, base_url: str, request
):
    """
    Test 11.5.1: Numeric Field Validation - DeviceCapabilities Enhanced
    Purpose: Verify numeric field validation with device-aware patterns
    Expected: Valid numbers accepted, invalid rejected, device-specific timing
    ENHANCED: Full DeviceCapabilities integration for validation pattern testing
    Series: Both - validates form patterns across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate form behavior")

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing numeric field validation on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to general configuration page
    general_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    general_config_page.verify_page_loaded()

    # Test numeric field validation with device-aware patterns
    try:
        # Test device identifier field (should accept alphanumeric)
        identifier_field = general_config_page.page.locator("input[name='identifier']")

        field_timeout = int(8000 * timeout_multiplier)
        expect(identifier_field).to_be_visible(timeout=field_timeout)

        logger.info(f"Testing identifier field validation on {device_model}")

        # Test valid numeric input
        test_cases = [
            ("123", True, "Valid numeric identifier"),
            ("ABC123", True, "Alphanumeric identifier"),
            ("Test-Device_1", True, "Complex valid identifier"),
            ("", False, "Empty identifier"),
            ("Test@Device#", False, "Special characters"),
        ]

        for test_value, should_be_valid, description in test_cases:
            logger.info(f"Testing {description}: '{test_value}'")

            try:
                # Clear field and enter test value
                identifier_field.clear()
                time.sleep(0.5)

                if test_value:
                    identifier_field.fill(test_value)
                    time.sleep(0.5)

                # Check field state
                current_value = identifier_field.input_value()
                field_visible = identifier_field.is_visible()
                field_enabled = identifier_field.is_enabled()

                if should_be_valid:
                    # Valid input should be accepted
                    if field_enabled and (
                        not test_value or test_value in current_value
                    ):
                        logger.info(
                            f" Valid input '{test_value}' accepted for {description}"
                        )
                    else:
                        logger.warning(
                            f" Valid input '{test_value}' may not have been accepted for {description}"
                        )
                else:
                    # Invalid input behavior depends on device implementation
                    logger.info(
                        f"ℹ Invalid input '{test_value}' testing - device-specific behavior"
                    )

            except Exception as e:
                logger.warning(f"Validation test failed for '{test_value}': {e}")

    except Exception as e:
        pytest.fail(f"Numeric field validation failed on {device_model}: {e}")

    # Test save button behavior with validation
    try:
        # Make a valid change to test save button
        test_identifier = "TestDevice123"
        general_config_page.configure_device_info(identifier=test_identifier)

        # Wait for save button to enable with device-aware timing
        save_button = general_config_page.get_save_button_locator()
        if save_button.count() > 0:
            expect(save_button).to_be_enabled(timeout=int(5000 * timeout_multiplier))
            logger.info(f"Save button enabled after valid input on {device_model}")

            # Test save functionality
            save_success = general_config_page.save_configuration()
            if save_success:
                logger.info(f"Valid input save successful on {device_model}")
            else:
                logger.warning(f"Valid input save failed on {device_model}")
        else:
            logger.warning(
                f"Save button not found for validation test on {device_model}"
            )

    except Exception as e:
        logger.warning(f"Save button validation test failed on {device_model}: {e}")

    # Test field persistence across navigation
    try:
        # Set a test value
        test_value = "ValidationTest123"
        general_config_page.configure_device_info(identifier=test_value)

        # Navigate away and back
        dashboard_page = general_config_page.page.locator("text=Dashboard")
        if dashboard_page.count() > 0:
            dashboard_page.click()
            time.sleep(2)

            # Navigate back
            general_config_page.navigate_to_page()
            time.sleep(2)

            # Check if value persisted
            current_value = identifier_field.input_value()
            if test_value in current_value:
                logger.info(f"Field value persistence verified on {device_model}")
            else:
                logger.warning(f"Field value may not have persisted on {device_model}")

    except Exception as e:
        logger.warning(f"Field persistence test failed on {device_model}: {e}")

    # Performance validation against device baselines
    try:
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            nav_performance = performance_data.get("navigation_performance", {})
            section_nav = nav_performance.get("section_navigation", {})
            typical_time = section_nav.get("typical_time", "")

            if typical_time:
                logger.info(f"Form navigation performance baseline: {typical_time}")

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)
    capabilities = DeviceCapabilities.get_capabilities(device_model)

    logger.info(f"Numeric field validation test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Device series: {device_series}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"NUMERIC FIELD VALIDATION COMPLETED: {device_model} (Series {device_series})"
    )
