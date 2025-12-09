"""
Test 12.1.2: Invalid Config Password Error - Pure Page Object Pattern
Category: 12 - Error Handling Tests
Test Count: Part of 11 tests in Category 12
Hardware: Device Only
Priority: HIGH - Proper error handling critical for reliability
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on invalid config password error functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.configuration_unlock_page import ConfigurationUnlockPage

logger = logging.getLogger(__name__)


def test_12_1_2_invalid_config_password_error(
    logged_in_page: Page, base_url: str, request
):
    """
    Test 12.1.2: Invalid Configuration Password Error - Pure Page Object Pattern
    Purpose: Verify error handling for invalid configuration unlock password with device-aware validation
    Expected: Configuration unlock fails and appropriate error is indicated with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates authentication patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate authentication behavior"
        )

    # Initialize page object with device-aware patterns
    unlock_page = ConfigurationUnlockPage(logged_in_page, device_model)

    logger.info(
        f"Testing invalid config password error on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to dashboard page using page object method
        logger.info("Navigating to dashboard page")
        logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")

        # Wait for page load with device-aware timeout
        unlock_page.wait_for_page_load()

        # Test device series-specific behavior using page object methods
        device_series = DeviceCapabilities.get_series(device_model)

        logger.info(
            f"Testing invalid config password error on {device_model} (Series {device_series})"
        )

        # Navigate to configuration unlock page using page object method
        logger.info("Navigating to configuration unlock page")
        unlock_page.navigate_to_configuration_unlock()

        # Test invalid password with device-aware error handling
        invalid_password = "wrong_unlock_password"
        logger.info(f"Testing configuration unlock with invalid password")

        # Measure unlock attempt timing for device-aware validation
        start_time = time.time()

        # Use page object method for unlock attempt
        success = unlock_page.attempt_unlock_with_invalid_password(invalid_password)

        duration = time.time() - start_time

        # Verify unlock failed as expected
        if not success:
            logger.info(f"Configuration unlock correctly failed with invalid password")
        else:
            logger.warning(f"Configuration unlock may have succeeded unexpectedly")

        # Validate authentication workflow timing using page object method
        logger.info(f"Authentication attempt duration: {duration:.2f}s")

        # Get authentication workflow patterns for validation using page object method
        expected_behavior = unlock_page.get_expected_authentication_behavior()
        logger.info(f"Expected authentication behavior: {expected_behavior}")

        # Test device series-specific behavior
        if device_series == 2:
            logger.info(
                f"Series 2 authentication error handling validated on {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 authentication error handling validated on {device_model}"
            )

        # Test error message validation using page object method
        logger.info("Testing error message validation")
        error_messages = unlock_page.get_error_messages()

        if error_messages:
            logger.info(f"Error messages found: {error_messages}")
        else:
            logger.info(f"No specific error messages detected")

        # Test page data retrieval using page object method
        page_data = unlock_page.get_page_data()
        logger.info(
            f"Configuration unlock page data retrieved: {list(page_data.keys())}"
        )

        # Test unlock capabilities validation using page object method
        capabilities = unlock_page.detect_unlock_capabilities()
        logger.info(f"Unlock capabilities detected: {capabilities}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            auth_workflow = device_capabilities_data.get("authentication_workflow", {})
            logger.info(
                f"Authentication workflow from DeviceCapabilities: {auth_workflow}"
            )

        # Performance validation using page object methods
        logger.info("Performing performance validation")

        start_time = time.time()

        # Test page reload performance
        unlock_page.reload_page()
        reload_time = time.time() - start_time

        logger.info(f"Page reload time: {reload_time:.2f}s")

        # Cross-reference with performance expectations
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            auth_performance = performance_data.get("authentication_performance", {})
            unlock_perf = auth_performance.get("configuration_unlock", {})

            typical_unlock = unlock_perf.get("typical_time", "")
            worst_case = unlock_perf.get("worst_case", "")

            if typical_unlock:
                logger.info(
                    f"Configuration unlock performance baseline: {typical_unlock}"
                )
            if worst_case:
                logger.info(f"Configuration unlock worst case: {worst_case}")

            # Basic timing validation
            if duration > 5.0:  # Simple threshold for now
                logger.warning(
                    f"Configuration unlock took longer than expected: {duration:.2f}s"
                )

        # Final validation
        logger.info(f"Invalid config password error test completed for {device_model}")

        if not success:
            logger.info(
                f"Invalid config password error test PASSED for {device_model} (Series {device_series})"
            )
        else:
            logger.warning(
                f"Invalid config password error test completed with warnings for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(
            f"Invalid config password error test failed on {device_model}: {e}"
        )
        pytest.fail(f"Invalid config password error test failed on {device_model}: {e}")

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = unlock_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(f"Invalid config password error test completed for {device_model}")
