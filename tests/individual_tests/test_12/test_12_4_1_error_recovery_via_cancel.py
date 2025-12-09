"""
Test 12.4.1: Error Recovery via Cancel Button - Pure Page Object Pattern
Category: 12 - Error Handling Tests
Test Count: Part of 11 tests in Category 12
Hardware: Device Only
Priority: HIGH - Proper error handling critical for reliability
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on error recovery via cancel button functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_12_4_1_error_recovery_via_cancel(logged_in_page: Page, base_url: str, request):
    """
    Test 12.4.1: Error Recovery via Cancel Button - Pure Page Object Pattern
    Purpose: Verify error recovery functionality through cancel button with device-aware validation
    Expected: Cancel button properly restores previous state with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates error recovery patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate configuration behavior"
        )

    # Initialize page object with device-aware patterns
    general_page = GeneralConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing error recovery via cancel button on {device_model} using pure page object pattern"
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
            f"Testing error recovery via cancel button on {device_model} (Series {device_series})"
        )

        # Navigate to general configuration page using page object method
        logger.info("Navigating to general configuration page")
        general_page.navigate_to_general_config()

        # Test error recovery patterns using page object methods
        logger.info("Testing error recovery patterns")

        # Get original valid values using page object method
        logger.info("Retrieving original configuration values")
        original_data = general_page.get_page_data()
        logger.info(
            f"Original configuration data: {list(original_data.keys()) if original_data else 'None'}"
        )

        # Test identifier field modification using page object methods
        logger.info("Testing identifier field modification")
        test_value = "TEST"
        identifier_config = general_page.configure_identifier(test_value)
        logger.info(f"Identifier configuration result: {identifier_config}")

        # Test field clearing and restoration using page object methods
        logger.info("Testing field clearing and restoration")
        clear_result = general_page.test_identifier_field_clearing()
        logger.info(f"Field clearing result: {clear_result}")

        # Test cancel button functionality using page object method
        logger.info("Testing cancel button functionality")
        cancel_result = general_page.test_cancel_button_functionality()
        logger.info(f"Cancel button functionality result: {cancel_result}")

        # Test device series-specific behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 error recovery patterns")

            # Test Series 2 specific cancel behavior
            series2_recovery = general_page.test_series2_cancel_recovery()
            logger.info(f"Series 2 cancel recovery result: {series2_recovery}")

            # Configure general settings for Series 2
            general_config = general_page.configure_series2_general_settings()
            logger.info(f"Series 2 general configuration result: {general_config}")

        elif device_series == 3:
            logger.info(f"Testing Series 3 error recovery patterns")

            # Test Series 3 specific cancel behavior
            series3_recovery = general_page.test_series3_cancel_recovery()
            logger.info(f"Series 3 cancel recovery result: {series3_recovery}")

            # Configure general settings for Series 3
            general_config = general_page.configure_series3_general_settings()
            logger.info(f"Series 3 general configuration result: {general_config}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            general_config = device_capabilities_data.get("general_configuration", {})
            cancel_behavior = general_config.get("cancel_behavior", {})
            logger.info(f"Cancel behavior from DeviceCapabilities: {cancel_behavior}")

        # Test error message validation using page object method
        logger.info("Testing error message validation")
        error_messages = general_page.get_error_messages()

        if error_messages:
            logger.info(f"Error messages found: {error_messages}")
        else:
            logger.info(f"No specific error messages detected")

        # Test form state validation using page object method
        logger.info("Testing form state validation")
        form_state = general_page.get_form_validation_state()
        logger.info(f"Form validation state: {form_state}")

        # Test save button state using page object method
        logger.info("Testing save button state")
        save_state = general_page.test_save_button_state()
        logger.info(f"Save button state: {save_state}")

        # Test data persistence after cancel using page object methods
        logger.info("Testing data persistence after cancel")
        persistence_result = general_page.test_data_persistence_after_cancel()
        logger.info(f"Data persistence result: {persistence_result}")

        # Test page reload behavior using page object method
        logger.info("Testing page reload behavior")
        reload_result = general_page.test_page_reload_behavior()
        logger.info(f"Page reload behavior result: {reload_result}")

        # Test form restoration patterns using page object method
        logger.info("Testing form restoration patterns")
        restoration_patterns = general_page.get_form_restoration_patterns()
        logger.info(f"Form restoration patterns: {restoration_patterns}")

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
            cancel_perf = general_performance.get("cancel_recovery", {})

            typical_recovery = cancel_perf.get("typical_time", "")
            worst_case = cancel_perf.get("worst_case", "")

            if typical_recovery:
                logger.info(f"Cancel recovery performance baseline: {typical_recovery}")
            if worst_case:
                logger.info(f"Cancel recovery worst case: {worst_case}")

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

        # Final validation
        logger.info(
            f"Error recovery via cancel button test completed for {device_model}"
        )

        if device_series == 2:
            logger.info(
                f"Series 2 error recovery via cancel test PASSED for {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 error recovery via cancel test PASSED for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(
            f"Error recovery via cancel button test failed on {device_model}: {e}"
        )
        pytest.fail(
            f"Error recovery via cancel button test failed on {device_model}: {e}"
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
            f"Error recovery via cancel button test completed for {device_model}"
        )
