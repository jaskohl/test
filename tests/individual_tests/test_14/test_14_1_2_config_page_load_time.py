"""
Test 14.1.2: Configuration Page Load Time - Pure Page Object Pattern
Category: 14 - Performance Tests
Test Count: Part of 6 tests in Category 14
Hardware: Device Only
Priority: LOW - Performance validation
Series: Both Series 2 and 3
TRANSFORMED: Pure page object integration
Based on configuration page load time functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_14_1_2_config_page_load_time(logged_in_page: Page, base_url: str, request):
    """
    Test 14.1.2: Configuration Page Load Time - Pure Page Object Pattern
    Purpose: Verify configuration pages load within acceptable performance thresholds with device-aware validation
    Expected: Load time within device-specific performance expectations with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates configuration page performance patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model detection failed - cannot validate config page performance"
        )

    # Initialize page object with device-aware patterns
    config_page = GeneralConfigPage(logged_in_page, device_model)

    logger.info(
        f"Testing configuration page load time on {device_model} using pure page object pattern"
    )

    # Get device series and timeout multiplier for device-aware handling
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Calculate device-aware performance thresholds
    # Configuration pages typically take longer due to more complex UI
    if device_series == 2:
        base_threshold = 11.0  # Series 2 config page baseline
    else:  # Series 3
        base_threshold = 11.0  # Series 3 config page baseline

    max_time = base_threshold * timeout_multiplier

    logger.info(f"Device Series: {device_series}")
    logger.info(f"Timeout Multiplier: {timeout_multiplier}")
    logger.info(f"Performance Threshold: {max_time:.2f}s")

    try:
        # Navigate to dashboard page first using page object method
        logger.info("Navigating to dashboard page")
        logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")

        # Wait for page load with device-aware timeout
        config_page.wait_for_page_load()

        # Navigate to configuration page using page object method with timing measurement
        logger.info("Measuring configuration page load time using page object method")

        start_time = time.time()
        config_page.navigate_to_page()
        load_time = time.time() - start_time

        logger.info(f"Configuration page load time: {load_time:.2f}s")

        # Validate performance against device-specific thresholds
        assert (
            load_time < max_time
        ), f"Configuration page took {load_time:.2f}s (Device: {device_model}, Threshold: {max_time:.2f}s)"

        logger.info(
            f"Configuration page performance validation PASSED for {device_model}"
        )

        # Test device series-specific configuration page performance behavior
        if device_series == 2:
            logger.info(f"Testing Series 2 configuration page performance patterns")

            # Test Series 2 specific configuration page performance
            series2_performance = config_page.test_series2_config_page_performance()
            logger.info(
                f"Series 2 configuration page performance result: {series2_performance}"
            )

            # Validate Series 2 specific performance expectations
            series2_validation = config_page.validate_series2_performance_expectations()
            logger.info(f"Series 2 performance validation result: {series2_validation}")

        elif device_series == 3:
            logger.info(f"Testing Series 3 configuration page performance patterns")

            # Test Series 3 specific configuration page performance
            series3_performance = config_page.test_series3_config_page_performance()
            logger.info(
                f"Series 3 configuration page performance result: {series3_performance}"
            )

            # Validate Series 3 specific performance expectations
            series3_validation = config_page.validate_series3_performance_expectations()
            logger.info(f"Series 3 performance validation result: {series3_validation}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            performance_config = device_capabilities_data.get(
                "performance_expectations", {}
            )
            config_performance = performance_config.get("config_page_performance", {})
            logger.info(
                f"Config page performance from DeviceCapabilities: {config_performance}"
            )

        # Test page load performance validation using page object method
        logger.info("Testing page load performance validation")
        performance_validation = config_page.test_page_load_performance_validation(
            load_time
        )
        logger.info(
            f"Page load performance validation result: {performance_validation}"
        )

        # Test configuration page readiness using page object method
        logger.info("Testing configuration page readiness")
        page_readiness = config_page.test_configuration_page_readiness()
        logger.info(f"Configuration page readiness result: {page_readiness}")

        # Test performance baseline compliance using page object method
        logger.info("Testing performance baseline compliance")
        baseline_compliance = config_page.test_performance_baseline_compliance(max_time)
        logger.info(f"Performance baseline compliance result: {baseline_compliance}")

        # Test configuration form loading performance using page object method
        logger.info("Testing configuration form loading performance")
        form_loading_performance = (
            config_page.test_configuration_form_loading_performance()
        )
        logger.info(
            f"Configuration form loading performance result: {form_loading_performance}"
        )

        # Test configuration element visibility performance using page object method
        logger.info("Testing configuration element visibility performance")
        element_performance = (
            config_page.test_configuration_element_visibility_performance()
        )
        logger.info(
            f"Configuration element visibility performance result: {element_performance}"
        )

        # Test configuration page refresh performance using page object method
        logger.info("Testing configuration page refresh performance")
        refresh_performance = config_page.test_configuration_page_refresh_performance()
        logger.info(
            f"Configuration page refresh performance result: {refresh_performance}"
        )

        # Test multiple configuration page load performance using page object method
        logger.info("Testing multiple configuration page load performance")
        multiple_load_performance = (
            config_page.test_multiple_config_page_load_performance()
        )
        logger.info(
            f"Multiple configuration page load performance result: {multiple_load_performance}"
        )

        # Test different configuration pages performance using page object method
        logger.info("Testing different configuration pages performance")
        different_pages_performance = (
            config_page.test_different_configuration_pages_performance()
        )
        logger.info(
            f"Different configuration pages performance result: {different_pages_performance}"
        )

        # Performance benchmarking using page object methods
        logger.info("Performing performance benchmarking")

        # Benchmark configuration page navigation multiple times
        load_times = []
        for i in range(3):
            start_time = time.time()
            config_page.reload_page()
            load_time = time.time() - start_time
            load_times.append(load_time)
            logger.info(f"Configuration page reload {i+1} time: {load_time:.2f}s")

        # Calculate average load time
        avg_load_time = sum(load_times) / len(load_times)
        logger.info(f"Average configuration page load time: {avg_load_time:.2f}s")

        # Validate average performance
        assert (
            avg_load_time < max_time
        ), f"Average configuration page load time {avg_load_time:.2f}s exceeds threshold {max_time:.2f}s"

        # Test page data retrieval using page object method
        page_data = config_page.get_page_data()
        logger.info(
            f"Configuration page data retrieved: {list(page_data.keys()) if page_data else 'None'}"
        )

        # Test configuration capabilities validation using page object method
        config_capabilities = config_page.detect_configuration_capabilities()
        logger.info(f"Configuration capabilities detected: {config_capabilities}")

        # Test error message validation using page object method
        logger.info("Testing error message validation")
        error_messages = config_page.get_error_messages()

        if error_messages:
            logger.info(f"Error messages found: {error_messages}")
        else:
            logger.info(f"No specific error messages detected")

        # Final validation
        logger.info(f"Configuration page load time test completed for {device_model}")

        if device_series == 2:
            logger.info(
                f"Series 2 configuration page load time test PASSED for {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 configuration page load time test PASSED for {device_model}"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Configuration page load time test failed on {device_model}: {e}")
        pytest.fail(f"Configuration page load time test failed on {device_model}: {e}")

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = config_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(f"Configuration page load time test completed for {device_model}")
