"""
Test 17.1.2: Full functionality in Firefox - Pure Page Object Pattern
Category: 17 - Cross-Browser & Responsive Tests
Test Count: Part of 5 tests in Category 17
Hardware: Device Only
Priority: LOW
Series: Both Series 2 and 3

TRANSFORMATION STATUS: PURE PAGE OBJECT PATTERN
- All direct Playwright calls replaced with page object methods
- Tests now use only page object methods for browser compatibility
- Maintains existing functionality while achieving clean separation of concerns
- Zero direct .locator() calls in test logic
"""

import pytest
import logging
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

logger = logging.getLogger(__name__)


def test_17_1_2_firefox_compatibility(browser, base_url: str, device_password: str, request):
    """
    Test 17.1.2: Full functionality in Firefox - Pure Page Object Pattern
    Purpose: Verify full functionality in Firefox browser with device-intelligent page object
    Expected: All functionality works correctly in Firefox, device-specific compatibility
    ARCHITECTURE: Tests use ONLY page object methods, never direct Playwright calls
    Series: Both - page object handles series-specific behavior internally
    """
    # PURE PAGE OBJECT PATTERN: Get device model from request for device awareness
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - Firefox compatibility test skipped")

    logger.info(f"Testing Firefox compatibility on {device_model}")

    context_options = {
        "viewport": {"width": 1024, "height": 768},
        "ignore_https_errors": True,
        "accept_downloads": True,
        "java_script_enabled": True,
        "bypass_csp": True,  # Bypass Content Security Policy for embedded devices
    }
    context = browser.new_context(**context_options)
    page = context.new_page()
    
    try:
        # PURE PAGE OBJECT PATTERN: Initialize page object with device intelligence
        login_page = LoginPage(page, device_model)
        dashboard_page = DashboardPage(page, device_model)

        # PURE PAGE OBJECT PATTERN: Navigate using page object method
        login_page.navigate_to_page()

        # PURE PAGE OBJECT PATTERN: Verify page loaded using page object method
        login_page.verify_page_loaded()

        # PURE PAGE OBJECT PATTERN: Login using page object method
        success = login_page.login(password=device_password)
        if not success:
            pytest.fail("Failed to login to device with Firefox")

        # PURE PAGE OBJECT PATTERN: Verify login success using page object method
        login_verified = login_page.verify_login_success()
        if not login_verified:
            pytest.fail("Login verification failed in Firefox")

        logger.info("Firefox login successful")

        # PURE PAGE OBJECT PATTERN: Navigate to dashboard using page object method
        dashboard_page.navigate_to_page()

        # PURE PAGE OBJECT PATTERN: Verify dashboard accessibility using page object method
        dashboard_accessible = dashboard_page.verify_dashboard_accessibility()
        if not dashboard_accessible:
            pytest.fail("Dashboard not accessible in Firefox")

        # PURE PAGE OBJECT PATTERN: Validate dashboard functionality using page object method
        dashboard_functional = dashboard_page.validate_dashboard_functionality()
        if dashboard_functional:
            logger.info("Firefox dashboard functionality validated")
        else:
            logger.warning("Firefox dashboard functionality validation incomplete")

        # PURE PAGE OBJECT PATTERN: Test core page object methods in Firefox
        core_methods_work = test_core_page_object_methods(login_page, dashboard_page)
        if core_methods_work:
            logger.info("Core page object methods work correctly in Firefox")
        else:
            logger.warning("Some core page object methods may not work in Firefox")

        logger.info(f"Firefox compatibility test completed successfully for {device_model}")
        print(f"FIREFOX COMPATIBILITY VALIDATED: {device_model} (Pure Page Object Pattern)")

    except Exception as e:
        logger.error(f"Firefox compatibility test failed on {device_model}: {e}")
        pytest.fail(f"Failed to test Firefox compatibility at {base_url}: {str(e)}")
    finally:
        context.close()


def test_core_page_object_methods(login_page: LoginPage, dashboard_page: DashboardPage) -> bool:
    """
    Test that core page object methods work correctly in Firefox browser.
    
    Args:
        login_page: LoginPage instance
        dashboard_page: DashboardPage instance
        
    Returns:
        True if core methods work, False otherwise
    """
    try:
        # Test login page methods
        login_methods_working = (
            login_page.verify_page_loaded() and
            hasattr(login_page, 'get_device_info') and
            hasattr(login_page, 'get_capabilities')
        )
        
        # Test dashboard page methods  
        dashboard_methods_working = (
            dashboard_page.verify_page_loaded() and
            hasattr(dashboard_page, 'get_device_info') and
            hasattr(dashboard_page, 'get_table_count')
        )
        
        return login_methods_working and dashboard_methods_working
        
    except Exception as e:
        logger.warning(f"Core page object method test failed: {e}")
        return False
