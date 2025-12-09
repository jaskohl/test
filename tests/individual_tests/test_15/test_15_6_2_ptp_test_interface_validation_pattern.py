"""
Test 15.6.2: PTP Tests Use Static Interface Validation Pattern - Pure Page Object Pattern
Category: 15 - Device Capability Detection Tests
Test Count: Part of 12 tests in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Both Series 2 and 3
IMPROVED: Pure page object architecture with device-aware interface validation pattern
"""

import pytest
import logging
import re
from playwright.sync_api import Page
from pages.device_capabilities import DeviceCapabilities
from pages.ptp_config_page import PtpConfigPage
from pages.network_config_page import NetworkConfigPage
from pages.dashboard_page import DashboardPage


def test_15_6_2_ptp_test_interface_validation_pattern(
    unlocked_config_page: Page, request
):
    """
    Test 15.6.2: PTP Tests Use Static Interface Validation Pattern (Pure Page Object Pattern)
    Purpose: Validate PTP tests check static interface definitions correctly using pure page object architecture
    Expected: Interface validation uses page objects with device-aware validation
    Series: Both - validates interface enumeration correctness with pure page object optimization
    IMPROVED: Pure page object pattern with comprehensive device-aware interface validation
    """
    logger = logging.getLogger(__name__)

    try:
        # Use DeviceCapabilities for comprehensive device detection
        device_model = request.session.device_hardware_model
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.skip("Device model not detected for interface validation")

        logger.info(
            f"{device_model}: Starting PTP interface validation with pure page object architecture"
        )

        # Initialize page objects for comprehensive interface validation pattern testing
        dashboard_page = DashboardPage(unlocked_config_page, device_model)
        network_page = NetworkConfigPage(unlocked_config_page, device_model)
        ptp_page = PtpConfigPage(unlocked_config_page, device_model)

        # Get comprehensive device information using page object encapsulation
        device_series_num = dashboard_page.get_expected_device_series()
        timeout_multiplier = dashboard_page.get_timeout_multiplier()

        logger.info(f"{device_model}: PTP interface validation")
        logger.info(f"{device_model}: - Series: {device_series_num}")
        logger.info(f"{device_model}: - Timeout multiplier: {timeout_multiplier}x")

        # Apply device-aware timeout using page object method
        base_timeout = 3000
        device_timeout = ptp_page.calculate_timeout(base_timeout)

        # CORRECT: Use page object method for interface enumeration
        ptp_interfaces = ptp_page.get_ptp_interfaces_from_database()

        logger.info(f"{device_model}: Page object PTP interfaces: {ptp_interfaces}")

        # Validate that page object provides consistent interface enumeration using page object validation
        ptp_page.validate_ptp_interfaces_list_format(ptp_interfaces)

        # Comprehensive validation for each interface in the list using page object validation
        ptp_page.validate_individual_ptp_interface_format(ptp_interfaces)
        ptp_page.validate_ptp_interface_naming_convention(ptp_interfaces)
        ptp_page.validate_ptp_interface_pattern_format(ptp_interfaces)

        # Validate consistent interface enumeration across multiple calls using page object method
        ptp_interfaces_second_call = ptp_page.get_ptp_interfaces_from_database()
        ptp_page.validate_interface_enumeration_consistency(
            ptp_interfaces, ptp_interfaces_second_call
        )

        logger.info(f"{device_model}: Interface consistency validation passed")

        # Test device-specific expectations based on page object database using page object methods
        if device_model in ["KRONOS-2R-HVXX-A2F", "KRONOS-2P-HV-2"]:
            # Series 2 devices should have no PTP interfaces
            ptp_page.validate_series2_no_ptp_interfaces(ptp_interfaces)
            logger.info(
                f"{device_model}: Series 2 validation passed: No PTP interfaces as expected"
            )

        elif device_model in [
            "KRONOS-3R-HVLV-TCXO-A2F",
            "KRONOS-3R-HVXX-TCXO-44A",
            "KRONOS-3R-HVXX-TCXO-A2X",
        ]:
            # Series 3 devices should have PTP interfaces
            ptp_page.validate_series3_has_ptp_interfaces(ptp_interfaces)

            # Validate that all interfaces are valid ethernet interfaces using page object validation
            ptp_page.validate_series3_ptp_interface_format(ptp_interfaces)

            logger.info(
                f"{device_model}: Series 3 validation passed: {len(ptp_interfaces)} PTP interfaces found"
            )

        # Additional network interface cross-validation using page object methods
        network_interfaces = network_page.get_network_interfaces_from_database()

        if len(ptp_interfaces) > 0:
            # For PTP devices, validate PTP interfaces are subset of network interfaces using page object validation
            ptp_page.validate_ptp_interfaces_subset_of_network_interfaces(
                ptp_interfaces, network_interfaces
            )

            logger.info(
                f"{device_model}: PTP/Network interface validation passed: PTP interfaces are subset of network interfaces"
            )

        # Validate interface-specific characteristics using page object methods
        if device_model == "KRONOS-3R-HVLV-TCXO-A2F":  # 66.3
            expected_interfaces = ptp_page.get_expected_device_66_3_ptp_interfaces()
            ptp_page.validate_device_specific_ptp_interfaces(
                expected_interfaces, ptp_interfaces
            )
            logger.info(f"{device_model}: Device-specific validation passed")

        elif device_model == "KRONOS-3R-HVXX-TCXO-44A":  # 66.6
            expected_interfaces = ptp_page.get_expected_device_66_6_ptp_interfaces()
            ptp_page.validate_device_specific_ptp_interfaces(
                expected_interfaces, ptp_interfaces
            )
            logger.info(f"{device_model}: Device-specific validation passed")

        elif device_model == "KRONOS-3R-HVXX-TCXO-A2X":  # 190.47
            expected_interfaces = ptp_page.get_expected_device_190_47_ptp_interfaces()
            ptp_page.validate_device_specific_ptp_interfaces(
                expected_interfaces, ptp_interfaces
            )
            logger.info(f"{device_model}: Device-specific validation passed")

        # Store validation results for subsequent tests using page object method
        validation_data = {
            "device_model": device_model,
            "device_series": device_series_num,
            "ptp_interfaces": ptp_interfaces,
            "network_interfaces": network_interfaces,
            "interface_count": len(ptp_interfaces),
            "validation_timestamp": "pure_page_object_interface_pattern_validation",
        }

        dashboard_page.store_ptp_interface_validation_results_in_session(
            request, validation_data
        )

        logger.info(f"{device_model}: PTP interface validation pattern verified")
        logger.info(f"{device_model}: - Interface count: {len(ptp_interfaces)}")
        logger.info(f"{device_model}: - Interfaces: {ptp_interfaces}")
        logger.info(f"{device_model}: - Network interfaces: {network_interfaces}")
        logger.info(f"{device_model}: - Pattern validation: PASSED")

        # Cross-validation test using page object method
        ptp_page.test_ptp_interface_validation_pattern_cross_validation()

        logger.info(
            f"{device_model}: Pure page object PTP interface validation pattern completed successfully"
        )
        print(f"PTP INTERFACE VALIDATION PATTERN COMPLETED: {device_model}")

    except Exception as e:
        logger.error(
            f"{device_model}: PTP interface validation pattern encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"PTP interface validation pattern failed for {device_model}: {e}")
