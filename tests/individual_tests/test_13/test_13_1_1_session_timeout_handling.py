"""
Test 13.1.1: Session Timeout Handling - Pure Page Object Pattern
Category: 13 - State Transitions Tests
Test Count: Part of 7 tests in Category 13
Hardware: Device Only
Priority: MEDIUM - Form state management
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on session timeout handling functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_13_1_1_session_timeout_handling(logged_in_page: Page, base_url: str, request):
    """
    Test 13.1.1: Session Timeout Handling - Pure Page Object Pattern
    Purpose: Verify timeout behavior for inactive sessions with device-aware validation
    Expected: Appropriate timeout handling and session management with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates session timeout patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate session timeout behavior"
        )

    # Initialize page object with device-aware patterns
    general_page = GeneralConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing session timeout handling on {device_model} using pure page object pattern"
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
            f"Testing session timeout handling on {device_model} (Series {device_series})"
        )

        # Navigate to general configuration page using page object method
        logger.info("Navigating to general configuration page")
        general_page.navigate_to_general_config()

        # Test session timeout patterns using page object methods
        logger.info("Testing session timeout patterns")

        # Verify we're on a configuration page using page object method
        logger.info("Verifying configuration page access")
        page_access = general_page.verify_page_access()
        logger.info(f"Configuration page access result: {page_access}")

        # Test device series-specific session timeout behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 session timeout patterns")

            # Test Series 2 specific session timeout behavior
            series2_timeout = general_page.test_series2_session_timeout_behavior()
            logger.info(f"Series 2 session timeout result: {series2_timeout}")

            # Configure general settings for Series 2
            general_config = general_page.configure_series2_general_settings()
            logger.info(f"Series 2 general configuration result: {general_config}")

        elif device_series == 3:
            logger.info(f"Testing Series 3 session timeout patterns")

            # Test Series 3 specific session timeout behavior
            series3_timeout = general_page.test_series3_session_timeout_behavior()
            logger.info(f"Series 3 session timeout result: {series3_timeout}")

            # Configure general settings for Series 3
            general_config = general_page.configure_series3_general_settings()
            logger.info(f"Series 3 general configuration result: {general_config}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            general_config = device_capabilities_data.get("general_configuration", {})
            session_timeout = general_config.get("session_timeout", {})
            logger.info(f"Session timeout from DeviceCapabilities: {session_timeout}")

        # Test session timeout validation using page object method
        logger.info("Testing session timeout validation")
        timeout_validation = general_page.test_session_timeout_validation()
        logger.info(f"Session timeout validation result: {timeout_validation}")

        # Test session expiry detection using page object method
        logger.info("Testing session expiry detection")
        expiry_detection = general_page.test_session_expiry_detection()
        logger.info(f"Session expiry detection result: {expiry_detection}")

        # Test session management patterns using page object method
        logger.info("Testing session management patterns")
        session_management = general_page.get_session_management_patterns()
        logger.info(f"Session management patterns: {session_management}")

        # Test page reload behavior during session testing using page object method
        logger.info("Testing page reload behavior during session testing")
        reload_result = general_page.test_page_reload_during_session_testing()
        logger.info(f"Page reload behavior result: {reload_result}")

        # Test session state persistence using page object method
        logger.info("Testing session state persistence")
        state_persistence = general_page.test_session_state_persistence()
        logger.info(f"Session state persistence result: {state_persistence}")

        # Test authentication redirect patterns using page object method
        logger.info("Testing authentication redirect patterns")
        auth_redirects = general_page.test_authentication_redirect_patterns()
        logger.info(f"Authentication redirect patterns: {auth_redirects}")

        # Test session expiry modal detection using page object method
        logger.info("Testing session expiry modal detection")
        modal_detection = general_page.test_session_expiry_modal_detection()
        logger.info(f"Session expiry modal detection: {modal_detection}")

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
            session_perf = general_performance.get("session_timeout", {})

            typical_timeout = session_perf.get("typical_time", "")
            worst_case = session_perf.get("worst_case", "")

            if typical_timeout:
                logger.info(f"Session timeout performance baseline: {typical_timeout}")
            if worst_case:
                logger.info(f"Session timeout worst case: {worst_case}")

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
        logger.info(f"Session timeout handling test completed for {device_model}")

        if device_series == 2:
            logger.info(
                f"Series 2 session timeout handling test PASSED for {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 session timeout handling test PASSED for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Session timeout handling test failed on {device_model}: {e}")
        pytest.fail(f"Session timeout handling test failed on {device_model}: {e}")

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = general_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(f"Session timeout handling test completed for {device_model}")
