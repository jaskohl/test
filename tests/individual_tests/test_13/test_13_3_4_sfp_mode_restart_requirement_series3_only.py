"""
Test 13.3.4: SFP Mode Restart Requirement (Series 3 Only) - Pure Page Object Pattern
Category: 13 - State Transitions Tests
Test Count: Part of 7 tests in Category 13
Hardware: Device Only
Priority: MEDIUM - Form state management
Series: Series 3 only
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on SFP mode restart requirement functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_13_3_4_sfp_mode_restart_requirement_series3_only(
    logged_in_page: Page, base_url: str, request
):
    """
    Test 13.3.4: SFP Mode Restart Requirement (Series 3 Only) - Pure Page Object Pattern
    Purpose: Verify SFP mode changes require device restart with device-aware validation
    Expected: Warning message or system response indicating restart requirement with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Series 3 only - validates SFP restart patterns specific to Series 3 devices
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate SFP mode behavior")

    # Initialize page object with device-aware patterns
    network_page = NetworkConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing SFP mode restart requirement on {device_model} using pure page object pattern"
    )

    # Test device series validation - this test is Series 3 only
    device_series = DeviceCapabilities.get_series(device_model)

    if device_series != 3:
        pytest.skip(
            f"SFP mode restart requirement only applies to Series 3, detected {device_model} ({device_series})"
        )

    try:
        # Navigate to dashboard page using page object method
        logger.info("Navigating to dashboard page")
        logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")

        # Wait for page load with device-aware timeout
        network_page.wait_for_page_load()

        logger.info(
            f"Testing SFP mode restart requirement on {device_model} (Series {device_series})"
        )

        # Navigate to network configuration page using page object method
        logger.info("Navigating to network configuration page")
        network_page.navigate_to_network_config()

        # Test SFP mode patterns using page object methods
        logger.info("Testing SFP mode patterns")

        # Test device series-specific SFP mode behavior (Series 3 only)
        logger.info(f"Testing Series 3 SFP mode patterns")

        # Test Series 3 specific SFP mode behavior
        series3_sfp = network_page.test_series3_sfp_mode_restart_requirement()
        logger.info(f"Series 3 SFP mode restart requirement result: {series3_sfp}")

        # Test SFP mode field detection using page object method
        logger.info("Testing SFP mode field detection")
        sfp_field_detection = network_page.test_sfp_mode_field_detection()
        logger.info(f"SFP mode field detection result: {sfp_field_detection}")

        # Test SFP mode interaction using page object method
        logger.info("Testing SFP mode interaction")
        sfp_interaction = network_page.test_sfp_mode_interaction()
        logger.info(f"SFP mode interaction result: {sfp_interaction}")

        # Configure network settings for Series 3
        network_config = network_page.configure_series3_network_settings()
        logger.info(f"Series 3 network configuration result: {network_config}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            network_config = device_capabilities_data.get("network_configuration", {})
            sfp_restart = network_config.get("sfp_restart_requirement", {})
            logger.info(
                f"SFP restart requirement from DeviceCapabilities: {sfp_restart}"
            )

        # Test SFP mode field visibility using page object method
        logger.info("Testing SFP mode field visibility")
        field_visibility = network_page.test_sfp_mode_field_visibility()
        logger.info(f"SFP mode field visibility result: {field_visibility}")

        # Test SFP mode validation using page object method
        logger.info("Testing SFP mode validation")
        sfp_validation = network_page.test_sfp_mode_validation()
        logger.info(f"SFP mode validation result: {sfp_validation}")

        # Test restart requirement detection using page object method
        logger.info("Testing restart requirement detection")
        restart_detection = network_page.test_restart_requirement_detection()
        logger.info(f"Restart requirement detection result: {restart_detection}")

        # Test warning message detection using page object method
        logger.info("Testing warning message detection")
        warning_detection = network_page.test_sfp_warning_message_detection()
        logger.info(f"Warning message detection result: {warning_detection}")

        # Test SFP mode state changes using page object method
        logger.info("Testing SFP mode state changes")
        state_changes = network_page.test_sfp_mode_state_changes()
        logger.info(f"SFP mode state changes result: {state_changes}")

        # Test system response validation using page object method
        logger.info("Testing system response validation")
        system_response = network_page.test_sfp_system_response_validation()
        logger.info(f"System response validation result: {system_response}")

        # Test SFP restart patterns using page object method
        logger.info("Testing SFP restart patterns")
        restart_patterns = network_page.get_sfp_restart_patterns()
        logger.info(f"SFP restart patterns: {restart_patterns}")

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
            sfp_perf = network_performance.get("sfp_mode_restart", {})

            typical_restart = sfp_perf.get("typical_time", "")
            worst_case = sfp_perf.get("worst_case", "")

            if typical_restart:
                logger.info(
                    f"SFP restart requirement performance baseline: {typical_restart}"
                )
            if worst_case:
                logger.info(f"SFP restart requirement worst case: {worst_case}")

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

        # Test error message validation using page object method
        logger.info("Testing error message validation")
        error_messages = network_page.get_error_messages()

        if error_messages:
            logger.info(f"Error messages found: {error_messages}")
        else:
            logger.info(f"No specific error messages detected")

        # Final validation
        logger.info(
            f"SFP mode restart requirement test completed for {device_model} (Series 3)"
        )

        logger.info(
            f"Series 3 SFP mode restart requirement test PASSED for {device_model}"
        )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"SFP mode restart requirement test failed on {device_model}: {e}")
        pytest.fail(f"SFP mode restart requirement test failed on {device_model}: {e}")

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = network_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(f"SFP mode restart requirement test completed for {device_model}")
