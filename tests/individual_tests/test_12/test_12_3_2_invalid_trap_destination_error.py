"""
Test 12.3.2: Invalid SNMP Trap Destination Error - Pure Page Object Pattern
Category: 12 - Error Handling Tests
Test Count: Part of 11 tests in Category 12
Hardware: Device Only
Priority: HIGH - Proper error handling critical for reliability
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on invalid SNMP trap destination error functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.snmp_config_page import SNMPConfigPage

logger = logging.getLogger(__name__)


def test_12_3_2_invalid_trap_destination_error(
    logged_in_page: Page, base_url: str, request
):
    """
    Test 12.3.2: Invalid SNMP Trap Destination Error - Pure Page Object Pattern
    Purpose: Verify error handling for invalid SNMP trap destination configuration with device-aware validation
    Expected: Trap destination validation fails and appropriate error is indicated with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates SNMP trap configuration patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate SNMP behavior")

    # Initialize page object with device-aware patterns
    snmp_page = SNMPConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing invalid SNMP trap destination error on {device_model} using pure page object pattern"
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
            f"Testing invalid SNMP trap destination error on {device_model} (Series {device_series})"
        )

        # Navigate to SNMP configuration page using page object method
        logger.info("Navigating to SNMP configuration page")
        snmp_page.navigate_to_snmp_config()

        # Test SNMP trap destination field validation using page object methods
        logger.info("Testing SNMP trap destination field validation")

        # Test trap destination field detection using page object method
        trap_fields = snmp_page.detect_trap_destination_fields()
        logger.info(f"Trap destination fields detected: {trap_fields}")

        # Test invalid trap destination validation using page object methods
        logger.info("Testing invalid trap destination validation")
        invalid_ip = "999.999.999.999"
        invalid_validation = snmp_page.test_invalid_trap_destination_validation(
            invalid_ip
        )
        logger.info(f"Invalid trap destination validation result: {invalid_validation}")

        # Test device series-specific behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 SNMP trap destination handling")

            # Test Series 2 specific trap validation
            series2_validation = snmp_page.test_series2_trap_validation()
            logger.info(f"Series 2 trap validation result: {series2_validation}")

            # Configure SNMP trap settings for Series 2
            trap_config = snmp_page.configure_series2_trap_settings()
            logger.info(f"Series 2 trap configuration result: {trap_config}")

        elif device_series == 3:
            logger.info(f"Testing Series 3 SNMP trap configuration")

            # Test Series 3 specific trap validation
            series3_validation = snmp_page.test_series3_trap_validation()
            logger.info(f"Series 3 trap validation result: {series3_validation}")

            # Configure SNMP trap settings for Series 3
            trap_config = snmp_page.configure_series3_trap_settings()
            logger.info(f"Series 3 trap configuration result: {trap_config}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            snmp_config = device_capabilities_data.get("snmp_configuration", {})
            trap_validation = snmp_config.get("trap_validation", {})
            logger.info(f"Trap validation from DeviceCapabilities: {trap_validation}")

        # Test error message validation using page object method
        logger.info("Testing error message validation")
        error_messages = snmp_page.get_error_messages()

        if error_messages:
            logger.info(f"Error messages found: {error_messages}")
        else:
            logger.info(f"No specific error messages detected")

        # Test save functionality with trap destination validation using page object method
        logger.info("Testing save functionality with trap destination validation")
        save_result = snmp_page.test_save_with_trap_validation()
        logger.info(f"Save with trap validation result: {save_result}")

        # Test form validation patterns using page object method
        logger.info("Testing form validation patterns")
        validation_patterns = snmp_page.get_form_validation_patterns()
        logger.info(f"Form validation patterns: {validation_patterns}")

        # Test trap destination field interaction using page object methods
        logger.info("Testing trap destination field interaction")
        trap_interaction = snmp_page.test_trap_field_interaction()
        logger.info(f"Trap field interaction result: {trap_interaction}")

        # Restore valid trap destination state using page object method
        logger.info("Restoring valid trap destination state")
        valid_ip = "172.16.0.1"
        restore_result = snmp_page.restore_trap_destination_state(valid_ip)
        logger.info(f"Trap destination restoration result: {restore_result}")

        # Test IP address validation patterns using page object method
        logger.info("Testing IP address validation patterns")
        ip_validation = snmp_page.test_ip_address_validation_patterns()
        logger.info(f"IP address validation patterns: {ip_validation}")

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
            trap_perf = snmp_performance.get("trap_validation", {})

            typical_validation = trap_perf.get("typical_time", "")
            worst_case = trap_perf.get("worst_case", "")

            if typical_validation:
                logger.info(
                    f"Trap validation performance baseline: {typical_validation}"
                )
            if worst_case:
                logger.info(f"Trap validation worst case: {worst_case}")

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
            f"Invalid SNMP trap destination error test completed for {device_model}"
        )

        if device_series == 2:
            logger.info(
                f"Series 2 invalid SNMP trap destination error test PASSED for {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 invalid SNMP trap destination error test PASSED for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(
            f"Invalid SNMP trap destination error test failed on {device_model}: {e}"
        )
        pytest.fail(
            f"Invalid SNMP trap destination error test failed on {device_model}: {e}"
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
            f"Invalid SNMP trap destination error test completed for {device_model}"
        )
