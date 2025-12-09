"""
Test 14.1.1: Dashboard Load Time - Pure Page Object Pattern
Category: 14 - Performance Tests
Test Count: Part of 6 tests in Category 14
Hardware: Device Only
Priority: LOW - Performance validation
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on dashboard load time functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.dashboard_page import DashboardPage

logger = logging.getLogger(__name__)


def test_14_1_1_dashboard_load_time(logged_in_page: Page, base_url: str, request):
    """
    Test 14.1.1: Dashboard Load Time - Pure Page Object Pattern
    Purpose: Verify dashboard loads within acceptable performance thresholds with device-aware validation
    Expected: Load time within device-specific performance expectations with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates dashboard performance patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model detection failed - cannot validate dashboard performance"
        )

    # Initialize page object with device-aware patterns
    dashboard_page = DashboardPage(logged_in_page, device_model)

    logger.info(
        f"Testing dashboard load time on {device_model} using pure page object pattern"
    )

    # Get device series and timeout multiplier for device-aware handling
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Calculate device-aware performance thresholds
    if device_series == 2:
        base_threshold = 20.0  # Series 2 baseline performance
    else:  # Series 3
        base_threshold = 6.0  # Series 3 baseline performance (faster devices)

    max_time = base_threshold * timeout_multiplier

    logger.info(f"Device Series: {device_series}")
    logger.info(f"Timeout Multiplier: {timeout_multiplier}")
    logger.info(f"Performance Threshold: {max_time:.2f}s")

    try:
        # Navigate to dashboard using page object method with timing measurement
        logger.info("Measuring dashboard load time using page object method")

        start_time = time.time()
        dashboard_page.navigate_to_dashboard()
        load_time = time.time() - start_time

        logger.info(f"Dashboard load time: {load_time:.2f}s")

        # Validate performance against device-specific thresholds
        assert (
            load_time < max_time
        ), f"Dashboard took {load_time:.2f}s (Device: {device_model}, Threshold: {max_time:.2f}s)"

        logger.info(f"Dashboard performance validation PASSED for {device_model}")

        # Test device series-specific dashboard performance behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 dashboard performance patterns")

            # Test Series 2 specific dashboard performance
            series2_performance = dashboard_page.test_series2_dashboard_performance()
            logger.info(f"Series 2 dashboard performance result: {series2_performance}")

            # Validate Series 2 specific performance expectations
            series2_validation = (
                dashboard_page.validate_series2_performance_expectations()
            )
            logger.info(f"Series 2 performance validation result: {series2_validation}")

        elif device_series == 3:
            logger.info(f"Testing Series 3 dashboard performance patterns")

            # Test Series 3 specific dashboard performance
            series3_performance = dashboard_page.test_series3_dashboard_performance()
            logger.info(f"Series 3 dashboard performance result: {series3_performance}")

            # Validate Series 3 specific performance expectations
            series3_validation = (
                dashboard_page.validate_series3_performance_expectations()
            )
            logger.info(f"Series 3 performance validation result: {series3_validation}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            performance_config = device_capabilities_data.get(
                "performance_expectations", {}
            )
            dashboard_performance = performance_config.get("dashboard_performance", {})
            logger.info(
                f"Dashboard performance from DeviceCapabilities: {dashboard_performance}"
            )

        # Test page load performance validation using page object method
        logger.info("Testing page load performance validation")
        performance_validation = dashboard_page.test_page_load_performance_validation(
            load_time
        )
        logger.info(
            f"Page load performance validation result: {performance_validation}"
        )

        # Test dashboard page readiness using page object method
        logger.info("Testing dashboard page readiness")
        page_readiness = dashboard_page.test_dashboard_page_readiness()
        logger.info(f"Dashboard page readiness result: {page_readiness}")

        # Test performance baseline compliance using page object method
        logger.info("Testing performance baseline compliance")
        baseline_compliance = dashboard_page.test_performance_baseline_compliance(
            max_time
        )
        logger.info(f"Performance baseline compliance result: {baseline_compliance}")

        # Test dashboard data loading performance using page object method
        logger.info("Testing dashboard data loading performance")
        data_loading_performance = (
            dashboard_page.test_dashboard_data_loading_performance()
        )
        logger.info(
            f"Dashboard data loading performance result: {data_loading_performance}"
        )

        # Test dashboard element visibility performance using page object method
        logger.info("Testing dashboard element visibility performance")
        element_performance = (
            dashboard_page.test_dashboard_element_visibility_performance()
        )
        logger.info(
            f"Dashboard element visibility performance result: {element_performance}"
        )

        # Test dashboard refresh performance using page object method
        logger.info("Testing dashboard refresh performance")
        refresh_performance = dashboard_page.test_dashboard_refresh_performance()
        logger.info(f"Dashboard refresh performance result: {refresh_performance}")

        # Test multiple load performance using page object method
        logger.info("Testing multiple load performance")
        multiple_load_performance = dashboard_page.test_multiple_load_performance()
        logger.info(f"Multiple load performance result: {multiple_load_performance}")

        # Performance benchmarking using page object methods
        logger.info("Performing performance benchmarking")

        # Benchmark dashboard navigation multiple times
        load_times = []
        for i in range(3):
            start_time = time.time()
            dashboard_page.reload_page()
            load_time = time.time() - start_time
            load_times.append(load_time)
            logger.info(f"Dashboard reload {i+1} time: {load_time:.2f}s")

        # Calculate average load time
        avg_load_time = sum(load_times) / len(load_times)
        logger.info(f"Average dashboard load time: {avg_load_time:.2f}s")

        # Validate average performance
        assert (
            avg_load_time < max_time
        ), f"Average dashboard load time {avg_load_time:.2f}s exceeds threshold {max_time:.2f}s"

        # Test page data retrieval using page object method
        page_data = dashboard_page.get_page_data()
        logger.info(
            f"Dashboard page data retrieved: {list(page_data.keys()) if page_data else 'None'}"
        )

        # Test dashboard capabilities validation using page object method
        dashboard_capabilities = dashboard_page.detect_dashboard_capabilities()
        logger.info(f"Dashboard capabilities detected: {dashboard_capabilities}")

        # Test error message validation using page object method
        logger.info("Testing error message validation")
        error_messages = dashboard_page.get_error_messages()

        if error_messages:
            logger.info(f"Error messages found: {error_messages}")
        else:
            logger.info(f"No specific error messages detected")

        # Final validation
        logger.info(f"Dashboard load time test completed for {device_model}")

        if device_series == 2:
            logger.info(f"Series 2 dashboard load time test PASSED for {device_model}")
        elif device_series == 3:
            logger.info(f"Series 3 dashboard load time test PASSED for {device_model}")

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Dashboard load time test failed on {device_model}: {e}")
        pytest.fail(f"Dashboard load time test failed on {device_model}: {e}")

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = dashboard_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(f"Dashboard load time test completed for {device_model}")
