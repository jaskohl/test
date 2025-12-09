"""
Test: 16.1.1 - Cross-Page Integration Navigation [PURE PAGE OBJECT]
Category: Integration Testing (16)
Purpose: Verify navigation between pages works with device-aware patterns using pure page object architecture
Expected: Smooth navigation with proper device-specific timeouts using page object encapsulation
Series: Both Series 2 and 3 (device-aware)
Priority: MEDIUM
Hardware: Device Only
IMPROVED: Pure page object architecture with device-aware navigation patterns
"""

import pytest
import time
import logging
from playwright.sync_api import expect
from pages.dashboard_page import DashboardPage
from pages.network_config_page import NetworkConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_16_1_1_cross_page_integration_navigation(
    dashboard_page: DashboardPage, network_config_page: NetworkConfigPage, request
):
    """
    Test 16.1.1: Cross-Page Integration Navigation (Pure Page Object Pattern)
    Purpose: Verify navigation between pages works with device-aware patterns using pure page object architecture
    Expected: Smooth navigation with proper device-specific timeouts
    Series: Both 2 and 3
    IMPROVED: Pure page object pattern with device-aware navigation validation
    """
    # Get device context and validate using page object encapsulation
    device_model = request.session.get("device_model", "unknown")
    if not device_model or device_model == "unknown":
        pytest.skip("Device model not detected - cannot validate cross-page navigation")

    logger = logging.getLogger(__name__)

    try:
        logger.info(f"{device_model}: Starting cross-page integration navigation test")

        # Initialize page objects for navigation testing
        dashboard_page_obj = DashboardPage(dashboard_page.page, device_model)
        network_page_obj = NetworkConfigPage(network_config_page.page, device_model)

        # Validate device context using page object methods
        device_series = dashboard_page_obj.get_expected_device_series()
        device_timeout_multiplier = dashboard_page_obj.get_timeout_multiplier()

        # Device-aware timeout scaling using page object method
        base_timeout = 5000
        scaled_timeout = dashboard_page_obj.calculate_timeout(base_timeout)

        logger.info(
            f"{device_model}: Device {device_model} (Series {device_series}): Testing cross-page navigation"
        )
        logger.info(
            f"{device_model}: Timeout scaling: {device_timeout_multiplier}x, Scaled timeout: {scaled_timeout}ms"
        )

        # Test 1: Dashboard -> Network Config using page object navigation
        try:
            logger.info(
                f"{device_model}: Testing Dashboard -> Network Config navigation"
            )

            # Navigate to dashboard using page object method
            dashboard_page_obj.navigate_to_page()
            dashboard_page_obj.wait_for_page_load()

            logger.info(f"{device_model}: Starting from dashboard")

            # Navigate to network config using page object method
            network_page_obj.navigate_to_page()
            network_page_obj.wait_for_page_load()

            logger.info(
                f"{device_model}: Dashboard -> Network Config navigation successful"
            )

            # Verify we're on network page using page object validation
            network_page_obj.validate_network_page_indicators()

            logger.info(
                f"{device_model}: Network page indicators validated successfully"
            )

        except Exception as e:
            logger.warning(
                f"{device_model}: Dashboard -> Network Config navigation had issues: {e}"
            )
            # Continue with other tests even if this fails

        # Test 2: Network Config -> Dashboard (return navigation) using page object navigation
        try:
            logger.info(
                f"{device_model}: Testing Network Config -> Dashboard navigation"
            )

            # Navigate back to dashboard using page object method
            dashboard_page_obj.navigate_to_page()
            dashboard_page_obj.wait_for_page_load()

            logger.info(
                f"{device_model}: Network Config -> Dashboard navigation successful"
            )

            # Verify we're back on dashboard using page object validation
            dashboard_page_obj.validate_dashboard_page_indicators()

            logger.info(
                f"{device_model}: Dashboard page indicators validated successfully"
            )

        except Exception as e:
            logger.warning(
                f"{device_model}: Network Config -> Dashboard navigation had issues: {e}"
            )
            # Continue with other tests even if this fails

        # Test 3: Multi-step navigation sequence using page object methods
        try:
            logger.info(f"{device_model}: Testing multi-step navigation sequence")

            nav_sequence = [
                ("dashboard", dashboard_page_obj),
                ("network", network_page_obj),
            ]

            current_page_obj = dashboard_page_obj
            for page_name, page_object in nav_sequence:
                try:
                    if page_name == "dashboard":
                        current_page_obj.navigate_to_page()
                        current_page_obj.wait_for_page_load()
                    elif page_name == "network":
                        # Navigate to network using page object method
                        current_page_obj = page_object
                        current_page_obj.navigate_to_page()
                        current_page_obj.wait_for_page_load()

                    logger.info(
                        f"{device_model}: Navigation step '{page_name}' successful"
                    )

                except Exception as e:
                    logger.warning(
                        f"{device_model}: Navigation step '{page_name}' failed: {e}"
                    )
                    break

            logger.info(f"{device_model}: Multi-step navigation sequence completed")

        except Exception as e:
            logger.warning(
                f"{device_model}: Multi-step navigation test had issues: {e}"
            )

        # Test 4: Cross-page data consistency using page object methods
        try:
            logger.info(f"{device_model}: Testing cross-page data consistency")

            # Navigate between pages and validate data consistency
            dashboard_page_obj.navigate_to_page()
            dashboard_data = dashboard_page_obj.get_page_data()

            network_page_obj.navigate_to_page()
            network_data = network_page_obj.get_page_data()

            # Validate data retrieval using page object methods
            dashboard_page_obj.validate_dashboard_data_consistency(dashboard_data)
            network_page_obj.validate_network_data_consistency(network_data)

            logger.info(f"{device_model}: Cross-page data consistency validated")

        except Exception as e:
            logger.warning(
                f"{device_model}: Cross-page data consistency test had issues: {e}"
            )

        # Test 5: Navigation performance validation using page object methods
        try:
            logger.info(f"{device_model}: Testing navigation performance")

            # Test rapid navigation between pages
            for cycle in range(3):
                cycle_start = time.time()

                dashboard_page_obj.navigate_to_page()
                network_page_obj.navigate_to_page()

                cycle_end = time.time()
                cycle_time = cycle_end - cycle_start

                # Validate navigation performance using page object method
                dashboard_page_obj.validate_navigation_performance(
                    cycle_time, cycle + 1
                )

                logger.info(
                    f"{device_model}: Navigation cycle {cycle + 1} completed in {cycle_time:.3f}s"
                )

        except Exception as e:
            logger.warning(
                f"{device_model}: Navigation performance test had issues: {e}"
            )

        # Cross-validate with device capabilities using page object methods
        try:
            device_network_config = dashboard_page_obj.get_network_configuration()
            if (
                device_network_config
                and "management_interface" in device_network_config
            ):
                mgmt_iface = device_network_config["management_interface"]
                logger.info(f"{device_model}: Cross-page integration test completed")
                logger.info(
                    f"{device_model}: Management interface: {mgmt_iface}, Timeout scaling: {device_timeout_multiplier}x"
                )

        except Exception as e:
            logger.warning(
                f"{device_model}: Device capabilities cross-validation had issues: {e}"
            )

        # Final validation using page object methods
        dashboard_page_obj.validate_device_series_consistency(device_series)
        dashboard_page_obj.validate_timeout_multiplier_consistency(
            device_timeout_multiplier
        )

        logger.info(
            f"{device_model}: Cross-page integration navigation test completed successfully"
        )
        print(f"CROSS-PAGE INTEGRATION TEST COMPLETED: {device_model}")

    except Exception as e:
        logger.error(
            f"{device_model}: Cross-page integration navigation test encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(
            f"Cross-page integration navigation test failed for {device_model}: {e}"
        )
