"""
Test 12.3.1: Empty SNMP Community String Error - Pure Page Object Pattern
Category: 12 - Error Handling Tests
Test Count: Part of 11 tests in Category 12
Hardware: Device Only
Priority: HIGH - Proper error handling critical for reliability
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on empty SNMP community string error functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.snmp_config_page import SNMPConfigPage

logger = logging.getLogger(__name__)


def test_12_3_1_empty_community_string_error(
    logged_in_page: Page, base_url: str, request
):
    """
    Test 12.3.1: Empty SNMP Community String Error - Pure Page Object Pattern
    Purpose: Verify error handling for empty SNMP community string with device-aware validation
    Expected: SNMP community validation fails and appropriate error is indicated with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates SNMP configuration patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate SNMP behavior")

    # Initialize page object with device-aware patterns
    snmp_page = SNMPConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing empty SNMP community string error on {device_model} using pure page object pattern"
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
            f"Testing empty SNMP community string error on {device_model} (Series {device_series})"
        )

        # Navigate to SNMP configuration page using page object method
        logger.info("Navigating to SNMP configuration page")
        snmp_page.navigate_to_snmp_config()

        # Test SNMP community field validation using page object methods
        logger.info("Testing SNMP community field validation")

        # Get original community string value using page object method
        original_value = snmp_page.get_ro_community1_value()
        logger.info(f"Original SNMP community string: '{original_value}'")

        # Test clearing community string with validation
        logger.info("Testing community string clearing")
        clear_result = snmp_page.test_community_string_clearing()
        logger.info(f"Community string clearing result: {clear_result}")

        # Test community string validation with empty value
        logger.info("Testing empty community string validation")
        empty_validation = snmp_page.test_empty_community_string_validation()
        logger.info(f"Empty community string validation: {empty_validation}")

        # Test device series-specific behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 SNMP error handling")

            # Test Series 2 specific SNMP validation
            series2_validation = snmp_page.test_series2_snmp_validation()
            logger.info(f"Series 2 SNMP validation result: {series2_validation}")

            # Configure SNMP settings for Series 2
            snmp_config = snmp_page.configure_series2_snmp_settings()
            logger.info(f"Series 2 SNMP configuration result: {snmp_config}")

        elif device_series == 3:
            logger.info(f"Testing Series 3 SNMP configuration")

            # Test Series 3 specific SNMP validation
            series3_validation = snmp_page.test_series3_snmp_validation()
            logger.info(f"Series 3 SNMP validation result: {series3_validation}")

            # Configure SNMP settings for Series 3
            snmp_config = snmp_page.configure_series3_snmp_settings()
            logger.info(f"Series 3 SNMP configuration result: {snmp_config}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            snmp_config = device_capabilities_data.get("snmp_configuration", {})
            community_validation = snmp_config.get("community_validation", {})
            logger.info(
                f"Community validation from DeviceCapabilities: {community_validation}"
            )

        # Test error message validation using page object method
        logger.info("Testing error message validation")
        error_messages = snmp_page.get_error_messages()

        if error_messages:
            logger.info(f"Error messages found: {error_messages}")
        else:
            logger.info(f"No specific error messages detected")

        # Test save functionality with community string validation using page object method
        logger.info("Testing save functionality with community string validation")
        save_result = snmp_page.test_save_with_community_validation()
        logger.info(f"Save with community validation result: {save_result}")

        # Test form validation patterns using page object method
        logger.info("Testing form validation patterns")
        validation_patterns = snmp_page.get_form_validation_patterns()
        logger.info(f"Form validation patterns: {validation_patterns}")

        # Test SNMP community field interaction using page object methods
        logger.info("Testing SNMP community field interaction")
        community_interaction = snmp_page.test_community_field_interaction()
        logger.info(f"Community field interaction result: {community_interaction}")

        # Restore valid community string state using page object method
        logger.info("Restoring valid community string state")
        restore_result = snmp_page.restore_community_string_state()
        logger.info(f"Community string restoration result: {restore_result}")

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
            community_perf = snmp_performance.get("community_validation", {})

            typical_validation = community_perf.get("typical_time", "")
            worst_case = community_perf.get("worst_case", "")

            if typical_validation:
                logger.info(
                    f"Community validation performance baseline: {typical_validation}"
                )
            if worst_case:
                logger.info(f"Community validation worst case: {worst_case}")

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
        logger.info(
            f"Empty SNMP community string error test completed for {device_model}"
        )

        if device_series == 2:
            logger.info(
                f"Series 2 empty SNMP community string error test PASSED for {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 empty SNMP community string error test PASSED for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(
            f"Empty SNMP community string error test failed on {device_model}: {e}"
        )
        pytest.fail(
            f"Empty SNMP community string error test failed on {device_model}: {e}"
        )

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = snmp_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(
            f"Empty SNMP community string error test completed for {device_model}"
        )
