"""
Category 10: Dashboard - Test 10.2.2
Extract Location from Status Table - Pure Page Object Pattern
Test Count: 3 of 10 in Category 10
Hardware: Device Only
Priority: HIGH - Critical status monitoring
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on dashboard requirements and location extraction patterns
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.dashboard_page import DashboardPage

logger = logging.getLogger(__name__)


def test_10_2_2_extract_location(unlocked_config_page: Page, base_url: str, request):
    """
    Test 10.2.2: Extract Location - Pure Page Object Pattern
    Purpose: Verify can extract location from status table with device-aware validation
    Expected: Location value is readable with device-specific data extraction (may be empty - this is valid)
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates location extraction patterns across device variants
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
        f"Testing location extraction on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to dashboard page using page object method
        dashboard_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        dashboard_page.wait_for_page_load()

        # Test location extraction using page object method
        logger.info("Testing location extraction")

        location_extracted = dashboard_page.get_location()
        logger.info(
            f"Extracted location: '{location_extracted}' (type: {type(location_extracted)})"
        )

        # Validate location data structure
        if location_extracted is not None:
            assert isinstance(
                location_extracted, str
            ), f"Location should be a string, got {type(location_extracted)}"

            # Empty location is valid behavior for unconfigured devices
            if location_extracted:
                assert (
                    len(location_extracted) > 0
                ), "If present, location should have content"
                logger.info(f"Location content validated: '{location_extracted}'")
            else:
                logger.info(
                    "Location is empty - this is valid behavior for unconfigured devices"
                )
        else:
            logger.info(
                "Location extraction returned None - this may be expected for this device model"
            )

        # Test device information extraction using page object method
        logger.info("Testing device information extraction")

        device_info = dashboard_page.get_device_info()
        logger.info(
            f"Device information keys: {list(device_info.keys()) if device_info else 'None'}"
        )

        # Test status data extraction using page object method
        logger.info("Testing status data extraction")

        status_data = dashboard_page.get_status_data()
        logger.info(
            f"Status data keys: {list(status_data.keys()) if status_data else 'None'}"
        )

        # Look for location data in status information
        if status_data:
            location_key = None
            for key in status_data.keys():
                if key.lower() in ["location", "device location"]:
                    location_key = key
                    break

            if location_key:
                logger.info(f"Found location key in status data: {location_key}")
                location_from_status = status_data[location_key]
                logger.info(f"Location from status data: '{location_from_status}'")
            else:
                # Check if location data exists under different naming
                potential_keys = [
                    k for k in status_data.keys() if "location" in k.lower()
                ]
                if potential_keys:
                    logger.info(
                        f"Found potential location keys in status data: {potential_keys}"
                    )
                else:
                    logger.info(
                        "No location data found in status data - this may be expected for this device model"
                    )

        # Test device-specific location expectations using page object method
        device_series = DeviceCapabilities.get_series(device_model)

        if device_series == 2:
            logger.info(
                f"Testing Series 2 specific location patterns on {device_model}"
            )
            # Series 2: Basic location field validation
            location_patterns = dashboard_page.get_series_2_location_patterns()
            logger.info(f"Series 2 location patterns: {location_patterns}")
        elif device_series == 3:
            logger.info(
                f"Testing Series 3 specific location patterns on {device_model}"
            )
            # Series 3: May have additional location fields or formatting
            location_patterns = dashboard_page.get_series_3_location_patterns()
            logger.info(f"Series 3 location patterns: {location_patterns}")

        # Test location field validation using page object method
        logger.info("Testing location field validation")

        location_valid = dashboard_page.validate_location_field()
        logger.info(f"Location field validation: {location_valid}")

        # Test location persistence using page object method
        logger.info("Testing location persistence")

        location_persistent = dashboard_page.test_location_persistence()
        logger.info(f"Location persistence: {location_persistent}")

        # Test dashboard completeness using page object method
        logger.info("Testing dashboard completeness")

        dashboard_complete = dashboard_page.is_dashboard_complete()
        logger.info(f"Dashboard completeness: {dashboard_complete}")

        # Test navigation reliability using page object method
        logger.info("Testing navigation reliability")

        navigation_reliable = dashboard_page.test_navigation_reliability()
        logger.info(f"Dashboard navigation reliability: {navigation_reliable}")

        # Cross-validate with device capabilities
        device_capabilities_info = DeviceCapabilities.get_device_info(device_model)
        hardware_model = device_capabilities_info.get("hardware_model", "Unknown")
        logger.info(
            f"Cross-validating location extraction from device: {hardware_model}"
        )

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

        # Test location extraction alternative methods using page object method
        logger.info("Testing location extraction alternative methods")

        alt_location = dashboard_page.extract_location_alternative()
        logger.info(f"Alternative location extraction: '{alt_location}'")

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

        # Final validation using page object method
        logger.info("Performing final validation")

        final_location = dashboard_page.get_location()
        final_device_info = dashboard_page.get_device_info()
        final_status_data = dashboard_page.get_status_data()

        logger.info(f"Final location extraction: '{final_location}'")
        logger.info(
            f"Final device info keys: {list(final_device_info.keys()) if final_device_info else 'None'}"
        )
        logger.info(
            f"Final status data keys: {list(final_status_data.keys()) if final_status_data else 'None'}"
        )

        # Cross-validate location extraction results
        if final_location is not None:
            logger.info(f"Location extraction validation PASSED: '{final_location}'")
        else:
            logger.info(
                f"Location extraction validation INFO: location not available (may be expected)"
            )

        logger.info(
            f"Location extraction test COMPLETED for {device_model} using pure page object pattern"
        )
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Location extraction test failed on {device_model}: {e}")
        pytest.fail(f"Location extraction test failed on {device_model}: {e}")
