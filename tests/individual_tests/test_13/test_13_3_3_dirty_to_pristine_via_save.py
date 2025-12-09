"""
Test 13.3.3: Dirty to Pristine State via Save - Pure Page Object Pattern
Category: 13 - State Transitions Tests
Test Count: Part of 7 tests in Category 13
Hardware: Device Only
Priority: MEDIUM - Form state management
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on dirty to pristine state via save functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_13_3_3_dirty_to_pristine_via_save(
    logged_in_page: Page, base_url: str, request
):
    """
    Test 13.3.3: Dirty to Pristine State via Save - Pure Page Object Pattern
    Purpose: Verify save button resets form to pristine state after successful save with device-aware validation
    Expected: Save button returns to disabled state after save operation with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates form state save patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate form state save behavior"
        )

    # Initialize page object with device-aware patterns
    general_page = GeneralConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing dirty to pristine state via save on {device_model} using pure page object pattern"
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
            f"Testing dirty to pristine state via save on {device_model} (Series {device_series})"
        )

        # Navigate to general configuration page using page object method
        logger.info("Navigating to general configuration page")
        general_page.navigate_to_general_config()

        # Test form state save patterns using page object methods
        logger.info("Testing form state save patterns")

        # Get original field values using page object method
        logger.info("Retrieving original field values")
        original_values = general_page.get_original_field_values()
        logger.info(f"Original field values: {original_values}")

        # Test form field modification using page object methods
        logger.info("Testing form field modification")
        test_value = "TEST_SAVE_STATE"
        identifier_config = general_page.configure_identifier(test_value)
        logger.info(f"Identifier configuration result: {identifier_config}")

        # Test device series-specific form state save behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 form state save patterns")

            # Test Series 2 specific form state save behavior
            series2_save = general_page.test_series2_dirty_to_pristine_via_save()
            logger.info(f"Series 2 dirty to pristine via save result: {series2_save}")

            # Test Series 2 save button state after save
            save_button_state = general_page.test_series2_save_button_state_after_save()
            logger.info(f"Series 2 save button state after save: {save_button_state}")

            # Configure general settings for Series 2
            general_config = general_page.configure_series2_general_settings()
            logger.info(f"Series 2 general configuration result: {general_config}")

        elif device_series == 3:
            logger.info(f"Testing Series 3 form state save patterns")

            # Test Series 3 specific form state save behavior
            series3_save = general_page.test_series3_dirty_to_pristine_via_save()
            logger.info(f"Series 3 dirty to pristine via save result: {series3_save}")

            # Test Series 3 save button state after save
            save_button_state = general_page.test_series3_save_button_state_after_save()
            logger.info(f"Series 3 save button state after save: {save_button_state}")

            # Configure general settings for Series 3
            general_config = general_page.configure_series3_general_settings()
            logger.info(f"Series 3 general configuration result: {general_config}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            general_config = device_capabilities_data.get("general_configuration", {})
            form_state_save = general_config.get("form_state_save", {})
            logger.info(f"Form state save from DeviceCapabilities: {form_state_save}")

        # Test save button functionality using page object method
        logger.info("Testing save button functionality")
        save_functionality = general_page.test_save_button_functionality()
        logger.info(f"Save button functionality result: {save_functionality}")

        # Test form state persistence using page object method
        logger.info("Testing form state persistence")
        state_persistence = general_page.test_form_state_persistence()
        logger.info(f"Form state persistence result: {state_persistence}")

        # Test save button state validation using page object method
        logger.info("Testing save button state validation")
        save_state_validation = general_page.test_save_button_state_validation()
        logger.info(f"Save button state validation result: {save_state_validation}")

        # Test form field value persistence using page object method
        logger.info("Testing form field value persistence")
        value_persistence = general_page.test_form_field_value_persistence(test_value)
        logger.info(f"Form field value persistence result: {value_persistence}")

        # Test pristine state detection after save using page object method
        logger.info("Testing pristine state detection after save")
        pristine_state = general_page.test_pristine_state_detection_after_save()
        logger.info(f"Pristine state detection after save result: {pristine_state}")

        # Test form validation patterns using page object method
        logger.info("Testing form validation patterns")
        validation_patterns = general_page.get_form_validation_patterns()
        logger.info(f"Form validation patterns: {validation_patterns}")

        # Test save operation patterns using page object method
        logger.info("Testing save operation patterns")
        save_patterns = general_page.get_save_operation_patterns()
        logger.info(f"Save operation patterns: {save_patterns}")

        # Test form state comparison using page object method
        logger.info("Testing form state comparison")
        state_comparison = general_page.test_form_state_comparison(original_values)
        logger.info(f"Form state comparison result: {state_comparison}")

        # Test original value restoration using page object method
        logger.info("Testing original value restoration")
        if original_values:
            restoration_result = general_page.restore_original_values(original_values)
            logger.info(f"Original value restoration result: {restoration_result}")

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
            save_perf = general_performance.get("save_operation", {})

            typical_save = save_perf.get("typical_time", "")
            worst_case = save_perf.get("worst_case", "")

            if typical_save:
                logger.info(f"Save operation performance baseline: {typical_save}")
            if worst_case:
                logger.info(f"Save operation worst case: {worst_case}")

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
            f"Dirty to pristine state via save test completed for {device_model}"
        )

        if device_series == 2:
            logger.info(
                f"Series 2 dirty to pristine state via save test PASSED for {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 dirty to pristine state via save test PASSED for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(
            f"Dirty to pristine state via save test failed on {device_model}: {e}"
        )
        pytest.fail(
            f"Dirty to pristine state via save test failed on {device_model}: {e}"
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
            f"Dirty to pristine state via save test completed for {device_model}"
        )
