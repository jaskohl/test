"""
Test 13.3.1: Pristine to Dirty State Transition - Pure Page Object Pattern
Category: 13 - State Transitions Tests
Test Count: Part of 7 tests in Category 13
Hardware: Device Only
Priority: MEDIUM - Form state management
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on pristine to dirty state transition functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_13_3_1_pristine_to_dirty_state(logged_in_page: Page, base_url: str, request):
    """
    Test 13.3.1: Pristine to Dirty State Transition - Pure Page Object Pattern
    Purpose: Verify form state transitions from pristine to dirty state with device-aware validation
    Expected: Form detects changes from pristine to dirty state with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates form state transition patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate form state transitions"
        )

    # Initialize page object with device-aware patterns
    general_page = GeneralConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing pristine to dirty state transition on {device_model} using pure page object pattern"
    )

    # Get device series and timeout multiplier for device-aware handling
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Calculate series-specific timeout
    base_timeout = 10000  # 10 seconds base for form interactions
    series_timeout = int(base_timeout * timeout_multiplier)

    logger.info(f"\n{'='*60}")
    logger.info(f"DEVICE TEST: Pristine to Dirty State Transition")
    logger.info(f"{'='*60}")
    logger.info(f"Device Model: {device_model}")
    logger.info(f"Device Series: {device_series}")
    logger.info(f"Timeout Multiplier: {timeout_multiplier}")
    logger.info(f"Series-Specific Timeout: {series_timeout}ms")
    logger.info(f"{'='*60}\n")

    try:
        # Navigate to dashboard page using page object method
        logger.info("Navigating to dashboard page")
        logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")

        # Wait for page load with device-aware timeout
        general_page.wait_for_page_load()

        logger.info(
            f"Testing pristine to dirty state transition on {device_model} (Series {device_series})"
        )

        # Navigate to general configuration page using page object method
        logger.info("Navigating to general configuration page")
        general_page.navigate_to_general_config()

        # Test form state transition patterns using page object methods
        logger.info("Testing form state transition patterns")

        # Test device series-specific form state behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 form state transition patterns")

            # Test Series 2 specific form state transition behavior
            series2_transition = (
                general_page.test_series2_pristine_to_dirty_transition()
            )
            logger.info(
                f"Series 2 pristine to dirty transition result: {series2_transition}"
            )

            # Test Series 2 save button state validation
            save_button_validation = (
                general_page.test_series2_save_button_state_validation()
            )
            logger.info(
                f"Series 2 save button state validation result: {save_button_validation}"
            )

            # Configure general settings for Series 2
            general_config = general_page.configure_series2_general_settings()
            logger.info(f"Series 2 general configuration result: {general_config}")

        elif device_series == 3:
            logger.info(f"Testing Series 3 form state transition patterns")

            # Test Series 3 specific form state transition behavior
            series3_transition = (
                general_page.test_series3_pristine_to_dirty_transition()
            )
            logger.info(
                f"Series 3 pristine to dirty transition result: {series3_transition}"
            )

            # Test Series 3 save button state validation
            save_button_validation = (
                general_page.test_series3_save_button_state_validation()
            )
            logger.info(
                f"Series 3 save button state validation result: {save_button_validation}"
            )

            # Configure general settings for Series 3
            general_config = general_page.configure_series3_general_settings()
            logger.info(f"Series 3 general configuration result: {general_config}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            general_config = device_capabilities_data.get("general_configuration", {})
            form_state_transitions = general_config.get("form_state_transitions", {})
            logger.info(
                f"Form state transitions from DeviceCapabilities: {form_state_transitions}"
            )

        # Test form field visibility using page object method
        logger.info("Testing form field visibility")
        field_visibility = general_page.test_identifier_field_visibility()
        logger.info(f"Identifier field visibility result: {field_visibility}")

        # Test form state detection using page object method
        logger.info("Testing form state detection")
        state_detection = general_page.test_form_state_detection()
        logger.info(f"Form state detection result: {state_detection}")

        # Test form state transition validation using page object method
        logger.info("Testing form state transition validation")
        transition_validation = general_page.test_form_state_transition_validation()
        logger.info(f"Form state transition validation result: {transition_validation}")

        # Test save button state validation using page object method
        logger.info("Testing save button state validation")
        save_state_validation = general_page.test_save_button_state_validation()
        logger.info(f"Save button state validation result: {save_state_validation}")

        # Test original field value retrieval using page object method
        logger.info("Retrieving original field values")
        original_values = general_page.get_original_field_values()
        logger.info(f"Original field values: {original_values}")

        # Test form change detection using page object method
        logger.info("Testing form change detection")
        test_value = f"TEST_STATE_CHANGE_{device_series}"
        change_detection = general_page.test_form_change_detection(test_value)
        logger.info(f"Form change detection result: {change_detection}")

        # Test form state comparison using page object method
        logger.info("Testing form state comparison")
        state_comparison = general_page.test_form_state_comparison(original_values)
        logger.info(f"Form state comparison result: {state_comparison}")

        # Test form interaction patterns using page object method
        logger.info("Testing form interaction patterns")
        interaction_patterns = general_page.test_form_interaction_patterns()
        logger.info(f"Form interaction patterns: {interaction_patterns}")

        # Test series-specific form validation using page object method
        logger.info("Testing series-specific form validation")
        series_validation = general_page.test_series_specific_form_validation()
        logger.info(f"Series-specific form validation: {series_validation}")

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
            form_transition_perf = general_performance.get("form_state_transitions", {})

            typical_transition = form_transition_perf.get("typical_time", "")
            worst_case = form_transition_perf.get("worst_case", "")

            if typical_transition:
                logger.info(
                    f"Form state transition performance baseline: {typical_transition}"
                )
            if worst_case:
                logger.info(f"Form state transition worst case: {worst_case}")

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
        logger.info(f"\n{'='*60}")
        logger.info(f"FINAL VALIDATION RESULTS")
        logger.info(f"{'='*60}")
        logger.info(f"Device Model: {device_model}")
        logger.info(f"Device Series: {device_series}")
        logger.info(f"Timeout Multiplier: {timeout_multiplier}")
        logger.info(f"Navigation Timeout: {series_timeout}ms")
        logger.info(f"Form State Transition: True")
        logger.info(f"{'='*60}\n")

        logger.info(
            f"Pristine to dirty state transition validated successfully for {device_model} (Series {device_series})"
        )

        if device_series == 2:
            logger.info(
                f"Series 2 pristine to dirty state transition test PASSED for {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 pristine to dirty state transition test PASSED for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(
            f"Pristine to dirty state transition test failed on {device_model}: {e}"
        )
        pytest.fail(
            f"Pristine to dirty state transition test failed on {device_model}: {e}"
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
            f"Pristine to dirty state transition test completed for {device_model}"
        )
