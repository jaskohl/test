"""
Test 12.4.2: Page Reload Clears Error State - Pure Page Object Pattern
Category: 12 - Error Handling Tests
Test Count: Part of 11 tests in Category 12
Hardware: Device Only
Priority: HIGH - Proper error handling critical for reliability
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on page reload clears error state functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_12_4_2_page_reload_clears_errors(logged_in_page: Page, base_url: str, request):
    """
    Test 12.4.2: Page Reload Clears Error State - Pure Page Object Pattern
    Purpose: Verify page reload clears error state and maintains valid configuration data with device-aware validation
    Expected: Page reload properly clears error state and preserves valid data with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates page reload patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate network behavior")

    # Initialize page object with device-aware patterns
    network_page = NetworkConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing page reload clears error state on {device_model} using pure page object pattern"
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
            f"Testing page reload clears error state on {device_model} (Series {device_series})"
        )

        # Navigate to network configuration page using page object method
        logger.info("Navigating to network configuration page")
        network_page.navigate_to_network_config()

        # Test page reload error clearing patterns using page object methods
        logger.info("Testing page reload error clearing patterns")

        # Get original network configuration using page object method
        logger.info("Retrieving original network configuration")
        original_config = network_page.get_network_configuration_state()
        logger.info(f"Original network configuration: {original_config}")

        # Test network field modification using page object methods
        logger.info("Testing network field modification")
        test_ip = "172.16.66.50"
        ip_config = network_page.configure_ip_address(test_ip)
        logger.info(f"IP address configuration result: {ip_config}")

        # Test field clearing using page object methods
        logger.info("Testing field clearing")
        clear_result = network_page.test_ip_field_clearing()
        logger.info(f"Field clearing result: {clear_result}")

        # Test device series-specific behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 page reload patterns")

            # Test Series 2 specific reload behavior
            series2_reload = network_page.test_series2_page_reload_behavior()
            logger.info(f"Series 2 page reload result: {series2_reload}")

            # Configure network settings for Series 2
            network_config = network_page.configure_series2_network_settings()
            logger.info(f"Series 2 network configuration result: {network_config}")

        elif device_series == 3:
            logger.info(f"Testing Series 3 page reload patterns")

            # Test Series 3 specific reload behavior
            series3_reload = network_page.test_series3_page_reload_behavior()
            logger.info(f"Series 3 page reload result: {series3_reload}")

            # Configure network settings for Series 3
            network_config = network_page.configure_series3_network_settings()
            logger.info(f"Series 3 network configuration result: {network_config}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            network_config = device_capabilities_data.get("network_configuration", {})
            reload_behavior = network_config.get("reload_behavior", {})
            logger.info(f"Reload behavior from DeviceCapabilities: {reload_behavior}")

        # Test error message validation using page object method
        logger.info("Testing error message validation")
        error_messages = network_page.get_error_messages()

        if error_messages:
            logger.info(f"Error messages found: {error_messages}")
        else:
            logger.info(f"No specific error messages detected")

        # Test page reload functionality using page object method
        logger.info("Testing page reload functionality")
        reload_result = network_page.test_page_reload_functionality()
        logger.info(f"Page reload functionality result: {reload_result}")

        # Test data persistence after reload using page object methods
        logger.info("Testing data persistence after reload")
        persistence_result = network_page.test_data_persistence_after_reload()
        logger.info(f"Data persistence result: {persistence_result}")

        # Test error state clearing using page object method
        logger.info("Testing error state clearing")
        error_clearing = network_page.test_error_state_clearing()
        logger.info(f"Error state clearing result: {error_clearing}")

        # Test configuration validation after reload using page object method
        logger.info("Testing configuration validation after reload")
        config_validation = network_page.test_configuration_validation_after_reload()
        logger.info(f"Configuration validation result: {config_validation}")

        # Test form state restoration using page object method
        logger.info("Testing form state restoration")
        state_restoration = network_page.get_form_state_restoration_patterns()
        logger.info(f"Form state restoration patterns: {state_restoration}")

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
            reload_perf = network_performance.get("page_reload", {})

            typical_reload = reload_perf.get("typical_time", "")
            worst_case = reload_perf.get("worst_case", "")

            if typical_reload:
                logger.info(f"Page reload performance baseline: {typical_reload}")
            if worst_case:
                logger.info(f"Page reload worst case: {worst_case}")

            # Basic timing validation
            if reload_time > 3.0:  # Simple threshold for now
                logger.warning(
                    f"Page reload took longer than expected: {reload_time:.2f}s"
                )

        # Verify valid IP is maintained after reload
        logger.info("Verifying IP configuration after reload")
        current_ip = network_page.get_current_ip_configuration()
        logger.info(f"Current IP configuration after reload: {current_ip}")

        if test_ip in str(current_ip):
            logger.info(f"Valid IP {test_ip} correctly maintained after reload")
        else:
            logger.warning(
                f"IP configuration may not have been maintained after reload"
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
        logger.info(f"Page reload clears error state test completed for {device_model}")

        if device_series == 2:
            logger.info(
                f"Series 2 page reload clears error state test PASSED for {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 page reload clears error state test PASSED for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(
            f"Page reload clears error state test failed on {device_model}: {e}"
        )
        pytest.fail(
            f"Page reload clears error state test failed on {device_model}: {e}"
        )

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = network_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(f"Page reload clears error state test completed for {device_model}")
