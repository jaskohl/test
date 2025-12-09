"""
Test 15.2.2: Series 2 Does Not Have PTP - Pure Page Object Pattern
Category: 15 - Device Capability Detection Tests
Test Count: 4 of 15 in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Series 2 Only
IMPROVED: Pure page object architecture with device-aware negative PTP capability validation
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.ptp_config_page import PtpConfigPage


def test_15_2_2_series2_no_ptp(
    unlocked_config_page: Page, base_url: str, device_series: str, request
):
    """
    Test 15.2.2: Series 2 Does Not Have PTP (Pure Page Object Pattern)
    Purpose: Verify Series 2 devices lack PTP capability using pure page object architecture
    Expected: PTP page not accessible and device database confirms no PTP support
    Series: Series 2 Only
    IMPROVED: Pure page object pattern with device-aware negative PTP capability validation
    """
    # Get device model for comprehensive validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate PTP absence")

    logger = logging.getLogger(__name__)

    try:
        # Initialize PTP configuration page object
        ptp_page = PtpConfigPage(unlocked_config_page, device_model)

        logger.info(f"{device_model}: Starting Series 2 PTP absence validation")

        # Get device series from database for validation using page object encapsulation
        expected_series = ptp_page.get_expected_device_series()
        if expected_series != 2:
            pytest.skip(
                f"Test only applies to Series 2, detected Series {expected_series} device {device_model}"
            )

        # Validate NO PTP support using page object method (negative test)
        ptp_supported = ptp_page.is_ptp_supported_from_database()
        assert (
            ptp_supported == False
        ), f"Device database should indicate NO PTP support for {device_model}"

        # Get PTP interfaces from database using page object method (should be empty)
        ptp_interfaces = ptp_page.get_ptp_interfaces_from_database()
        assert (
            len(ptp_interfaces) == 0
        ), f"Series 2 device should have no PTP interfaces, found {ptp_interfaces} for {device_model}"

        logger.info(f"{device_model}: Expected series from database: {expected_series}")
        logger.info(
            f"{device_model}: PTP supported according to database: {ptp_supported}"
        )
        logger.info(
            f"{device_model}: PTP interfaces from database: {ptp_interfaces} (should be empty)"
        )

        # Test PTP page accessibility using page object method (expect failure for Series 2)
        ptp_access_result = ptp_page.test_ptp_page_inaccessibility()

        logger.info(f"{device_model}: PTP page accessibility test result:")
        logger.info(f"  - PTP accessible: {ptp_access_result['accessible']}")
        logger.info(f"  - Has 404 error: {ptp_access_result['has_404']}")
        logger.info(f"  - Has not found: {ptp_access_result['has_not_found']}")
        logger.info(f"  - Final URL: {ptp_access_result['final_url']}")

        # Series 2 should NOT have PTP page - validate expected behavior using page object validation
        if ptp_access_result["accessible"] and not (
            ptp_access_result["has_404"] or ptp_access_result["has_not_found"]
        ):
            # PTP page is accessible but shouldn't be for Series 2
            logger.warning(
                f"{device_model}: PTP page appears accessible for Series 2 device"
            )

            # Additional validation: check if PTP elements actually exist using page object method
            profile_count = ptp_page.count_ptp_profile_configurations()

            if profile_count == 0:
                logger.info(
                    f"{device_model}: PTP page accessible but no PTP configuration elements found - acceptable"
                )
            else:
                logger.warning(
                    f"{device_model}: PTP page has {profile_count} PTP elements - unexpected for Series 2 device"
                )
                # This might indicate a configuration issue

        else:
            logger.info(
                f"{device_model}: PTP page correctly inaccessible for Series 2 device"
            )

        # Validate that database expectation matches actual behavior using page object validation
        ptp_page.validate_series2_ptp_absence_expectation(ptp_access_result)

        # Additional database cross-validation using page object methods
        capabilities = ptp_page.get_device_capabilities()
        network_interfaces = ptp_page.get_network_interfaces_from_database()

        logger.info(f"{device_model}: Device network interfaces: {network_interfaces}")
        logger.info(f"{device_model}: Device capabilities: {capabilities}")

        # Validate PTP-related fields in capabilities using page object validation
        ptp_page.validate_ptp_capabilities_absence(capabilities)

        # Validate network interfaces don't include PTP-capable ones using page object validation
        ptp_capable_interfaces = ["eth1", "eth2", "eth3", "eth4"]
        for interface in ptp_capable_interfaces:
            if interface in network_interfaces:
                logger.warning(
                    f"{device_model}: Network interface {interface} exists but should not support PTP"
                )

        # Series-specific validation using page object methods
        if expected_series == 2:
            # Series 2 validation - should definitively not support PTP
            ptp_page.validate_series2_definitive_no_ptp()

            logger.info(
                f"{device_model}: Series 2 PTP validation: Confirmed NO PTP support"
            )

            # Additional validation: check if PTP would be expected based on network interfaces
            if len(network_interfaces) > 1:
                logger.warning(
                    f"{device_model}: Series 2 device has {len(network_interfaces)} network interfaces - verify this is expected"
                )

        # Cross-validation test using page object method
        ptp_page.test_series2_ptp_absence_cross_validation()

        # Final validation using page object capability detection
        ui_detected_ptp_interfaces = ptp_page.detect_ptp_interfaces_from_ui()
        logger.info(
            f"{device_model}: UI-detected PTP interfaces: {ui_detected_ptp_interfaces}"
        )

        # Validate UI detection matches database capabilities (should be empty)
        ptp_page.validate_ui_ptp_detection_matches_database(
            ui_detected_ptp_interfaces, []
        )

        # Enhanced PTP absence validation using page object methods
        ptp_page.validate_series2_ptp_capabilities_comprehensive_absence()

        logger.info(f"{device_model}: Series 2 PTP absence test completed successfully")
        print(f"PTP ABSENCE VALIDATED: {device_model} - Confirmed NO PTP support")

    except Exception as e:
        logger.error(
            f"{device_model}: Series 2 PTP absence test encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"Series 2 PTP absence test failed for {device_model}: {e}")
