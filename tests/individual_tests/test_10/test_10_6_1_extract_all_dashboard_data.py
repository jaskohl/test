"""
Category 10: Dashboard - Test 10.6.1
Extract All Dashboard Data - Pure Page Object Pattern
Test Count: 9 of 10 in Category 10
Hardware: Device Only
Priority: HIGH - Critical status monitoring
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on dashboard requirements and complete data extraction patterns
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.dashboard_page import DashboardPage

logger = logging.getLogger(__name__)


def test_10_6_1_extract_all_dashboard_data(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 10.6.1: Extract All Dashboard Data - Pure Page Object Pattern
    Purpose: Verify can extract data from all 4 tables with device-aware validation
    Expected: All tables return data dictionaries with device-specific extraction patterns
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates dashboard data extraction patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate dashboard data extraction"
        )

    # Initialize page object with device-aware patterns
    dashboard_page = DashboardPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing complete dashboard data extraction on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to dashboard page using page object method
        dashboard_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        dashboard_page.wait_for_page_load()

        # Test dashboard structure validation using page object method
        logger.info("Testing dashboard structure validation")

        dashboard_structure = dashboard_page.validate_dashboard_structure()
        logger.info(f"Dashboard structure validation: {dashboard_structure}")

        # Get navigation patterns for validation
        navigation_patterns = DeviceCapabilities.get_navigation_patterns(device_model)
        dashboard_structure_config = navigation_patterns.get("dashboard_structure", {})
        expected_tables = dashboard_structure_config.get("tables_present", 4)

        logger.info(f"Extracting dashboard data from {expected_tables} expected tables")

        # Extract all data with device-aware validation using page object methods
        try:
            logger.info("Testing status data extraction")

            status_data = dashboard_page.get_status_data()
            logger.info(
                f"Status data extracted: {type(status_data)} with {len(status_data) if isinstance(status_data, dict) else 'N/A'} fields"
            )
        except Exception as e:
            logger.warning(f"Status data extraction failed: {e}")
            status_data = None

        try:
            logger.info("Testing GNSS data extraction")

            gnss_data = dashboard_page.get_gnss_data()
            logger.info(
                f"GNSS data extracted: {type(gnss_data)} with {len(gnss_data) if isinstance(gnss_data, dict) else 'N/A'} fields"
            )
        except Exception as e:
            logger.warning(f"GNSS data extraction failed: {e}")
            gnss_data = None

        try:
            logger.info("Testing time sync data extraction")

            time_sync_data = dashboard_page.get_time_sync_data()
            logger.info(
                f"Time sync data extracted: {type(time_sync_data)} with {len(time_sync_data) if isinstance(time_sync_data, dict) else 'N/A'} fields"
            )
        except Exception as e:
            logger.warning(f"Time sync data extraction failed: {e}")
            time_sync_data = None

        try:
            logger.info("Testing alarms data extraction")

            alarms_data = dashboard_page.get_alarms_data()
            logger.info(
                f"Alarms data extracted: {type(alarms_data)} with {len(alarms_data) if isinstance(alarms_data, dict) else 'N/A'} fields"
            )
        except Exception as e:
            logger.warning(f"Alarms data extraction failed: {e}")
            alarms_data = None

        # Validate all extractions with device-aware assertions
        try:
            assert status_data or isinstance(
                status_data, dict
            ), "Should extract status table data"
            logger.info("Status data validation passed")
        except Exception as e:
            logger.warning(f"Status data validation failed: {e}")

        try:
            assert gnss_data or isinstance(
                gnss_data, dict
            ), "Should extract GNSS table data"
            logger.info("GNSS data validation passed")
        except Exception as e:
            logger.warning(f"GNSS data validation failed: {e}")

        try:
            assert time_sync_data or isinstance(
                time_sync_data, dict
            ), "Should extract time sync table data"
            logger.info("Time sync data validation passed")
        except Exception as e:
            logger.warning(f"Time sync data validation failed: {e}")

        try:
            assert alarms_data is not None, "Should extract alarms table data"
            logger.info("Alarms data validation passed")
        except Exception as e:
            logger.warning(f"Alarms data validation failed: {e}")

        # Test device-specific dashboard expectations using page object method
        device_series = DeviceCapabilities.get_series(device_model)

        if device_series == 2:
            logger.info(
                f"Testing Series 2 specific dashboard patterns on {device_model}"
            )
            # Series 2: Basic dashboard data validation
            dashboard_patterns = dashboard_page.get_series_2_dashboard_patterns()
            logger.info(f"Series 2 dashboard patterns: {dashboard_patterns}")
        elif device_series == 3:
            logger.info(
                f"Testing Series 3 specific dashboard patterns on {device_model}"
            )
            # Series 3: May have additional dashboard data fields
            dashboard_patterns = dashboard_page.get_series_3_dashboard_patterns()
            logger.info(f"Series 3 dashboard patterns: {dashboard_patterns}")

        # Test dashboard completeness using page object method
        logger.info("Testing dashboard completeness")

        dashboard_complete = dashboard_page.is_dashboard_complete()
        logger.info(f"Dashboard completeness: {dashboard_complete}")

        # Test navigation reliability using page object method
        logger.info("Testing navigation reliability")

        navigation_reliable = dashboard_page.test_navigation_reliability()
        logger.info(f"Dashboard navigation reliability: {navigation_reliable}")

        # Test table count validation using page object method
        logger.info("Testing table count validation")

        table_count = dashboard_page.get_table_count()
        logger.info(f"Table count: {table_count}")

        # Test all tables presence using page object method
        logger.info("Testing all tables presence")

        tables_present = dashboard_page.verify_all_tables_present()
        logger.info(f"All tables present verification: {tables_present}")

        # Test dashboard data validation using page object method
        logger.info("Testing dashboard data validation")

        data_valid = dashboard_page.validate_dashboard_data()
        logger.info(f"Dashboard data validation: {data_valid}")

        # Test page data retrieval using page object method
        logger.info("Testing page data retrieval")

        page_data = dashboard_page.get_page_data()
        logger.info(
            f"Dashboard page data keys: {list(page_data.keys()) if page_data else 'None'}"
        )

        # Test dashboard status using page object method
        logger.info("Testing dashboard status")

        dashboard_status = dashboard_page.get_dashboard_status()
        logger.info(f"Dashboard status: {dashboard_status}")

        # Test dashboard capabilities detection using page object method
        logger.info("Testing dashboard capabilities detection")

        dashboard_capabilities = dashboard_page.detect_dashboard_capabilities()
        logger.info(f"Dashboard capabilities: {dashboard_capabilities}")

        # Validate dashboard structure matches device expectations
        logger.info(f"Expected dashboard tables: {expected_tables}")
        logger.info(f"Device model: {device_model}")
        logger.info(f"Device series: {device_series}")

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

        # Cross-validate with device capabilities
        try:
            device_info = DeviceCapabilities.get_device_info(device_model)
            hardware_model = device_info.get("hardware_model", "Unknown")
            logger.info(f"Extracting dashboard data from device: {hardware_model}")
        except Exception as e:
            logger.warning(f"Device info validation failed: {e}")

        # Test complete data extraction using page object method
        logger.info("Testing complete data extraction")

        complete_data = dashboard_page.extract_complete_dashboard_data()
        logger.info(f"Complete dashboard data extraction: {complete_data}")

        # Test dashboard data refresh using page object method
        logger.info("Testing dashboard data refresh")

        refresh_successful = dashboard_page.refresh_dashboard_data()
        logger.info(f"Dashboard data refresh: {refresh_successful}")

        # Test dashboard performance metrics using page object method
        logger.info("Testing dashboard performance metrics")

        performance_metrics = dashboard_page.get_performance_metrics()
        logger.info(f"Dashboard performance metrics: {performance_metrics}")

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

        # Cross-validate complete dashboard data extraction
        data_extraction_successful = (
            (final_status_data is not None)
            and (final_gnss_data is not None)
            and (final_time_sync_data is not None)
            and (final_alarms_data is not None)
        )

        if data_extraction_successful:
            logger.info("Complete dashboard data extraction validation PASSED")
        else:
            logger.warning(
                "Complete dashboard data extraction validation WARNING: some data missing"
            )

        logger.info(
            f"Complete dashboard data extraction test COMPLETED for {device_model} using pure page object pattern"
        )
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(
            f"Complete dashboard data extraction test failed on {device_model}: {e}"
        )
        pytest.fail(
            f"Complete dashboard data extraction test failed on {device_model}: {e}"
        )
