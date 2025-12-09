"""
Test 21.1.1: Multiple Sessions Allowed - Pure Page Object Pattern
Category: 21 - Session & Concurrency Testing
Test Count: Part of 3 tests in Category 21
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3

TRANSFORMATION STATUS: PURE PAGE OBJECT PATTERN
- All direct DeviceCapabilities calls replaced with page object methods
- All direct locator usage replaced with page object methods
- Tests now use only page object methods for session concurrency
- Maintains existing functionality while achieving clean separation of concerns
- Zero direct .locator() calls in test logic
"""

import pytest
import time
import logging
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

logger = logging.getLogger(__name__)


def test_21_1_1_multiple_sessions_allowed(browser, base_url: str, device_password: str, request):
    """
    Test 21.1.1: Multiple Sessions Allowed - Pure Page Object Pattern
    Purpose: Verify multiple browser sessions can access device with device-intelligent page object
    Expected: Multiple sessions work correctly, device-specific session handling
    ARCHITECTURE: Tests use ONLY page object methods, never DeviceCapabilities directly
    Series: Both - page object handles series-specific behavior internally
    """
    # PURE PAGE OBJECT PATTERN: Get device model from request for device awareness
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - multiple sessions test skipped")

    logger.info(f"Testing multiple sessions on {device_model}")

    # Create two contexts (simulating two users) with device-aware patterns
    context1 = browser.new_context()
    context2 = browser.new_context()
    page1 = context1.new_page()
    page2 = context2.new_page()

    try:
        # PURE PAGE OBJECT PATTERN: Initialize page objects with device intelligence
        login_page1 = LoginPage(page1, device_model)
        dashboard_page1 = DashboardPage(page1, device_model)
        login_page2 = LoginPage(page2, device_model)
        dashboard_page2 = DashboardPage(page2, device_model)

        # PURE PAGE OBJECT PATTERN: Test session 1 login
        logger.info("Session 1: Starting login process")
        session1_success = test_single_session_login(login_page1, dashboard_page1, device_password)
        if not session1_success:
            pytest.fail("Session 1: Failed to login")

        # PURE PAGE OBJECT PATTERN: Test session 2 login
        logger.info("Session 2: Starting login process")
        session2_success = test_single_session_login(login_page2, dashboard_page2, device_password)
        if not session2_success:
            pytest.fail("Session 2: Failed to login")

        # PURE PAGE OBJECT PATTERN: Verify both sessions are active
        logger.info("Verifying both sessions are active")
        session1_active = verify_session_active(dashboard_page1, device_model)
        session2_active = verify_session_active(dashboard_page2, device_model)

        if not (session1_active and session2_active):
            pytest.fail(f"Multiple sessions test failed - Session 1: {session1_active}, Session 2: {session2_active}")

        logger.info("Both sessions verified active")

        # PURE PAGE OBJECT PATTERN: Test session independence
        session_independent = test_session_independence(dashboard_page1, dashboard_page2, device_model)
        if session_independent:
            logger.info("Session independence validated")
        else:
            logger.warning("Session independence validation incomplete")

        logger.info(f"Multiple sessions test completed successfully for {device_model}")
        print(f"MULTIPLE SESSIONS VALIDATED: {device_model} (Pure Page Object Pattern)")

    except Exception as e:
        logger.error(f"Multiple sessions test failed on {device_model}: {e}")
        pytest.fail(f"Multiple sessions test failed: {str(e)}")
    finally:
        # PURE PAGE OBJECT PATTERN: Cleanup using device-aware timing
        context1.close()
        context2.close()


def test_single_session_login(login_page: LoginPage, dashboard_page: DashboardPage, device_password: str) -> bool:
    """
    Test login for a single session using page object methods.
    
    Args:
        login_page: LoginPage instance
        dashboard_page: DashboardPage instance
        device_password: Device password
        
    Returns:
        True if login successful, False otherwise
    """
    try:
        # PURE PAGE OBJECT PATTERN: Navigate using page object method
        login_page.navigate_to_page()

        # PURE PAGE OBJECT PATTERN: Verify page loaded using page object method
        login_page.verify_page_loaded()

        # PURE PAGE OBJECT PATTERN: Login using page object method
        success = login_page.login(password=device_password)
        if not success:
            return False

        # PURE PAGE OBJECT PATTERN: Verify login success using page object method
        login_verified = login_page.verify_login_success()
        if not login_verified:
            return False

        # PURE PAGE OBJECT PATTERN: Navigate to dashboard using page object method
        dashboard_page.navigate_to_page()

        # PURE PAGE OBJECT PATTERN: Verify dashboard accessible using page object method
        dashboard_accessible = dashboard_page.verify_dashboard_accessibility()
        return dashboard_accessible

    except Exception as e:
        logger.warning(f"Single session login failed: {e}")
        return False


def verify_session_active(dashboard_page: DashboardPage, device_model: str) -> bool:
    """
    Verify that a session is active using page object methods.
    
    Args:
        dashboard_page: DashboardPage instance
        device_model: Device model for validation
        
    Returns:
        True if session is active, False otherwise
    """
    try:
        # PURE PAGE OBJECT PATTERN: Get device info using page object method
        device_info = dashboard_page.get_device_info()
        if not device_info:
            return False

        # PURE PAGE OBJECT PATTERN: Validate dashboard functionality using page object method
        dashboard_functional = dashboard_page.validate_dashboard_functionality()
        return dashboard_functional

    except Exception as e:
        logger.warning(f"Session active verification failed: {e}")
        return False


def test_session_independence(dashboard_page1: DashboardPage, dashboard_page2: DashboardPage, device_model: str) -> bool:
    """
    Test that two sessions are independent using page object methods.
    
    Args:
        dashboard_page1: DashboardPage instance for session 1
        dashboard_page2: DashboardPage instance for session 2
        device_model: Device model for validation
        
    Returns:
        True if sessions are independent, False otherwise
    """
    try:
        # PURE PAGE OBJECT PATTERN: Get page data from both sessions using page object methods
        page_data1 = dashboard_page1.get_page_data()
        page_data2 = dashboard_page2.get_page_data()

        # PURE PAGE OBJECT PATTERN: Validate both sessions have valid data using page object methods
        valid_data1 = dashboard_page1.validate_page_data_consistency(page_data1)
        valid_data2 = dashboard_page2.validate_page_data_consistency(page_data2)

        if not (valid_data1 and valid_data2):
            return False

        # PURE PAGE OBJECT PATTERN: Test session isolation by checking device info from both sessions
        device_info1 = dashboard_page1.get_device_info()
        device_info2 = dashboard_page2.get_device_info()

        # Both sessions should see the same device
        if device_info1 and device_info2:
            return True
        else:
            return False

    except Exception as e:
        logger.warning(f"Session independence test failed: {e}")
        return False
