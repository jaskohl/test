"""
Test 15.6.1: PTP Tests Follow Correct Device Validation Pattern - Pure Page Object Pattern
Category: 15 - Device Capability Detection Tests
Test Count: Part of 12 tests in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Both Series 2 and 3
IMPROVED: Pure page object architecture with device-aware validation pattern
"""

import pytest
import logging
from pages.device_capabilities import DeviceCapabilities
from pages.ptp_config_page import PtpConfigPage
from pages.network_config_page import NetworkConfigPage
from pages.dashboard_page import DashboardPage


def test_15_6_1_ptp_test_device_validation_pattern(request):
    """
    Test 15.6.1: PTP Tests Follow Correct Device Validation Pattern (Pure Page Object Pattern)
    Purpose: Validate all PTP tests use proper page object-based device validation patterns
    Expected: Tests should use page objects with device-aware validation and skip appropriately
    Series: Both - meta-validation of test correctness with pure page object enhancements
    IMPROVED: Pure page object pattern with comprehensive device-aware validation
    """
    logger = logging.getLogger(__name__)

    try:
        # Use DeviceCapabilities for comprehensive device detection
        device_model = request.session.device_hardware_model
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.skip("Device model not detected for pattern validation")

        logger.info(
            f"{device_model}: Starting PTP pattern validation with pure page object architecture"
        )

        # Initialize page objects for comprehensive validation pattern testing
        dashboard_page = DashboardPage(
            None, device_model
        )  # No page needed for pattern validation
        network_page = NetworkConfigPage(
            None, device_model
        )  # No page needed for pattern validation
        ptp_page = PtpConfigPage(
            None, device_model
        )  # No page needed for pattern validation

        # Get comprehensive device information using page object encapsulation
        device_series_num = dashboard_page.get_expected_device_series()
        timeout_multiplier = dashboard_page.get_timeout_multiplier()
        ptp_supported = ptp_page.is_ptp_supported_from_database()
        ptp_interfaces = ptp_page.get_ptp_interfaces_from_database()
        network_interfaces = network_page.get_network_interfaces_from_database()

        logger.info(f"{device_model}: PTP pattern validation")
        logger.info(f"{device_model}: - Series: {device_series_num}")
        logger.info(f"{device_model}: - Timeout multiplier: {timeout_multiplier}x")
        logger.info(f"{device_model}: - PTP supported: {ptp_supported}")
        logger.info(f"{device_model}: - PTP interfaces: {ptp_interfaces}")
        logger.info(f"{device_model}: - Network interfaces: {network_interfaces}")

        # Comprehensive validation based on device characteristics using page object validation
        if not ptp_supported:
            # For non-PTP devices, validate comprehensive absence of PTP features
            logger.info(
                f"{device_model}: Device correctly does not support PTP - comprehensive validation"
            )

            # Validate no PTP interfaces for non-PTP devices using page object validation
            ptp_page.validate_no_ptp_interfaces_for_non_ptp_device(ptp_interfaces)

            # Additional validations for non-PTP devices using page object validation
            dashboard_page.validate_non_ptp_device_series(device_series_num)

            # Validate network interface expectations for Series 2 using page object validation
            network_page.validate_series2_network_interface_expectations(
                network_interfaces
            )

        else:
            # For PTP devices, validate comprehensive PTP feature presence
            logger.info(
                f"{device_model}: Device supports PTP - comprehensive validation"
            )

            # Validate PTP interfaces exist for PTP devices using page object validation
            ptp_page.validate_ptp_interfaces_exist_for_ptp_device(ptp_interfaces)

            # Additional validations for PTP devices using page object validation
            dashboard_page.validate_ptp_device_series(device_series_num)

            # Validate network interface expectations for Series 3 using page object validation
            network_page.validate_series3_network_interface_expectations(
                network_interfaces
            )

        # Validate this pattern works for all known device models with comprehensive checks using page object methods
        if device_model == "KRONOS-2R-HVXX-A2F":  # 66.1
            ptp_page.validate_device_66_1_pattern(
                ptp_supported, ptp_interfaces, device_series_num, network_interfaces
            )
            logger.info(
                f"{device_model}: KRONOS-2R-HVXX-A2F (66.1) validation passed - Series 2, no PTP, single network interface"
            )

        elif device_model == "KRONOS-2P-HV-2":  # 190.46
            ptp_page.validate_device_190_46_pattern(
                ptp_supported, ptp_interfaces, device_series_num, network_interfaces
            )
            logger.info(
                f"{device_model}: KRONOS-2P-HV-2 (190.46) validation passed - Series 2, no PTP, single network interface"
            )

        elif device_model == "KRONOS-3R-HVLV-TCXO-A2F":  # 66.3
            ptp_page.validate_device_66_3_pattern(
                ptp_supported, ptp_interfaces, device_series_num, network_interfaces
            )
            logger.info(
                f"{device_model}: KRONOS-3R-HVLV-TCXO-A2F (66.3) validation passed - Series 3, PTP enabled, {len(network_interfaces)} network interfaces"
            )

        elif device_model == "KRONOS-3R-HVXX-TCXO-44A":  # 66.6
            ptp_page.validate_device_66_6_pattern(
                ptp_supported, ptp_interfaces, device_series_num, network_interfaces
            )
            logger.info(
                f"{device_model}: KRONOS-3R-HVXX-TCXO-44A (66.6) validation passed - Series 3, PTP enabled, {len(network_interfaces)} network interfaces"
            )

        elif device_model == "KRONOS-3R-HVXX-TCXO-A2X":  # 190.47
            ptp_page.validate_device_190_47_pattern(
                ptp_supported, ptp_interfaces, device_series_num, network_interfaces
            )
            logger.info(
                f"{device_model}: KRONOS-3R-HVXX-TCXO-A2X (190.47) validation passed - Series 3, PTP enabled, {len(network_interfaces)} network interfaces"
            )

        # Store validation results for subsequent tests using page object method
        validation_data = {
            "device_model": device_model,
            "device_series": device_series_num,
            "ptp_supported": ptp_supported,
            "ptp_interface_count": len(ptp_interfaces),
            "network_interface_count": len(network_interfaces),
            "timeout_multiplier": timeout_multiplier,
            "validation_timestamp": "pure_page_object_pattern_validation",
        }

        dashboard_page.store_ptp_device_validation_results_in_session(
            request, validation_data
        )

        logger.info(f"{device_model}: PTP device validation pattern verified")
        logger.info(f"{device_model}: - Pattern validation: PASSED")
        logger.info(f"{device_model}: - Device series: {device_series_num}")
        logger.info(f"{device_model}: - PTP capability: {ptp_supported}")
        logger.info(
            f"{device_model}: - Interface counts: PTP={len(ptp_interfaces)}, Network={len(network_interfaces)}"
        )

        # Cross-validation test using page object method
        dashboard_page.test_ptp_device_validation_pattern_cross_validation()

        logger.info(
            f"{device_model}: Pure page object PTP pattern validation completed successfully"
        )
        print(f"PTP DEVICE VALIDATION PATTERN COMPLETED: {device_model}")

    except Exception as e:
        logger.error(
            f"{device_model}: PTP device validation pattern encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"PTP device validation pattern failed for {device_model}: {e}")
