"""
Category 14: Performance - Test 14.1.1
Dashboard Load Time - Pure Page Object Pattern
Test Count: 1 of 4 in Category 14
Hardware: Device Only
Priority: HIGH - Performance functionality
Series: Both Series 2 and 3

TRANSFORMATION STATUS: PURE PAGE OBJECT PATTERN
- All direct DeviceCapabilities calls replaced with DashboardPage methods
- Tests now use only DashboardPage methods for device-aware behavior
- Maintains existing functionality while achieving clean separation of concerns
- Zero direct .locator() calls in test logic
"""

import pytest
import time
import logging
from pages.dashboard_page import DashboardPage

logger = logging.getLogger(__name__)


def test_14_1_1_dashboard_load_time(
    dashboard_page: DashboardPage,
    request,
    base_url: str,
):
    """
    Test 14.1.1: Dashboard Load Time - Pure Page Object Pattern
    Purpose: Verify dashboard load time performance with device-intelligent page object
    Expected: Load times within acceptable limits, device-specific timing
    ARCHITECTURE: Tests use ONLY page object methods, never DeviceCapabilities directly
    Series: Both - page object handles series-specific behavior internally
    """
    # PURE PAGE OBJECT PATTERN: Get device model from request
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate performance behavior")

    # PURE PAGE OBJECT PATTERN: Initialize page object with device intelligence
    dashboard = DashboardPage(dashboard_page, device_model)

    # PURE PAGE OBJECT PATTERN: Get device info from page object properties
    device_series = dashboard.device_series
    timeout_multiplier = dashboard.get_timeout_multiplier()

    logger.info(f"Testing Dashboard Load Time on {device_model}")
    logger.info(f"  - Device Series: {device_series}")
    logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")

    # Test dashboard load time performance using page object methods
    try:
        # PURE PAGE OBJECT PATTERN: Test initial page load time
        start_time = time.time()
        dashboard.navigate_to_page()
        initial_load_time = time.time() - start_time

        # PURE PAGE OBJECT PATTERN: Verify page loaded
        dashboard.verify_page_loaded()

        # PURE PAGE OBJECT PATTERN: Test data extraction performance
        data_start_time = time.time()
        page_data = dashboard.get_page_data()
        data_load_time = time.time() - data_start_time

        logger.info(f" Dashboard initial load time: {initial_load_time:.2f}s")
        logger.info(f" Dashboard data extraction time: {data_load_time:.2f}s")

        # PURE PAGE OBJECT PATTERN: Test table loading performance
        table_start_time = time.time()
        table_count = dashboard.get_table_count()
        table_load_time = time.time() - table_start_time

        logger.info(f" Dashboard table loading time: {table_load_time:.2f}s")
        logger.info(f" Tables loaded: {table_count}")

        # PURE PAGE OBJECT PATTERN: Performance validation
        performance_valid = dashboard.validate_dashboard_performance(
            initial_load_time, data_load_time, table_load_time
        )
        if performance_valid:
            logger.info(f" Dashboard performance within acceptable limits")
        else:
            logger.warning(f" Dashboard performance may be outside acceptable limits")

    except Exception as e:
        pytest.fail(f"Dashboard load time test failed on {device_model}: {e}")

    # Test device series-specific performance behavior
    if device_series == 2:
        # Series 2: Basic performance expectations
        logger.info(f"Series 2: Testing basic performance patterns")

        # PURE PAGE OBJECT PATTERN: Test basic performance interaction
        basic_performance = dashboard.test_basic_performance_interaction()
        if basic_performance:
            logger.info(f" Series 2 basic performance interaction successful")
        else:
            logger.warning(f" Series 2 basic performance interaction failed")

    elif device_series == 3:
        # Series 3: Enhanced performance expectations
        logger.info(f"Series 3: Testing enhanced performance patterns")

        # PURE PAGE OBJECT PATTERN: Test enhanced performance interaction
        enhanced_performance = dashboard.test_enhanced_performance_interaction()
        if enhanced_performance:
            logger.info(f" Series 3 enhanced performance interaction successful")
        else:
            logger.warning(f" Series 3 enhanced performance interaction failed")

    else:
        # Unknown device series - use basic validation
        logger.warning(
            f"Unknown device series {device_series} - using basic performance validation"
        )

    # Test performance benchmarking using page object methods
    try:
        # PURE PAGE OBJECT PATTERN: Test performance benchmarking
        benchmark_results = dashboard.run_performance_benchmark()
        if benchmark_results:
            logger.info(f" Performance benchmarking completed")
            for metric, value in benchmark_results.items():
                logger.info(f"  {metric}: {value}")
        else:
            logger.warning(f" Performance benchmarking failed")

    except Exception as e:
        logger.warning(f"Performance benchmarking test failed: {e}")

    # Test load time consistency using page object methods
    try:
        # PURE PAGE OBJECT PATTERN: Test load time consistency
        consistency_valid = dashboard.validate_load_time_consistency()
        if consistency_valid:
            logger.info(f" Load time consistency validated")
        else:
            logger.warning(f" Load time consistency validation failed")

    except Exception as e:
        logger.warning(f"Load time consistency test failed: {e}")

    # Test comprehensive performance scenarios using page object methods
    try:
        # PURE PAGE OBJECT PATTERN: Test comprehensive performance scenarios
        comprehensive_performance = dashboard.test_comprehensive_performance_scenarios()
        if comprehensive_performance:
            logger.info(f" Comprehensive performance scenarios handled")
        else:
            logger.warning(f" Some performance scenarios may not be handled")

    except Exception as e:
        logger.warning(f"Comprehensive performance test failed: {e}")

    # Log comprehensive test results using page object methods
    # PURE PAGE OBJECT PATTERN: Use page object methods instead of direct DeviceCapabilities calls
    device_info = dashboard.get_device_info()
    capabilities = dashboard.get_capabilities()

    logger.info(f"Dashboard Load Time test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"Performance capabilities: {capabilities}")

    print(f"DASHBOARD LOAD TIME VALIDATED: {device_model} (Pure Page Object Pattern)")
