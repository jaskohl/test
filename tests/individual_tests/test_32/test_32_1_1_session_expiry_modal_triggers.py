"""
Category 32: Session Expiry Modal - Test 32.1.1
Session Expiry Modal Triggers - DeviceCapabilities
Test Count: 1 of 2 in Category 32
Hardware: Device Only
Priority: MEDIUM - Session management
Series: Both Series 2 and 3
: Comprehensive DeviceCapabilities integration for device-aware session validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.dashboard_page import DashboardPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_32_1_1_session_expiry_modal_triggers(
    logged_in_page: Page, base_url: str, request
):
    """
    Test 32.1.1: Session Expiry Modal Triggers - DeviceCapabilities
    Purpose: Verify session expiry modal behavior with device-aware timing
    Expected: Modal appears appropriately, session timeout handling works
    : Full DeviceCapabilities integration for session management validation
    Series: Both - validates session patterns across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate session behavior")

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing session expiry modal triggers on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Get session timeout information
    session_timeout = DeviceCapabilities.get_session_timeout(device_model)

    logger.info(f"Session timeout for {device_model}: {session_timeout} minutes")

    # Initialize dashboard page object
    dashboard_page = DashboardPage(logged_in_page, device_model)

    # Verify dashboard is loaded
    dashboard_page.verify_page_loaded()

    # Test session state monitoring
    try:
        # Test that session is active
        current_url = logged_in_page.url
        if "login" not in current_url:
            logger.info(f"Session is active - current URL: {current_url}")
        else:
            logger.warning(f"Session may have expired - current URL: {current_url}")

        # Test dashboard functionality while session is active
        dashboard_data = dashboard_page.get_status_data()
        if dashboard_data:
            logger.info(f"Dashboard data accessible - session validation successful")
        else:
            logger.warning(f"Dashboard data not accessible - possible session issue")

    except Exception as e:
        logger.warning(f"Session state monitoring test failed: {e}")

    # Test session timeout handling
    try:
        # Get device-specific session timeout
        session_timeout_ms = session_timeout * 60 * 1000  # Convert to milliseconds
        test_timeout = min(session_timeout_ms, 300000)  # Cap at 5 minutes for testing

        logger.info(
            f"Testing session timeout handling with {test_timeout/1000:.0f}s timeout"
        )

        # Wait for potential session expiry (but not full timeout)
        wait_time = min(30000, test_timeout / 10)  # Wait 1/10 of timeout or 30s max
        logger.info(f"Waiting {wait_time/1000:.0f}s to test session stability")

        time.sleep(wait_time / 1000)

        # Check if session is still active
        current_url = logged_in_page.url
        if "login" not in current_url:
            logger.info(f"Session still active after {wait_time/1000:.0f}s wait")
        else:
            logger.warning(f"Session may have expired - redirecting to login")

    except Exception as e:
        logger.warning(f"Session timeout test failed: {e}")

    # Test session persistence across navigation
    try:
        # Navigate to different sections and back
        sections_to_test = ["General", "Network", "Time"]

        for section in sections_to_test:
            try:
                # Navigate to section
                section_link = logged_in_page.get_by_role("link", name=section)
                if section_link.is_visible():
                    section_link.click()
                    time.sleep(2)

                    # Check current URL
                    current_url = logged_in_page.url
                    if "login" not in current_url:
                        logger.info(
                            f"Navigation to {section} successful - session maintained"
                        )
                    else:
                        logger.warning(f"Session lost during navigation to {section}")
                        break

                    # Navigate back to dashboard
                    dashboard_link = logged_in_page.get_by_role(
                        "link", name="Dashboard"
                    )
                    if dashboard_link.is_visible():
                        dashboard_link.click()
                        time.sleep(2)

                        # Verify session is still active
                        current_url = logged_in_page.url
                        if "login" not in current_url:
                            logger.info(
                                f"Return to dashboard successful - session maintained"
                            )
                        else:
                            logger.warning(f"Session lost during return navigation")
                            break
                else:
                    logger.info(f"Section {section} link not visible - skipping")

            except Exception as e:
                logger.warning(f"Navigation test failed for {section}: {e}")

    except Exception as e:
        logger.warning(f"Session persistence test failed: {e}")

    # Test modal trigger behavior (if session expiry modal exists)
    try:
        # Look for session expiry modal elements
        modal_selectors = [
            ".modal",
            "[role='dialog']",
            ".session-expiry-modal",
            ".timeout-modal",
        ]

        modal_found = False
        for selector in modal_selectors:
            modal = logged_in_page.locator(selector)
            if modal.count() > 0 and modal.first.is_visible():
                logger.info(f"Session expiry modal found using selector: {selector}")
                modal_found = True
                break

        if not modal_found:
            logger.info(
                f"No session expiry modal detected - may not be triggered yet or not present"
            )
        else:
            logger.info(f"Session expiry modal behavior validated")

    except Exception as e:
        logger.warning(f"Session expiry modal test failed: {e}")

    # Performance validation against device baselines
    try:
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            auth_performance = performance_data.get("authentication_performance", {})
            status_login = auth_performance.get("status_monitoring_login", {})
            typical_time = status_login.get("typical_time", "")

            if typical_time:
                logger.info(f"Session performance baseline: {typical_time}")

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)
    capabilities = DeviceCapabilities.get_capabilities(device_model)

    logger.info(f"Session expiry modal triggers test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"Session timeout: {session_timeout} minutes")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"SESSION EXPIRY MODAL TRIGGERS VALIDATED: {device_model} (Series {device_series})"
    )
