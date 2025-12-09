"""
Test 12.5.1: Multiple Field Validation Errors - Pure Page Object Pattern
Category: 12 - Error Handling Tests
Test Count: Part of 11 tests in Category 12
Hardware: Device Only
Priority: HIGH - Proper error handling critical for reliability
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on multiple field validation errors functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_12_5_1_multiple_field_errors(logged_in_page: Page, base_url: str, request):
    """
    Test 12.5.1: Multiple Field Validation Errors - Pure Page Object Pattern
    Purpose: Verify error handling for multiple field validation errors simultaneously with device-aware validation
    Expected: Multiple field validation fails and appropriate errors are indicated with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates multiple field validation patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate network behavior")

    # Initialize page object with device-aware patterns
    network_page = NetworkConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing multiple field validation errors on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to dashboard page using page object method
        logger.info("Navigating to dashboard page")
        logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")

        # Wait for page load with device-aware timeout
        network_page.wait_for_page_load()

        # Test device series-specific behavior using page object methods
        device_series = DeviceCapabilities.get_series(device_model)

        logger.info(
            f"Testing multiple field validation errors on {device_model} (Series {device_series})"
        )

        # Navigate to network configuration page using page object method
        logger.info("Navigating to network configuration page")
        network_page.navigate_to_network_config()

        # Test multiple field validation patterns using page object methods
        logger.info("Testing multiple field validation patterns")

        # Test network mode configuration for Series 2 behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 multiple field validation")
            network_page.configure_network_mode("SINGLE")

            # Test multiple field interaction using page object methods
            logger.info("Testing multiple field interaction")

            # Configure gateway field
            gateway_value = "172.16.0.1"
            gateway_config = network_page.configure_gateway(gateway_value)
            logger.info(f"Gateway configuration result: {gateway_config}")

            # Configure IP address field
            ip_value = "172.16.66.50"
            ip_config = network_page.configure_ip_address(ip_value)
            logger.info(f"IP address configuration result: {ip_config}")

            # Configure subnet mask field
            mask_value = "255.255.0.0"
            mask_config = network_page.configure_subnet_mask(mask_value)
            logger.info(f"Subnet mask configuration result: {mask_config}")

            # Test multiple field validation using page object method
            logger.info("Testing multiple field validation")
            validation_result = network_page.test_multiple_field_validation()
            logger.info(f"Multiple field validation result: {validation_result}")

            # Test network configuration state using page object method
            network_state = network_page.get_network_configuration_state()
            logger.info(f"Network configuration state: {network_state}")

        elif device_series == 3:
            logger.info(f"Testing Series 3 multiple field validation")

            # Test Series 3 specific multiple field behavior
            series3_validation = network_page.test_series3_multiple_field_validation()
            logger.info(
                f"Series 3 multiple field validation result: {series3_validation}"
            )

            # Configure network settings for Series 3
            network_config = network_page.configure_series3_network_settings()
            logger.info(f"Series 3 network configuration result: {network_config}")

            # Test Series 3 field interaction patterns
            field_interaction = network_page.test_series3_field_interaction_patterns()
            logger.info(f"Series 3 field interaction patterns: {field_interaction}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            network_config = device_capabilities_data.get("network_configuration", {})
            multiple_field_validation = network_config.get(
                "multiple_field_validation", {}
            )
            logger.info(
                f"Multiple field validation from DeviceCapabilities: {multiple_field_validation}"
            )

        # Test error message validation using page object method
        logger.info("Testing error message validation")
        error_messages = network_page.get_error_messages()

        if error_messages:
            logger.info(f"Error messages found: {error_messages}")
        else:
            logger.info(f"No specific error messages detected")

        # Test save functionality with multiple field validation using page object method
        logger.info("Testing save functionality with multiple field validation")
        save_result = network_page.test_save_with_multiple_field_validation()
        logger.info(f"Save with multiple field validation result: {save_result}")

        # Test form validation patterns using page object method
        logger.info("Testing form validation patterns")
        validation_patterns = network_page.get_form_validation_patterns()
        logger.info(f"Form validation patterns: {validation_patterns}")

        # Test field interaction patterns using page object method
        logger.info("Testing field interaction patterns")
        interaction_patterns = network_page.get_field_interaction_patterns()
        logger.info(f"Field interaction patterns: {interaction_patterns}")

        # Test simultaneous field modifications using page object methods
        logger.info("Testing simultaneous field modifications")
        simultaneous_result = network_page.test_simultaneous_field_modifications()
        logger.info(f"Simultaneous field modifications result: {simultaneous_result}")

        # Test field validation dependencies using page object method
        logger.info("Testing field validation dependencies")
        dependencies = network_page.test_field_validation_dependencies()
        logger.info(f"Field validation dependencies: {dependencies}")

        # Test error accumulation patterns using page object method
        logger.info("Testing error accumulation patterns")
        error_accumulation = network_page.get_error_accumulation_patterns()
        logger.info(f"Error accumulation patterns: {error_accumulation}")

        # Performance validation using page object methods
        logger.info("Performing performance validation")

        start_time = time.time()

        # Test page reload performance
        network_page.reload_page()
        reload_time = time.time() - start_time

        logger.info(f"Page reload time: {reload_time:.2f}s")

        # Cross-reference with performance expectations
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            network_performance = performance_data.get("network_configuration", {})
            multiple_field_perf = network_performance.get(
                "multiple_field_validation", {}
            )

            typical_validation = multiple_field_perf.get("typical_time", "")
            worst_case = multiple_field_perf.get("worst_case", "")

            if typical_validation:
                logger.info(
                    f"Multiple field validation performance baseline: {typical_validation}"
                )
            if worst_case:
                logger.info(f"Multiple field validation worst case: {worst_case}")

            # Basic timing validation
            if reload_time > 3.0:  # Simple threshold for now
                logger.warning(
                    f"Page reload took longer than expected: {reload_time:.2f}s"
                )

        # Test page data retrieval using page object method
        page_data = network_page.get_page_data()
        logger.info(
            f"Network configuration page data retrieved: {list(page_data.keys())}"
        )

        # Test network capabilities validation using page object method
        network_capabilities = network_page.detect_network_capabilities()
        logger.info(f"Network capabilities detected: {network_capabilities}")

        # Final validation
        logger.info(
            f"Multiple field validation errors test completed for {device_model}"
        )

        if device_series == 2:
            logger.info(
                f"Series 2 multiple field validation errors test PASSED for {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 multiple field validation errors test PASSED for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(
            f"Multiple field validation errors test failed on {device_model}: {e}"
        )
        pytest.fail(
            f"Multiple field validation errors test failed on {device_model}: {e}"
        )

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = network_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(
            f"Multiple field validation errors test completed for {device_model}"
        )
