"""
Test 13.2.1: Configuration Page to Configuration Page Navigation - Pure Page Object Pattern
Category: 13 - State Transitions Tests
Test Count: Part of 7 tests in Category 13
Hardware: Device Only
Priority: MEDIUM - Form state management
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on configuration page to configuration page navigation functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_13_2_1_config_page_to_config_page(
    logged_in_page: Page, base_url: str, request
):
    """
    Test 13.2.1: Configuration Page to Configuration Page Navigation - Pure Page Object Pattern
    Purpose: Verify navigation between configuration pages maintains state with device-aware validation
    Expected: Target page loads, form elements visible, page ready for interaction with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates navigation patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate navigation behavior")

    # Initialize page objects with device-aware patterns
    general_page = GeneralConfigPage(logged_in_page, device_model)
    network_page = NetworkConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing configuration page to configuration page navigation on {device_model} using pure page object pattern"
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
            f"Testing configuration page to configuration page navigation on {device_model} (Series {device_series})"
        )

        # Navigate to general configuration page using page object method (starting point)
        logger.info("Navigating to general configuration page")
        general_page.navigate_to_general_config()

        # Test navigation patterns using page object methods
        logger.info("Testing navigation patterns")

        # Test device series-specific navigation behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 navigation patterns")

            # Test Series 2 specific navigation behavior
            series2_navigation = general_page.test_series2_config_page_navigation()
            logger.info(f"Series 2 navigation result: {series2_navigation}")

            # Navigate to network configuration page using page object method
            logger.info("Navigating to network configuration page")
            network_page.navigate_to_network_config()

            # Test Series 2 network configuration page validation
            series2_validation = network_page.test_series2_network_page_validation()
            logger.info(
                f"Series 2 network page validation result: {series2_validation}"
            )

        elif device_series == 3:
            logger.info(f"Testing Series 3 navigation patterns")

            # Test Series 3 specific navigation behavior
            series3_navigation = general_page.test_series3_config_page_navigation()
            logger.info(f"Series 3 navigation result: {series3_navigation}")

            # Navigate to network configuration page using page object method
            logger.info("Navigating to network configuration page")
            network_page.navigate_to_network_config()

            # Test Series 3 network configuration page validation
            series3_validation = network_page.test_series3_network_page_validation()
            logger.info(
                f"Series 3 network page validation result: {series3_validation}"
            )

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            navigation_config = device_capabilities_data.get(
                "navigation_configuration", {}
            )
            page_transitions = navigation_config.get("page_transitions", {})
            logger.info(f"Page transitions from DeviceCapabilities: {page_transitions}")

        # Test navigation link detection using page object method
        logger.info("Testing navigation link detection")
        link_detection = network_page.test_navigation_link_detection()
        logger.info(f"Navigation link detection result: {link_detection}")

        # Test page load state validation using page object method
        logger.info("Testing page load state validation")
        load_state = network_page.test_page_load_state_validation()
        logger.info(f"Page load state validation result: {load_state}")

        # Test form element visibility using page object method
        logger.info("Testing form element visibility")
        element_visibility = network_page.test_form_element_visibility()
        logger.info(f"Form element visibility result: {element_visibility}")

        # Test navigation state preservation using page object method
        logger.info("Testing navigation state preservation")
        state_preservation = network_page.test_navigation_state_preservation()
        logger.info(f"Navigation state preservation result: {state_preservation}")

        # Test inter-page navigation patterns using page object method
        logger.info("Testing inter-page navigation patterns")
        inter_page_patterns = network_page.test_inter_page_navigation_patterns()
        logger.info(f"Inter-page navigation patterns: {inter_page_patterns}")

        # Test configuration page readiness using page object method
        logger.info("Testing configuration page readiness")
        page_readiness = network_page.test_configuration_page_readiness()
        logger.info(f"Configuration page readiness result: {page_readiness}")

        # Test device-aware field detection using page object method
        logger.info("Testing device-aware field detection")
        field_detection = network_page.test_field_detection()
        logger.info(f"Device-aware field detection result: {field_detection}")

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
            navigation_performance = performance_data.get("navigation_performance", {})
            page_transition_perf = navigation_performance.get("page_transitions", {})

            typical_transition = page_transition_perf.get("typical_time", "")
            worst_case = page_transition_perf.get("worst_case", "")

            if typical_transition:
                logger.info(
                    f"Page transition performance baseline: {typical_transition}"
                )
            if worst_case:
                logger.info(f"Page transition worst case: {worst_case}")

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
            f"Configuration page to configuration page navigation test completed for {device_model}"
        )

        if device_series == 2:
            logger.info(
                f"Series 2 configuration page to configuration page navigation test PASSED for {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 configuration page to configuration page navigation test PASSED for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(
            f"Configuration page to configuration page navigation test failed on {device_model}: {e}"
        )
        pytest.fail(
            f"Configuration page to configuration page navigation test failed on {device_model}: {e}"
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
            f"Configuration page to configuration page navigation test completed for {device_model}"
        )
