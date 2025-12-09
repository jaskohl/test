"""
Test 15.1.1: Detect Device Series from Page Title - Pure Page Object Pattern
Category: 15 - Device Capability Detection Tests
Test Count: 1 of 15 in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Both Series 2 and 3
IMPROVED: Pure page object architecture with device-aware capability validation
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.dashboard_page import DashboardPage


def test_15_1_1_detect_device_series_from_title(unlocked_config_page: Page, request):
    """
    Test 15.1.1: Detect Device Series from Page Title (Pure Page Object Pattern)
    Purpose: Determine device series from page title using pure page object architecture
    Expected: Title indicates correct series that matches device database
    Series: Both - validates detection accuracy
    IMPROVED: Pure page object pattern with device-aware capability validation
    """
    # Get device model for database cross-validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot cross-validate series detection"
        )

    logger = logging.getLogger(__name__)

    try:
        # Initialize dashboard page object for title detection
        dashboard_page = DashboardPage(unlocked_config_page, device_model)

        logger.info(f"{device_model}: Starting device series detection test")

        # Get expected series from device database using page object encapsulation
        expected_series = dashboard_page.get_expected_device_series()
        if expected_series == 0:
            pytest.fail(
                f"Unknown device model {device_model} - not in DeviceCapabilities database"
            )

        logger.info(f"{device_model}: Expected series from database: {expected_series}")

        # Extract series from page title using page object method
        page_title = dashboard_page.get_page_title()

        logger.info(f"{device_model}: Page title: {page_title}")

        # Validate title contains expected Kronos branding using page object validation
        dashboard_page.validate_kronos_branding_in_title()

        # Extract detected series from title using page object method
        detected_series = dashboard_page.extract_device_series_from_title()

        logger.info(f"{device_model}: Detected series from title: {detected_series}")
        logger.info(f"{device_model}: Expected series from database: {expected_series}")

        # CRITICAL VALIDATION: Title detection should match database
        assert (
            detected_series == expected_series
        ), f"Series detection mismatch - title shows Series {detected_series}, but device database shows Series {expected_series} for {device_model}"

        # Log successful validation using page object methods
        if detected_series == 2:
            logger.info(
                f"Series detection VALIDATED: Kronos Series 2 detected and confirmed for {device_model}"
            )
            print(f"DETECTED & VALIDATED: Kronos Series 2 ({device_model})")
        else:
            logger.info(
                f"Series detection VALIDATED: Kronos Series 3 detected and confirmed for {device_model}"
            )
            print(f"DETECTED & VALIDATED: Kronos Series 3 ({device_model})")

        # Additional device information validation using page object methods
        device_info = dashboard_page.get_comprehensive_device_info()
        logger.info(f"{device_model}: Device information: {device_info}")

        # Validate device info contains expected fields using page object validation
        dashboard_page.validate_device_info_structure(device_info)
        dashboard_page.validate_device_info_series_match(device_info, expected_series)

        # Test capability detection implications using page object methods
        capabilities = dashboard_page.get_device_capabilities()
        logger.info(f"{device_model}: Device capabilities: {capabilities}")

        # Series-specific validation using page object methods
        if expected_series == 2:
            # Series 2 validation
            dashboard_page.validate_series2_capabilities(capabilities)

            network_interfaces = dashboard_page.get_network_interfaces()
            dashboard_page.validate_series2_network_interfaces(network_interfaces)

            logger.info(
                f"{device_model}: Series 2 capabilities validated: No PTP, 1 interface (eth0)"
            )

        elif expected_series == 3:
            # Series 3 validation
            dashboard_page.validate_series3_capabilities(capabilities)

            network_interfaces = dashboard_page.get_network_interfaces()
            ptp_interfaces = dashboard_page.get_ptp_interfaces()

            dashboard_page.validate_series3_network_interfaces(network_interfaces)
            dashboard_page.validate_series3_ptp_interfaces(ptp_interfaces)

            logger.info(
                f"{device_model}: Series 3 capabilities validated: PTP supported, {len(network_interfaces)} interfaces, {len(ptp_interfaces)} PTP interfaces"
            )

        # Cross-validation test using page object method
        dashboard_page.test_series_detection_cross_validation()

        # Final validation using page object capability detection
        detected_capabilities = dashboard_page.detect_device_capabilities_from_ui()
        logger.info(
            f"{device_model}: UI-detected capabilities: {detected_capabilities}"
        )

        # Validate UI detection matches database capabilities
        dashboard_page.validate_ui_detection_matches_database(
            detected_capabilities, capabilities
        )

        logger.info(f"{device_model}: Series detection test completed successfully")

    except Exception as e:
        logger.error(f"{device_model}: Series detection test encountered error - {e}")
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"Series detection test failed for {device_model}: {e}")
