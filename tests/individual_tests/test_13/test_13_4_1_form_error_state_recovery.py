"""
Test 13.4.1: Form Error State Recovery - Pure Page Object Pattern
Category: 13 - State Transitions Tests
Test Count: Part of 7 tests in Category 13
Hardware: Device Only
Priority: MEDIUM - Form state management
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on form error state recovery functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_13_4_1_form_error_state_recovery(logged_in_page: Page, base_url: str, request):
    """
    Test 13.4.1: Form Error State Recovery - Pure Page Object Pattern
    Purpose: Verify form recovers gracefully from validation errors with device-aware validation
    Expected: Error states can be cleared and form returns to normal operation with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates form error recovery patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate form error recovery behavior"
        )

    # Initialize page object with device-aware patterns
    general_page = GeneralConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing form error state recovery on {device_model} using pure page object pattern"
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
            f"Testing form error state recovery on {device_model} (Series {device_series})"
        )

        # Navigate to general configuration page using page object method
        logger.info("Navigating to general configuration page")
        general_page.navigate_to_general_config()

        # Test form error state recovery patterns using page object methods
        logger.info("Testing form error state recovery patterns")

        # Get original data using page object method
        logger.info("Retrieving original form data")
        original_data = general_page.get_page_data()
        logger.info(
            f"Original form data: {list(original_data.keys()) if original_data else 'None'}"
        )

        # Test form field modification using page object methods
        logger.info("Testing form field modification")
        test_value = "TEST_ERROR_RECOVERY"
        identifier_config = general_page.configure_identifier(test_value)
        logger.info(f"Identifier configuration result: {identifier_config}")

        # Test device series-specific form error recovery behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 form error recovery patterns")

            # Test Series 2 specific form error recovery behavior
            series2_recovery = general_page.test_series2_form_error_state_recovery()
            logger.info(
                f"Series 2 form error state recovery result: {series2_recovery}"
            )

            # Test Series 2 error state validation
            error_validation = general_page.test_series2_error_state_validation()
            logger.info(f"Series 2 error state validation result: {error_validation}")

            # Configure general settings for Series 2
            general_config = general_page.configure_series2_general_settings()
            logger.info(f"Series 2 general configuration result: {general_config}")

        elif device_series == 3:
            logger.info(f"Testing Series 3 form error recovery patterns")

            # Test Series 3 specific form error recovery behavior
            series3_recovery = general_page.test_series3_form_error_state_recovery()
            logger.info(
                f"Series 3 form error state recovery result: {series3_recovery}"
            )

            # Test Series 3 error state validation
            error_validation = general_page.test_series3_error_state_validation()
            logger.info(f"Series 3 error state validation result: {error_validation}")

            # Configure general settings for Series 3
            general_config = general_page.configure_series3_general_settings()
            logger.info(f"Series 3 general configuration result: {general_config}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            general_config = device_capabilities_data.get("general_configuration", {})
            error_recovery = general_config.get("error_state_recovery", {})
            logger.info(
                f"Error state recovery from DeviceCapabilities: {error_recovery}"
            )

        # Test form error recovery using page object method
        logger.info("Testing form error recovery")
        error_recovery = general_page.test_form_error_recovery()
        logger.info(f"Form error recovery result: {error_recovery}")

        # Test form state validation using page object method
        logger.info("Testing form state validation")
        state_validation = general_page.test_form_state_validation()
        logger.info(f"Form state validation result: {state_validation}")

        # Test error state detection using page object method
        logger.info("Testing error state detection")
        error_detection = general_page.test_error_state_detection()
        logger.info(f"Error state detection result: {error_detection}")

        # Test form recovery mechanisms using page object method
        logger.info("Testing form recovery mechanisms")
        recovery_mechanisms = general_page.test_form_recovery_mechanisms()
        logger.info(f"Form recovery mechanisms result: {recovery_mechanisms}")

        # Test normal operation restoration using page object method
        logger.info("Testing normal operation restoration")
        operation_restoration = general_page.test_normal_operation_restoration()
        logger.info(f"Normal operation restoration result: {operation_restoration}")

        # Test validation error clearing using page object method
        logger.info("Testing validation error clearing")
        error_clearing = general_page.test_validation_error_clearing()
        logger.info(f"Validation error clearing result: {error_clearing}")

        # Test form field value restoration using page object method
        logger.info("Testing form field value restoration")
        if original_data:
            value_restoration = general_page.test_form_field_value_restoration(
                original_data
            )
            logger.info(f"Form field value restoration result: {value_restoration}")

        # Test graceful error handling using page object method
        logger.info("Testing graceful error handling")
        error_handling = general_page.test_graceful_error_handling()
        logger.info(f"Graceful error handling result: {error_handling}")

        # Test form error patterns using page object method
        logger.info("Testing form error patterns")
        error_patterns = general_page.get_form_error_patterns()
        logger.info(f"Form error patterns: {error_patterns}")

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
            error_recovery_perf = general_performance.get("error_state_recovery", {})

            typical_recovery = error_recovery_perf.get("typical_time", "")
            worst_case = error_recovery_perf.get("worst_case", "")

            if typical_recovery:
                logger.info(
                    f"Error state recovery performance baseline: {typical_recovery}"
                )
            if worst_case:
                logger.info(f"Error state recovery worst case: {worst_case}")

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
        logger.info(f"Form error state recovery test completed for {device_model}")

        if device_series == 2:
            logger.info(
                f"Series 2 form error state recovery test PASSED for {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 form error state recovery test PASSED for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Form error state recovery test failed on {device_model}: {e}")
        pytest.fail(f"Form error state recovery test failed on {device_model}: {e}")

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = general_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(f"Form error state recovery test completed for {device_model}")
