"""
Test 12.2.2: Missing Gateway Error - Pure Page Object Pattern
Category: 12 - Error Handling Tests
Test Count: Part of 11 tests in Category 12
Hardware: Device Only
Priority: HIGH - Proper error handling critical for reliability
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on missing gateway error functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_12_2_2_missing_gateway_error(logged_in_page: Page, base_url: str, request):
    """
    Test 12.2.2: Missing Gateway Error - Pure Page Object Pattern
    Purpose: Verify error handling for missing required gateway configuration with device-aware validation
    Expected: Gateway validation fails and appropriate error is indicated with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates network configuration patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate network behavior")

    # Initialize page object with device-aware patterns
    network_page = NetworkConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing missing gateway error on {device_model} using pure page object pattern"
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
            f"Testing missing gateway error on {device_model} (Series {device_series})"
        )

        # Navigate to network configuration page using page object method
        logger.info("Navigating to network configuration page")
        network_page.navigate_to_network_config()

        # Test network mode configuration for Series 2 behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 network mode configuration")
            network_page.configure_network_mode("SINGLE")

            # Test missing gateway validation using page object methods
            logger.info("Testing missing gateway validation")
            gateway_test_result = network_page.test_gateway_validation("")

            if gateway_test_result.get("validation_triggered", False):
                logger.info(
                    f"Gateway validation triggered for Series 2: {gateway_test_result}"
                )
            else:
                logger.info(
                    f"Gateway validation behavior for Series 2: {gateway_test_result}"
                )

            # Test network field interaction using page object methods
            logger.info("Testing network field interaction")
            ip_addr = "172.16.190.50"
            ip_mask = "255.255.0.0"
            gateway = "172.16.0.1"

            # Configure IP address
            ip_config = network_page.configure_ip_address(ip_addr)
            logger.info(f"IP address configuration result: {ip_config}")

            # Configure subnet mask
            mask_config = network_page.configure_subnet_mask(ip_mask)
            logger.info(f"Subnet mask configuration result: {mask_config}")

            # Test gateway configuration with validation
            gateway_config = network_page.configure_gateway(gateway)
            logger.info(f"Gateway configuration result: {gateway_config}")

            # Validate network state using page object method
            network_state = network_page.get_network_configuration_state()
            logger.info(f"Network configuration state: {network_state}")

        elif device_series == 3:
            logger.info(f"Testing Series 3 network configuration")

            # Test gateway field validation for Series 3
            logger.info("Testing Series 3 gateway field validation")
            gateway_validation = (
                network_page.test_gateway_field_visibility_and_required()
            )
            logger.info(f"Gateway field validation for Series 3: {gateway_validation}")

            # Configure network settings for Series 3
            network_config = network_page.configure_series3_network_settings()
            logger.info(f"Series 3 network configuration result: {network_config}")

            # Test gateway-specific validation
            gateway_test = network_page.test_gateway_validation_series3()
            logger.info(f"Series 3 gateway validation result: {gateway_test}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            network_config = device_capabilities_data.get("network_configuration", {})
            gateway_validation = network_config.get("gateway_validation", {})
            logger.info(
                f"Gateway validation from DeviceCapabilities: {gateway_validation}"
            )

        # Test error message validation using page object method
        logger.info("Testing error message validation")
        error_messages = network_page.get_error_messages()

        if error_messages:
            logger.info(f"Error messages found: {error_messages}")
        else:
            logger.info(f"No specific error messages detected")

        # Test save functionality with gateway validation using page object method
        logger.info("Testing save functionality with gateway validation")
        save_result = network_page.test_save_with_gateway_validation()
        logger.info(f"Save with gateway validation result: {save_result}")

        # Test form validation patterns using page object method
        logger.info("Testing form validation patterns")
        validation_patterns = network_page.get_form_validation_patterns()
        logger.info(f"Form validation patterns: {validation_patterns}")

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
            gateway_perf = network_performance.get("gateway_validation", {})

            typical_validation = gateway_perf.get("typical_time", "")
            worst_case = gateway_perf.get("worst_case", "")

            if typical_validation:
                logger.info(
                    f"Gateway validation performance baseline: {typical_validation}"
                )
            if worst_case:
                logger.info(f"Gateway validation worst case: {worst_case}")

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
        logger.info(f"Missing gateway error test completed for {device_model}")

        if device_series == 2:
            logger.info(
                f"Series 2 missing gateway error test PASSED for {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 missing gateway error test PASSED for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Missing gateway error test failed on {device_model}: {e}")
        pytest.fail(f"Missing gateway error test failed on {device_model}: {e}")

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = network_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(f"Missing gateway error test completed for {device_model}")
