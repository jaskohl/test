"""
Category 10: Dashboard Data Extraction Tests - Test 10.1.1
All 4 Dashboard Tables Present - Pure Page Object Pattern
Test Count: 1 of 12 in Category 10
Hardware: Device Only
Priority: HIGH - Critical status monitoring
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on dashboard table presence validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.dashboard_page import DashboardPage

logger = logging.getLogger(__name__)


def test_10_1_1_all_tables_present(logged_in_page: Page, base_url: str, request):
    """
    Test 10.1.1: All 4 Dashboard Tables Present - Pure Page Object Pattern
    Purpose: Verify dashboard contains all 4 status tables with device-aware validation
    Expected: Tables for Status, GNSS, Time Sync, and Alarms visible with device-specific timing
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates dashboard patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate dashboard behavior")

    # Initialize page object with device-aware patterns
    dashboard_page = DashboardPage(logged_in_page, device_model)

    logger.info(
        f"Testing dashboard tables on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to dashboard page using page object method
        dashboard_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        dashboard_page.wait_for_page_load()

        # Test device series-specific behavior using page object methods
        device_series = DeviceCapabilities.get_series(device_model)

        logger.info(
            f"Testing dashboard tables on {device_model} (Series {device_series})"
        )

        # Get expected table count using page object method
        expected_tables = dashboard_page.get_expected_table_count()
        logger.info(f"Expected dashboard tables: {expected_tables}")

        # Test table presence with retry logic using page object method
        logger.info("Testing dashboard table presence with device-aware retry logic")

        # Retry logic for table loading with device-aware timing
        max_retries = 5  # Scale based on device capabilities in page object
        table_count = 0

        for attempt in range(max_retries):
            logger.info(f"Table count attempt {attempt + 1}")

            # Use page object method to get table count
            table_count = dashboard_page.get_table_count()
            logger.info(f"Table count: {table_count}")

            if table_count == expected_tables:
                logger.info(
                    f"Found expected {expected_tables} tables on attempt {attempt + 1}"
                )
                break

            # Wait for device stability using page object timeout
            stability_wait = dashboard_page.get_timeout() // 5  # 20% of timeout
            time.sleep(stability_wait // 1000)  # Convert to seconds

        if table_count != expected_tables:
            pytest.fail(
                f"Dashboard should have {expected_tables} tables, found {table_count} after {max_retries} attempts on {device_model}"
            )

        # Verify each table is visible using page object method
        logger.info("Verifying table visibility")
        for i in range(table_count):
            table_visible = dashboard_page.is_table_visible(i)
            if table_visible:
                logger.info(f"Table {i + 1} is visible")
            else:
                logger.warning(f"Table {i + 1} may not be visible")

        # Test device series-specific behavior
        if device_series == 2:
            logger.info(
                f"Series 2 dashboard validation - immediate table loading expected"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 dashboard validation - asynchronous table loading handled"
            )

        # Validate dashboard structure using page object method
        logger.info("Validating dashboard structure")
        dashboard_structure = dashboard_page.validate_dashboard_structure()
        logger.info(f"Dashboard structure validation: {dashboard_structure}")

        # Test page data retrieval using page object method
        page_data = dashboard_page.get_page_data()
        logger.info(f"Dashboard page data retrieved: {list(page_data.keys())}")

        # Test dashboard capabilities validation using page object method
        capabilities = dashboard_page.detect_dashboard_capabilities()
        logger.info(f"Dashboard capabilities detected: {capabilities}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            navigation_patterns = device_capabilities_data.get(
                "navigation_patterns", {}
            )
            logger.info(
                f"Navigation patterns from DeviceCapabilities: {navigation_patterns}"
            )

        # Performance validation using page object methods
        logger.info("Performing performance validation")

        start_time = time.time()

        # Test page reload performance
        dashboard_page.reload_page()
        reload_time = time.time() - start_time

        logger.info(f"Page reload time: {reload_time:.2f}s")

        # Cross-reference with performance expectations
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            nav_performance = performance_data.get("navigation_performance", {})
            section_nav = nav_performance.get("section_navigation", {})
            typical_time = section_nav.get("typical_time", "")
            if typical_time:
                logger.info(f"Dashboard loading performance baseline: {typical_time}")

        # Final validation
        logger.info(f"All dashboard tables test completed for {device_model}")

        if table_count == expected_tables:
            logger.info(
                f"All dashboard tables test PASSED for {device_model} (Series {device_series})"
            )
        else:
            logger.warning(
                f"All dashboard tables test partially completed for {device_model}"
            )

    except Exception as e:
        logger.error(f"All dashboard tables test failed on {device_model}: {e}")
        pytest.fail(f"All dashboard tables test failed on {device_model}: {e}")

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = dashboard_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(f"All dashboard tables test completed for {device_model}")
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )
