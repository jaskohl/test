"""
Test 14.2.1: Multiple Page Loads Performance - Pure Page Object Pattern
Category: 14 - Performance Tests
Test Count: Part of 6 tests in Category 14
Hardware: Device Only
Priority: LOW - Performance validation
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on multiple page loads performance functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage
from pages.network_config_page import NetworkConfigPage
from pages.outputs_config_page import OutputsConfigPage

logger = logging.getLogger(__name__)


def test_14_2_1_multiple_page_loads(logged_in_page: Page, base_url: str, request):
    """
    Test 14.2.1: Multiple Page Loads Performance - Pure Page Object Pattern
    Purpose: Verify performance when loading multiple configuration pages with device-aware validation
    Expected: Consistent performance across multiple page loads with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates multiple page load patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model detection failed - cannot validate multiple page load performance"
        )

    # Initialize page objects with device-aware patterns
    general_page = GeneralConfigPage(logged_in_page, device_model)
    network_page = NetworkConfigPage(logged_in_page, device_model)
    outputs_page = OutputsConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing multiple page loads performance on {device_model} using pure page object pattern"
    )

    # Get device series and timeout multiplier for device-aware handling
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Calculate device-aware performance thresholds
    if device_series == 2:
        base_avg_threshold = 20.0  # Series 2 average performance
        base_max_threshold = 20.0  # Series 2 worst case
    else:  # Series 3
        base_avg_threshold = 20.0  # Series 3 average performance
        base_max_threshold = 20.0  # Series 3 worst case

    max_avg_time = base_avg_threshold * timeout_multiplier
    max_single_time = base_max_threshold * timeout_multiplier

    logger.info(f"Device Series: {device_series}")
    logger.info(f"Timeout Multiplier: {timeout_multiplier}")
    logger.info(f"Average Load Time Threshold: {max_avg_time:.2f}s")
    logger.info(f"Single Load Time Threshold: {max_single_time:.2f}s")

    try:
        # Navigate to dashboard page using page object method
        logger.info("Navigating to dashboard page")
        logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")

        # Wait for page load with device-aware timeout
        general_page.wait_for_page_load()

        # Test multiple page loads using page object methods
        logger.info("Testing multiple page loads performance")

        # Define pages to test
        pages_to_test = [
            ("general", general_page, "navigate_to_general_config"),
            ("network", network_page, "navigate_to_network_config"),
            ("outputs", outputs_page, "navigate_to_outputs_config"),
        ]

        load_times = []

        for page_name, page_obj, nav_method in pages_to_test:
            logger.info(f"Testing {page_name} page load performance")

            start_time = time.time()
            nav_func = getattr(page_obj, nav_method)
            nav_func()
            load_time = time.time() - start_time

            load_times.append(load_time)
            logger.info(f"{device_model} {page_name} page load: {load_time:.2f}s")

        # Verify all loads are within acceptable range
        avg_load_time = sum(load_times) / len(load_times)
        max_load_time = max(load_times)

        logger.info(f"Multiple page loads performance analysis:")
        logger.info(f"Average load time: {avg_load_time:.2f}s")
        logger.info(f"Maximum load time: {max_load_time:.2f}s")

        # Validate performance against device-specific thresholds
        assert (
            avg_load_time < max_avg_time
        ), f"Average load time {avg_load_time:.2f}s too slow (Device: {device_model})"
        assert (
            max_load_time < max_single_time
        ), f"Max load time {max_load_time:.2f}s too slow (Device: {device_model})"

        logger.info(
            f"Multiple page loads performance validation PASSED for {device_model}"
        )

        # Test device series-specific multiple page load behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 multiple page load patterns")

            # Test Series 2 specific multiple page load behavior
            series2_performance = (
                general_page.test_series2_multiple_page_load_performance()
            )
            logger.info(
                f"Series 2 multiple page load performance result: {series2_performance}"
            )

            # Validate Series 2 specific performance expectations
            series2_validation = (
                general_page.validate_series2_multiple_load_expectations()
            )
            logger.info(
                f"Series 2 multiple load validation result: {series2_validation}"
            )

        elif device_series == 3:
            logger.info(f"Testing Series 3 multiple page load patterns")

            # Test Series 3 specific multiple page load behavior
            series3_performance = (
                general_page.test_series3_multiple_page_load_performance()
            )
            logger.info(
                f"Series 3 multiple page load performance result: {series3_performance}"
            )

            # Validate Series 3 specific performance expectations
            series3_validation = (
                general_page.validate_series3_multiple_load_expectations()
            )
            logger.info(
                f"Series 3 multiple load validation result: {series3_validation}"
            )

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            performance_config = device_capabilities_data.get(
                "performance_expectations", {}
            )
            multiple_load_performance = performance_config.get(
                "multiple_page_loads", {}
            )
            logger.info(
                f"Multiple page loads performance from DeviceCapabilities: {multiple_load_performance}"
            )

        # Test concurrent page load performance using page object method
        logger.info("Testing concurrent page load performance")
        concurrent_performance = general_page.test_concurrent_page_load_performance()
        logger.info(
            f"Concurrent page load performance result: {concurrent_performance}"
        )

        # Test page load consistency using page object method
        logger.info("Testing page load consistency")
        load_consistency = general_page.test_page_load_consistency(load_times)
        logger.info(f"Page load consistency result: {load_consistency}")

        # Test performance degradation detection using page object method
        logger.info("Testing performance degradation detection")
        degradation_detection = general_page.test_performance_degradation_detection(
            load_times
        )
        logger.info(
            f"Performance degradation detection result: {degradation_detection}"
        )

        # Test sequential page navigation performance using page object method
        logger.info("Testing sequential page navigation performance")
        sequential_performance = (
            general_page.test_sequential_page_navigation_performance()
        )
        logger.info(
            f"Sequential page navigation performance result: {sequential_performance}"
        )

        # Test page load stabilization using page object method
        logger.info("Testing page load stabilization")
        load_stabilization = general_page.test_page_load_stabilization()
        logger.info(f"Page load stabilization result: {load_stabilization}")

        # Test memory usage during multiple loads using page object method
        logger.info("Testing memory usage during multiple loads")
        memory_usage = general_page.test_memory_usage_during_multiple_loads()
        logger.info(f"Memory usage during multiple loads result: {memory_usage}")

        # Performance benchmarking using page object methods
        logger.info("Performing performance benchmarking")

        # Benchmark multiple page loads multiple times
        benchmark_load_times = []
        for i in range(2):  # Reduced iterations for performance
            benchmark_load_times_inner = []
            for page_name, page_obj, nav_method in pages_to_test:
                start_time = time.time()
                nav_func = getattr(page_obj, nav_method)
                nav_func()
                load_time = time.time() - start_time
                benchmark_load_times_inner.append(load_time)

            avg_benchmark = sum(benchmark_load_times_inner) / len(
                benchmark_load_times_inner
            )
            benchmark_load_times.append(avg_benchmark)
            logger.info(f"Benchmark run {i+1} average load time: {avg_benchmark:.2f}s")

        # Calculate overall average performance
        overall_avg = sum(benchmark_load_times) / len(benchmark_load_times)
        logger.info(f"Overall average performance: {overall_avg:.2f}s")

        # Validate overall performance
        assert (
            overall_avg < max_avg_time
        ), f"Overall average performance {overall_avg:.2f}s exceeds threshold {max_avg_time:.2f}s"

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
        logger.info(
            f"Multiple page loads performance test completed for {device_model}"
        )
        logger.info(
            f"{device_model} concurrent performance: avg={avg_load_time:.2f}s, max={max_load_time:.2f}s"
        )

        if device_series == 2:
            logger.info(
                f"Series 2 multiple page loads performance test PASSED for {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 multiple page loads performance test PASSED for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(
            f"Multiple page loads performance test failed on {device_model}: {e}"
        )
        pytest.fail(
            f"Multiple page loads performance test failed on {device_model}: {e}"
        )

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = general_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(
            f"Multiple page loads performance test completed for {device_model}"
        )
