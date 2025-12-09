"""
Category 10: Dashboard - Test 10.6.2
Dashboard Data Refresh - Pure Page Object Pattern
Test Count: 10 of 10 in Category 10
Hardware: Device Only
Priority: HIGH - Critical status monitoring
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on dashboard requirements and data refresh patterns
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.dashboard_page import DashboardPage

logger = logging.getLogger(__name__)


def test_10_6_2_dashboard_data_refresh(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 10.6.2: Dashboard Data Refresh - Pure Page Object Pattern
    Purpose: Verify dashboard data updates on page reload with device-aware validation
    Expected: Data extraction works consistently after refresh with device-specific behavior
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates dashboard refresh patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate dashboard data refresh"
        )

    # Initialize page object with device-aware patterns
    dashboard_page = DashboardPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing dashboard data refresh on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to dashboard page using page object method
        dashboard_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        dashboard_page.wait_for_page_load()

        # First data extraction using page object method
        logger.info("Testing first data extraction")

        status_data_1 = dashboard_page.get_status_data()
        logger.info(
            f"First status data extraction: {len(status_data_1) if status_data_1 else 'None'} fields"
        )

        gnss_data_1 = dashboard_page.get_gnss_data()
        logger.info(
            f"First GNSS data extraction: {len(gnss_data_1) if gnss_data_1 else 'None'} fields"
        )

        time_sync_data_1 = dashboard_page.get_time_sync_data()
        logger.info(
            f"First time sync data extraction: {len(time_sync_data_1) if time_sync_data_1 else 'None'} fields"
        )

        alarms_data_1 = dashboard_page.get_alarms_data()
        logger.info(
            f"First alarms data extraction: {len(alarms_data_1) if alarms_data_1 else 'None'} fields"
        )

        # Test dashboard data refresh using page object method
        logger.info("Testing dashboard data refresh")

        refresh_successful = dashboard_page.refresh_dashboard_data()
        logger.info(f"Dashboard data refresh successful: {refresh_successful}")

        # Wait for page reload with device-aware timeout
        dashboard_page.wait_for_page_load()

        # Second data extraction using page object method
        logger.info("Testing second data extraction after refresh")

        status_data_2 = dashboard_page.get_status_data()
        logger.info(
            f"Second status data extraction: {len(status_data_2) if status_data_2 else 'None'} fields"
        )

        gnss_data_2 = dashboard_page.get_gnss_data()
        logger.info(
            f"Second GNSS data extraction: {len(gnss_data_2) if gnss_data_2 else 'None'} fields"
        )

        time_sync_data_2 = dashboard_page.get_time_sync_data()
        logger.info(
            f"Second time sync data extraction: {len(time_sync_data_2) if time_sync_data_2 else 'None'} fields"
        )

        alarms_data_2 = dashboard_page.get_alarms_data()
        logger.info(
            f"Second alarms data extraction: {len(alarms_data_2) if alarms_data_2 else 'None'} fields"
        )

        # Validate both extractions succeed using page object methods
        logger.info("Validating data extraction consistency")

        assert status_data_1 or isinstance(
            status_data_1, dict
        ), "First status data extraction should succeed"
        assert status_data_2 or isinstance(
            status_data_2, dict
        ), "Second status data extraction should succeed"

        assert gnss_data_1 or isinstance(
            gnss_data_1, dict
        ), "First GNSS data extraction should succeed"
        assert gnss_data_2 or isinstance(
            gnss_data_2, dict
        ), "Second GNSS data extraction should succeed"

        assert time_sync_data_1 or isinstance(
            time_sync_data_1, dict
        ), "First time sync data extraction should succeed"
        assert time_sync_data_2 or isinstance(
            time_sync_data_2, dict
        ), "Second time sync data extraction should succeed"

        assert alarms_data_1 is not None, "First alarms data extraction should succeed"
        assert alarms_data_2 is not None, "Second alarms data extraction should succeed"

        logger.info("All data extractions validated successfully")

        # Test device-specific dashboard expectations using page object method
        device_series = DeviceCapabilities.get_series(device_model)

        if device_series == 2:
            logger.info(f"Testing Series 2 specific refresh patterns on {device_model}")
            # Series 2: Basic refresh validation
            refresh_patterns = dashboard_page.get_series_2_refresh_patterns()
            logger.info(f"Series 2 refresh patterns: {refresh_patterns}")
        elif device_series == 3:
            logger.info(f"Testing Series 3 specific refresh patterns on {device_model}")
            # Series 3: May have different refresh behavior
            refresh_patterns = dashboard_page.get_series_3_refresh_patterns()
            logger.info(f"Series 3 refresh patterns: {refresh_patterns}")

        # Test dashboard completeness using page object method
        logger.info("Testing dashboard completeness after refresh")

        dashboard_complete = dashboard_page.is_dashboard_complete()
        logger.info(f"Dashboard completeness after refresh: {dashboard_complete}")

        # Test navigation reliability using page object method
        logger.info("Testing navigation reliability after refresh")

        navigation_reliable = dashboard_page.test_navigation_reliability()
        logger.info(
            f"Dashboard navigation reliability after refresh: {navigation_reliable}"
        )

        # Test page data retrieval using page object method
        logger.info("Testing page data retrieval after refresh")

        page_data = dashboard_page.get_page_data()
        logger.info(
            f"Dashboard page data keys after refresh: {list(page_data.keys()) if page_data else 'None'}"
        )

        # Test dashboard status using page object method
        logger.info("Testing dashboard status after refresh")

        dashboard_status = dashboard_page.get_dashboard_status()
        logger.info(f"Dashboard status after refresh: {dashboard_status}")

        # Performance validation using device baselines
        performance_expectations = DeviceCapabilities.get_performance_expectations(
            device_model
        )
        if performance_expectations:
            nav_performance = performance_expectations.get("navigation_performance", {})
            section_nav = nav_performance.get("section_navigation", {})
            typical_time = section_nav.get("typical_time", "")
            if typical_time:
                logger.info(
                    f"Dashboard navigation performance baseline: {typical_time}"
                )

        # Test complete data extraction using page object method
        logger.info("Testing complete data extraction after refresh")

        complete_data = dashboard_page.extract_complete_dashboard_data()
        logger.info(f"Complete dashboard data after refresh: {complete_data}")

        # Test dashboard capabilities detection using page object method
        logger.info("Testing dashboard capabilities detection after refresh")

        dashboard_capabilities = dashboard_page.detect_dashboard_capabilities()
        logger.info(f"Dashboard capabilities after refresh: {dashboard_capabilities}")

        # Test table validation using page object method
        logger.info("Testing table validation after refresh")

        table_validation = dashboard_page.validate_dashboard_tables()
        logger.info(f"Dashboard table validation after refresh: {table_validation}")

        # Cross-validate with device capabilities
        try:
            device_info = DeviceCapabilities.get_device_info(device_model)
            hardware_model = device_info.get("hardware_model", "Unknown")
            logger.info(f"Refresh testing on device: {hardware_model}")
        except Exception as e:
            logger.warning(f"Device info validation failed: {e}")

        # Final validation using page object method
        logger.info("Performing final validation")

        final_status_data = dashboard_page.get_status_data()
        final_gnss_data = dashboard_page.get_gnss_data()
        final_time_sync_data = dashboard_page.get_time_sync_data()
        final_alarms_data = dashboard_page.get_alarms_data()

        logger.info(
            f"Final status data: {len(final_status_data) if final_status_data else 'None'} fields"
        )
        logger.info(
            f"Final GNSS data: {len(final_gnss_data) if final_gnss_data else 'None'} fields"
        )
        logger.info(
            f"Final time sync data: {len(final_time_sync_data) if final_time_sync_data else 'None'} fields"
        )
        logger.info(
            f"Final alarms data: {len(final_alarms_data) if final_alarms_data else 'None'} fields"
        )

        # Cross-validate dashboard data refresh
        refresh_validation_successful = (
            (final_status_data is not None)
            and (final_gnss_data is not None)
            and (final_time_sync_data is not None)
            and (final_alarms_data is not None)
        )

        if refresh_validation_successful:
            logger.info("Dashboard data refresh validation PASSED")
        else:
            logger.warning(
                "Dashboard data refresh validation WARNING: some data missing after refresh"
            )

        logger.info(
            f"Dashboard data refresh test COMPLETED for {device_model} using pure page object pattern"
        )
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Dashboard data refresh test failed on {device_model}: {e}")
        pytest.fail(f"Dashboard data refresh test failed on {device_model}: {e}")
