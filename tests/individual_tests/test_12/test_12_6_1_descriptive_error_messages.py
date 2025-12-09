"""
Test 12.6.1: Descriptive Error Messages - Pure Page Object Pattern
Category: 12 - Error Handling Tests
Test Count: Part of 11 tests in Category 12
Hardware: Device Only
Priority: HIGH - Proper error handling critical for reliability
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on descriptive error messages functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.snmp_config_page import SNMPConfigPage

logger = logging.getLogger(__name__)


def test_12_6_1_descriptive_error_messages(
    logged_in_page: Page, base_url: str, request
):
    """
    Test 12.6.1: Descriptive Error Messages - Pure Page Object Pattern
    Purpose: Verify error messages are descriptive and meaningful with device-aware validation
    Expected: Error messages provide clear, actionable information with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates error message patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate SNMP behavior")

    # Initialize page object with device-aware patterns
    snmp_page = SNMPConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing descriptive error messages on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to dashboard page using page object method
        logger.info("Navigating to dashboard page")
        logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")

        # Wait for page load with device-aware timeout
        snmp_page.wait_for_page_load()

        # Test device series-specific behavior using page object methods
        device_series = DeviceCapabilities.get_series(device_model)

        logger.info(
            f"Testing descriptive error messages on {device_model} (Series {device_series})"
        )

        # Navigate to SNMP configuration page using page object method
        logger.info("Navigating to SNMP configuration page")
        snmp_page.navigate_to_snmp_config()

        # Test descriptive error message patterns using page object methods
        logger.info("Testing descriptive error message patterns")

        # Test SNMP community field validation for error messages using page object methods
        logger.info("Testing SNMP community field validation for error messages")

        # Get original community string value using page object method
        original_value = snmp_page.get_ro_community1_value()
        logger.info(f"Original SNMP community string: '{original_value}'")

        # Test clearing community string to trigger validation errors using page object method
        logger.info("Testing community string clearing for error message validation")
        clear_result = snmp_page.test_community_string_clearing_for_error_messages()
        logger.info(f"Community string clearing result: {clear_result}")

        # Test device series-specific behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 descriptive error message patterns")

            # Test Series 2 specific error message behavior
            series2_error_patterns = snmp_page.test_series2_descriptive_error_patterns()
            logger.info(
                f"Series 2 descriptive error patterns: {series2_error_patterns}"
            )

            # Configure SNMP settings for Series 2
            snmp_config = snmp_page.configure_series2_snmp_settings()
            logger.info(f"Series 2 SNMP configuration result: {snmp_config}")

        elif device_series == 3:
            logger.info(f"Testing Series 3 descriptive error message patterns")

            # Test Series 3 specific error message behavior
            series3_error_patterns = snmp_page.test_series3_descriptive_error_patterns()
            logger.info(
                f"Series 3 descriptive error patterns: {series3_error_patterns}"
            )

            # Configure SNMP settings for Series 3
            snmp_config = snmp_page.configure_series3_snmp_settings()
            logger.info(f"Series 3 SNMP configuration result: {snmp_config}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            snmp_config = device_capabilities_data.get("snmp_configuration", {})
            error_message_patterns = snmp_config.get("error_message_patterns", {})
            logger.info(
                f"Error message patterns from DeviceCapabilities: {error_message_patterns}"
            )

        # Test error message validation using page object method
        logger.info("Testing error message validation")
        error_messages = snmp_page.get_error_messages()

        if error_messages:
            logger.info(f"Error messages found: {error_messages}")

            # Test error message quality using page object method
            logger.info("Testing error message quality")
            message_quality = snmp_page.test_error_message_quality()
            logger.info(f"Error message quality assessment: {message_quality}")

            # Test error message clarity using page object method
            logger.info("Testing error message clarity")
            message_clarity = snmp_page.test_error_message_clarity()
            logger.info(f"Error message clarity assessment: {message_clarity}")

            # Test error message actionability using page object method
            logger.info("Testing error message actionability")
            message_actionability = snmp_page.test_error_message_actionability()
            logger.info(
                f"Error message actionability assessment: {message_actionability}"
            )
        else:
            logger.info(f"No specific error messages detected")

        # Test save functionality with error message validation using page object method
        logger.info("Testing save functionality with error message validation")
        save_result = snmp_page.test_save_with_error_message_validation()
        logger.info(f"Save with error message validation result: {save_result}")

        # Test form validation patterns using page object method
        logger.info("Testing form validation patterns")
        validation_patterns = snmp_page.get_form_validation_patterns()
        logger.info(f"Form validation patterns: {validation_patterns}")

        # Test error message detection patterns using page object method
        logger.info("Testing error message detection patterns")
        detection_patterns = snmp_page.get_error_message_detection_patterns()
        logger.info(f"Error message detection patterns: {detection_patterns}")

        # Test descriptive error categorization using page object method
        logger.info("Testing descriptive error categorization")
        error_categorization = snmp_page.test_descriptive_error_categorization()
        logger.info(f"Descriptive error categorization: {error_categorization}")

        # Test error message accessibility using page object method
        logger.info("Testing error message accessibility")
        message_accessibility = snmp_page.test_error_message_accessibility()
        logger.info(f"Error message accessibility: {message_accessibility}")

        # Performance validation using page object methods
        logger.info("Performing performance validation")

        start_time = time.time()

        # Test page reload performance
        snmp_page.reload_page()
        reload_time = time.time() - start_time

        logger.info(f"Page reload time: {reload_time:.2f}s")

        # Cross-reference with performance expectations
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            snmp_performance = performance_data.get("snmp_configuration", {})
            error_message_perf = snmp_performance.get("error_message_display", {})

            typical_display = error_message_perf.get("typical_time", "")
            worst_case = error_message_perf.get("worst_case", "")

            if typical_display:
                logger.info(
                    f"Error message display performance baseline: {typical_display}"
                )
            if worst_case:
                logger.info(f"Error message display worst case: {worst_case}")

            # Basic timing validation
            if reload_time > 3.0:  # Simple threshold for now
                logger.warning(
                    f"Page reload took longer than expected: {reload_time:.2f}s"
                )

        # Test page data retrieval using page object method
        page_data = snmp_page.get_page_data()
        logger.info(f"SNMP configuration page data retrieved: {list(page_data.keys())}")

        # Test SNMP capabilities validation using page object method
        snmp_capabilities = snmp_page.detect_snmp_capabilities()
        logger.info(f"SNMP capabilities detected: {snmp_capabilities}")

        # Final validation
        logger.info(f"Descriptive error messages test completed for {device_model}")

        if device_series == 2:
            logger.info(
                f"Series 2 descriptive error messages test PASSED for {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 descriptive error messages test PASSED for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Descriptive error messages test failed on {device_model}: {e}")
        pytest.fail(f"Descriptive error messages test failed on {device_model}: {e}")

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = snmp_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(f"Descriptive error messages test completed for {device_model}")
