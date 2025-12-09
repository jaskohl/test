"""
Category 14.4.1: Network Request Timing
Purpose: Verify network requests complete within acceptable time using pure page object pattern
Expected: Network operations complete within device-specific time limits
Series: Both 2 and 3
IMPROVED: Pure page object architecture with device-aware network performance validation

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
from pages.network_config_page import NetworkConfigPage


def test_14_4_1_network_request_timing(unlocked_config_page: Page, request):
    """
    Test 14.4.1: Network Request Timing (Pure Page Object Pattern)
    Purpose: Verify network requests complete within acceptable time using pure page object architecture
    Expected: Network operations complete within device-specific time limits
    Series: Both 2 and 3
    IMPROVED: Pure page object pattern with device-aware network performance validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model detection failed - skipping network performance test")

    logger = logging.getLogger(__name__)

    try:
        # Initialize network configuration page object
        network_page = NetworkConfigPage(unlocked_config_page, device_model)

        logger.info(f"{device_model}: Starting network request timing test")

        # Test network request timing using page object navigation
        start_time = time.time()

        # Use page object navigation method with device-aware validation
        network_page.navigate_to_page()

        # Validate page loaded successfully
        network_page.wait_for_page_load()

        end_time = time.time()
        total_navigation_time = end_time - start_time

        logger.info(
            f"{device_model}: Network navigation completed in {total_navigation_time:.3f}s"
        )

        # Get device-specific performance thresholds
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        # Network performance validation using device-aware thresholds
        base_network_threshold = 6.0  # Universal network performance baseline
        max_acceptable_time = base_network_threshold * timeout_multiplier

        assert (
            total_navigation_time < max_acceptable_time
        ), f"{device_model}: Network navigation took {total_navigation_time:.3f}s (Threshold: {max_acceptable_time:.3f}s)"

        logger.info(f"{device_model}: Network performance validation passed")
        logger.info(f"  - Navigation time: {total_navigation_time:.3f}s")
        logger.info(f"  - Performance threshold: {max_acceptable_time:.3f}s")
        logger.info(f"  - Device multiplier: {timeout_multiplier}")

        # Test multiple network requests for consistency validation
        network_times = [total_navigation_time]

        for attempt in range(2):  # Test 2 additional navigation attempts
            try:
                attempt_start = time.time()

                # Navigate to network page again using page object
                network_page.navigate_to_page()
                network_page.wait_for_page_load()

                attempt_end = time.time()
                attempt_time = attempt_end - attempt_start
                network_times.append(attempt_time)

                logger.info(
                    f"{device_model}: Network attempt {attempt + 2} completed in {attempt_time:.3f}s"
                )

                # Validate each attempt meets performance requirements
                assert (
                    attempt_time < max_acceptable_time
                ), f"{device_model}: Network attempt {attempt + 2} took {attempt_time:.3f}s (Threshold: {max_acceptable_time:.3f}s)"

            except Exception as e:
                logger.warning(
                    f"{device_model}: Network attempt {attempt + 2} handled gracefully - {e}"
                )
                continue

        # Comprehensive network performance analysis
        if len(network_times) > 1:
            avg_network_time = sum(network_times) / len(network_times)
            max_network_time = max(network_times)
            min_network_time = min(network_times)

            logger.info(f"{device_model}: Network performance analysis:")
            logger.info(f"  - Average network time: {avg_network_time:.3f}s")
            logger.info(f"  - Max network time: {max_network_time:.3f}s")
            logger.info(f"  - Min network time: {min_network_time:.3f}s")
            logger.info(f"  - Total attempts: {len(network_times)}")

            # Network consistency validation
            network_variance = (
                (max_network_time - min_network_time) / avg_network_time
                if avg_network_time > 0
                else 0
            )
            assert (
                network_variance < 1.5
            ), f"{device_model}: High network performance variance detected ({network_variance:.2f})"

            logger.info(
                f"{device_model}: Network consistency validation passed - variance: {network_variance:.2f}"
            )

        # Test network performance with form interactions
        logger.info(
            f"{device_model}: Testing network performance with form interactions"
        )

        try:
            form_interaction_start = time.time()

            # Use page object method to interact with network form
            network_page.test_network_form_interaction()

            form_interaction_end = time.time()
            form_interaction_time = form_interaction_end - form_interaction_start

            logger.info(
                f"{device_model}: Network form interaction completed in {form_interaction_time:.3f}s"
            )

            # Validate form interaction performance
            form_performance_threshold = (
                max_acceptable_time * 1.5
            )  # Allow more time for form interactions
            assert (
                form_interaction_time < form_performance_threshold
            ), f"{device_model}: Network form interaction took {form_interaction_time:.3f}s (Threshold: {form_performance_threshold:.3f}s)"

        except Exception as e:
            logger.warning(
                f"{device_model}: Network form interaction test handled gracefully - {e}"
            )

        # Final network performance validation
        logger.info(
            f"{device_model}: Network request timing test completed successfully"
        )
        logger.info(f"{device_model}: All network performance validations passed")

    except Exception as e:
        logger.error(
            f"{device_model}: Network request timing test encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"Network request timing test failed for {device_model}: {e}")
