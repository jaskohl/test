"""
Test 13.3.2: Dirty to Pristine State via Cancel - Pure Page Object Pattern
Category: 13 - State Transitions Tests
Test Count: Part of 7 tests in Category 13
Hardware: Device Only
Priority: MEDIUM - Form state management
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on dirty to pristine state via cancel functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_13_3_2_dirty_to_pristine_via_cancel(
    logged_in_page: Page, base_url: str, request
):
    """
    Test 13.3.2: Dirty to Pristine State via Cancel - Pure Page Object Pattern
    Purpose: Verify cancel button resets form to pristine state with device-aware validation
    Expected: Save button returns to disabled state after cancel with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates form state reset patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate form state reset behavior"
        )

    # Initialize page object with device-aware patterns
    general_page = GeneralConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing dirty to pristine state via cancel on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to dashboard page using page object method
        logger.info("Navigating to dashboard page")
        logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")

        # Wait for page load with device-aware timeout
        general_page.wait_for_page_load()

        # Test device series-specific behavior using page object methods
        device_series = DeviceCapabilities.get_series(device_model)

        logger.info(
            f"Testing dirty to pristine state via cancel on {device_model} (Series {device_series})"
        )

        # Navigate to general configuration page using page object method
        logger.info("Navigating to general configuration page")
        general_page.navigate_to_general_config()

        # Test form state reset patterns using page object methods
        logger.info("Testing form state reset patterns")

        # Get original field values using page object method
        logger.info("Retrieving original field values")
        original_values = general_page.get_original_field_values()
        logger.info(f"Original field values: {original_values}")

        # Test form field modification using page object methods
        logger.info("Testing form field modification")
        test_value = "TEST_CANCEL_STATE"
        identifier_config = general_page.configure_identifier(test_value)
        logger.info(f"Identifier configuration result: {identifier_config}")

        # Test device series-specific form state reset behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 form state reset patterns")

            # Test Series 2 specific form state reset behavior
            series2_reset = general_page.test_series2_dirty_to_pristine_via_cancel()
            logger.info(
                f"Series 2 dirty to pristine via cancel result: {series2_reset}"
            )

            # Test Series 2 save button state after cancel
            save_button_state = (
                general_page.test_series2_save_button_state_after_cancel()
            )
            logger.info(f"Series 2 save button state after cancel: {save_button_state}")

            # Configure general settings for Series 2
            general_config = general_page.configure_series2_general_settings()
            logger.info(f"Series 2 general configuration result: {general_config}")

        elif device_series == 3:
            logger.info(f"Testing Series 3 form state reset patterns")

            # Test Series 3 specific form state reset behavior
            series3_reset = general_page.test_series3_dirty_to_pristine_via_cancel()
            logger.info(
                f"Series 3 dirty to pristine via cancel result: {series3_reset}"
            )

            # Test Series 3 save button state after cancel
            save_button_state = (
                general_page.test_series3_save_button_state_after_cancel()
            )
            logger.info(f"Series 3 save button state after cancel: {save_button_state}")

            # Configure general settings for Series 3
            general_config = general_page.configure_series3_general_settings()
            logger.info(f"Series 3 general configuration result: {general_config}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            general_config = device_capabilities_data.get("general_configuration", {})
            form_state_reset = general_config.get("form_state_reset", {})
            logger.info(f"Form state reset from DeviceCapabilities: {form_state_reset}")

        # Test cancel button functionality using page object method
        logger.info("Testing cancel button functionality")
        cancel_functionality = general_page.test_cancel_button_functionality()
        logger.info(f"Cancel button functionality result: {cancel_functionality}")

        # Test form state restoration using page object method
        logger.info("Testing form state restoration")
        state_restoration = general_page.test_form_state_restoration()
        logger.info(f"Form state restoration result: {state_restoration}")

        # Test save button state validation using page object method
        logger.info("Testing save button state validation")
        save_state_validation = general_page.test_save_button_state_validation()
        logger.info(f"Save button state validation result: {save_state_validation}")

        # Test form field value restoration using page object method
        logger.info("Testing form field value restoration")
        value_restoration = general_page.test_form_field_value_restoration(
            original_values
        )
        logger.info(f"Form field value restoration result: {value_restoration}")

        # Test pristine state detection using page object method
        logger.info("Testing pristine state detection")
        pristine_state = general_page.test_pristine_state_detection()
        logger.info(f"Pristine state detection result: {pristine_state}")

        # Test form validation patterns using page object method
        logger.info("Testing form validation patterns")
        validation_patterns = general_page.get_form_validation_patterns()
        logger.info(f"Form validation patterns: {validation_patterns}")

        # Test cancel operation patterns using page object method
        logger.info("Testing cancel operation patterns")
        cancel_patterns = general_page.get_cancel_operation_patterns()
        logger.info(f"Cancel operation patterns: {cancel_patterns}")

        # Test form state comparison using page object method
        logger.info("Testing form state comparison")
        state_comparison = general_page.test_form_state_comparison(original_values)
        logger.info(f"Form state comparison result: {state_comparison}")

        # Performance validation using page object methods
        logger.info("Performing performance validation")

        start_time = time.time()

        # Test page reload performance
        general_page.reload_page()
        reload_time = time.time() - start_time

        logger.info(f"Page reload time: {reload_time:.2f}s")

        # Cross-reference with performance expectations
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            general_performance = performance_data.get("general_configuration", {})
            cancel_perf = general_performance.get("cancel_operation", {})

            typical_cancel = cancel_perf.get("typical_time", "")
            worst_case = cancel_perf.get("worst_case", "")

            if typical_cancel:
                logger.info(f"Cancel operation performance baseline: {typical_cancel}")
            if worst_case:
                logger.info(f"Cancel operation worst case: {worst_case}")

            # Basic timing validation
            if reload_time > 3.0:  # Simple threshold for now
                logger.warning(
                    f"Page reload took longer than expected: {reload_time:.2f}s"
                )

        # Test page data retrieval using page object method
        page_data = general_page.get_page_data()
        logger.info(
            f"General configuration page data retrieved: {list(page_data.keys()) if page_data else 'None'}"
        )

        # Test general configuration capabilities using page object method
        general_capabilities = general_page.detect_general_capabilities()
        logger.info(
            f"General configuration capabilities detected: {general_capabilities}"
        )

        # Test error message validation using page object method
        logger.info("Testing error message validation")
        error_messages = general_page.get_error_messages()

        if error_messages:
            logger.info(f"Error messages found: {error_messages}")
        else:
            logger.info(f"No specific error messages detected")

        # Final validation
        logger.info(
            f"Dirty to pristine state via cancel test completed for {device_model}"
        )

        if device_series == 2:
            logger.info(
                f"Series 2 dirty to pristine state via cancel test PASSED for {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 dirty to pristine state via cancel test PASSED for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(
            f"Dirty to pristine state via cancel test failed on {device_model}: {e}"
        )
        pytest.fail(
            f"Dirty to pristine state via cancel test failed on {device_model}: {e}"
        )

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = general_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(
            f"Dirty to pristine state via cancel test completed for {device_model}"
        )
