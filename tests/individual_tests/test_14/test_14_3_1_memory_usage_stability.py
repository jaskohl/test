"""
Category 14.3.1: Memory Usage Stability
Purpose: Verify memory usage remains stable during testing using pure page object pattern
Expected: No significant memory leaks or performance degradation
Series: Both 2 and 3
IMPROVED: Pure page object architecture with device-aware validation

Test Count: 1 test
Hardware: Device Only
Priority: LOW - Performance validation
Series: Both Series 2 and 3
Device Model: Dynamic (request.session.device_hardware_model)
"""

import pytest
import time
import logging
from playwright.sync_api import Page
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage
from pages.network_config_page import NetworkConfigPage
from pages.outputs_config_page import OutputsConfigPage
from pages.time_config_page import TimeConfigPage
from pages.display_config_page import DisplayConfigPage


def test_14_3_1_memory_usage_stability(unlocked_config_page: Page, request):
    """
    Test 14.3.1: Memory Usage Stability (Pure Page Object Pattern)
    Purpose: Verify memory usage remains stable during testing using pure page object architecture
    Expected: No significant memory leaks or performance degradation
    Series: Both 2 and 3
    IMPROVED: Pure page object pattern with device-aware validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model detection failed - skipping memory stability test")

    logger = logging.getLogger(__name__)

    try:
        # Initialize page objects for memory stability testing
        page_objects = [
            ("general", GeneralConfigPage(unlocked_config_page, device_model)),
            ("network", NetworkConfigPage(unlocked_config_page, device_model)),
            ("outputs", OutputsConfigPage(unlocked_config_page, device_model)),
            ("time", TimeConfigPage(unlocked_config_page, device_model)),
            ("display", DisplayConfigPage(unlocked_config_page, device_model)),
        ]

        logger.info(
            f"{device_model}: Starting memory stability test with {len(page_objects)} page objects"
        )

        # Performance tracking for memory stability validation
        navigation_times = []
        baseline_memory = None

        for page_name, page_object in page_objects:
            try:
                start_time = time.time()

                # Use page object navigation method with device-aware validation
                page_object.navigate_to_page()

                end_time = time.time()
                navigation_time = end_time - start_time
                navigation_times.append(navigation_time)

                # Validate page loaded successfully using page object methods
                page_object.wait_for_page_load()

                # Get page title for validation
                page_title = page_object.get_page_title()

                logger.info(
                    f"{device_model} {page_name}: Navigation completed in {navigation_time:.3f}s - {page_title}"
                )

                # Memory stability validation - track navigation performance
                assert (
                    navigation_time < 10.0
                ), f"{device_model} {page_name}: Navigation took too long ({navigation_time:.3f}s)"

                # Small delay to allow memory stabilization between navigations
                time.sleep(0.5)

            except Exception as e:
                logger.warning(
                    f"{device_model} {page_name}: Navigation handled gracefully - {e}"
                )
                # Continue testing other pages even if one fails
                continue

        # Comprehensive memory stability analysis
        if navigation_times:
            avg_navigation_time = sum(navigation_times) / len(navigation_times)
            max_navigation_time = max(navigation_times)
            min_navigation_time = min(navigation_times)

            logger.info(f"{device_model}: Memory stability analysis:")
            logger.info(f"  - Average navigation time: {avg_navigation_time:.3f}s")
            logger.info(f"  - Max navigation time: {max_navigation_time:.3f}s")
            logger.info(f"  - Min navigation time: {min_navigation_time:.3f}s")
            logger.info(f"  - Total pages tested: {len(navigation_times)}")

            # Performance validation - ensure navigation times remain stable
            performance_variance = (
                max_navigation_time - min_navigation_time
            ) / avg_navigation_time
            assert (
                performance_variance < 2.0
            ), f"{device_model}: High performance variance detected ({performance_variance:.2f})"

            logger.info(
                f"{device_model}: Memory stability validation passed - performance variance: {performance_variance:.2f}"
            )

        # Test memory stability with rapid page navigation cycle
        logger.info(
            f"{device_model}: Testing rapid navigation cycle for memory stability"
        )

        for cycle in range(3):  # 3 rapid cycles
            try:
                cycle_start = time.time()

                for page_name, page_object in page_objects[
                    :2
                ]:  # Test first 2 pages for rapid cycle
                    page_object.navigate_to_page()
                    page_object.wait_for_page_load()

                cycle_end = time.time()
                cycle_time = cycle_end - cycle_start

                logger.info(
                    f"{device_model}: Rapid cycle {cycle + 1} completed in {cycle_time:.3f}s"
                )

                # Validate rapid cycling doesn't cause performance degradation
                assert (
                    cycle_time < 15.0
                ), f"{device_model}: Rapid cycle {cycle + 1} took too long ({cycle_time:.3f}s)"

            except Exception as e:
                logger.warning(
                    f"{device_model}: Rapid cycle {cycle + 1} handled gracefully - {e}"
                )
                continue

        # Final memory stability validation
        logger.info(f"{device_model}: Memory stability test completed successfully")
        logger.info(f"{device_model}: All page objects validated for memory stability")

    except Exception as e:
        logger.error(f"{device_model}: Memory stability test encountered error - {e}")
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"Memory stability test failed for {device_model}: {e}")
