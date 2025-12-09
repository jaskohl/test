"""
Test 15.5.1: PTP Page Capability Detection - Pure Page Object Pattern
Category: 15 - Device Capability Detection Tests
Test Count: Part of 12 tests in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Both Series 2 and 3
IMPROVED: Pure page object architecture with device-aware PTP capability validation
"""

import pytest
import logging
import time
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_15_5_1_ptp_page_capability_detection(
    unlocked_config_page: Page, device_ip: str, request
):
    """
    Test 15.5.1: PTP Page Capability Detection (Pure Page Object Pattern)
    Purpose: Validate PTPConfigPage uses device-aware patterns correctly with pure page object architecture
    Expected: Page object reports capabilities matching authoritative data with device-aware validation
    Series: Both - validates page object correctness with device-aware patterns
    IMPROVED: Pure page object pattern with comprehensive device-aware PTP capability validation
    """
    # 1. Comprehensive Device Context Validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected for page capability validation")

    logger = logging.getLogger(__name__)

    try:
        # Initialize PTP configuration page object with device-aware patterns
        ptp_page = PTPConfigPage(
            unlocked_config_page, device_ip=device_ip, device_model=device_model
        )

        logger.info(f"{device_model}: Starting PTP page capability detection")
        logger.info(
            f"{device_model}: Page object created with device model: {device_model}"
        )

        # 2. Device Database Cross-Validation using page object encapsulation
        expected_series = ptp_page.get_expected_device_series()
        device_info = ptp_page.get_device_info_from_database()
        timeout_multiplier = ptp_page.get_timeout_multiplier()

        # 3. Comprehensive Capability Validation using page object methods
        expected_ptp_supported = ptp_page.is_ptp_supported_from_database()
        expected_ptp_interfaces = ptp_page.get_ptp_interfaces_from_database()
        network_interfaces = ptp_page.get_network_interfaces_from_database()
        capabilities = ptp_page.get_device_capabilities()

        logger.info(f"{device_model}: Expected series from database: {expected_series}")
        logger.info(
            f"{device_model}: PTP supported according to database: {expected_ptp_supported}"
        )
        logger.info(
            f"{device_model}: PTP interfaces from database: {expected_ptp_interfaces}"
        )
        logger.info(
            f"{device_model}: Network interfaces from database: {network_interfaces}"
        )
        logger.info(f"{device_model}: Device capabilities: {capabilities}")
        logger.info(f"{device_model}: Device info: {device_info}")
        logger.info(f"{device_model}: Timeout multiplier: {timeout_multiplier}x")

        # 4. Device-Aware Navigation using page object method
        ptp_page.navigate_to_page()

        # Validate page loaded successfully using page object method
        ptp_page.wait_for_page_load()

        logger.info(f"{device_model}: PTP page loaded successfully")

        # 5. Comprehensive Capability Validation using page object validation
        if expected_ptp_supported:
            # For PTP-supported devices, comprehensive validation
            ptp_page.validate_ptp_supported_device(
                expected_ptp_supported, expected_ptp_interfaces
            )

            logger.info(
                f"{device_model}: Series {expected_series} PTP validation - device supports PTP"
            )

            # Validate PTP-specific capabilities using page object validation
            ptp_page.validate_ptp_capabilities(capabilities)
            ptp_page.validate_minimum_ptp_interface_count(
                expected_ptp_interfaces, expected_series
            )

        else:
            # For non-PTP devices, comprehensive absence validation
            ptp_page.validate_ptp_unsupported_device(
                expected_ptp_supported, expected_ptp_interfaces
            )

            logger.info(
                f"{device_model}: Series {expected_series} PTP validation - device does not support PTP"
            )

            # Validate absence of PTP-specific capabilities using page object validation
            ptp_page.validate_no_ptp_capabilities(capabilities)

        # 6. Interface Consistency Validation using page object validation
        ptp_page.validate_ptp_network_interface_consistency(
            expected_ptp_interfaces, network_interfaces
        )

        logger.info(f"{device_model}: Interface consistency validation passed")

        # 7. Page Object Capability Reporting using page object method
        logger.info(f"{device_model}: Retrieving page object capabilities")
        actual_capabilities = ptp_page.get_device_capabilities_from_page_object()
        logger.info(
            f"{device_model}: Page object reported capabilities: {actual_capabilities}"
        )

        # 8. Comprehensive Capability Cross-Validation using page object validation
        if expected_ptp_supported:
            # For PTP-supported devices, comprehensive validation
            ptp_page.validate_ptp_support_consistency(
                actual_capabilities, expected_ptp_supported
            )

            # Validate interface reporting matches with detailed logging using page object validation
            expected_interfaces = set(expected_ptp_interfaces)
            actual_interfaces = set(actual_capabilities.get("ptp_interfaces", []))

            ptp_page.validate_ptp_interface_consistency(
                expected_interfaces, actual_interfaces
            )

            # Additional PTP-Specific Validation using page object validation
            ptp_page.validate_minimum_ptp_interface_count_from_capabilities(
                actual_capabilities, expected_series
            )

            # Validate each interface has proper configuration using page object validation
            ptp_page.validate_all_expected_ptp_interfaces_present(
                expected_ptp_interfaces, actual_interfaces
            )

            logger.info(f"{device_model}: PTP interface validation passed")

        else:
            # For non-PTP devices, comprehensive absence validation
            ptp_page.validate_no_ptp_support_in_capabilities(actual_capabilities)

            # Validate absence of PTP interfaces using page object validation
            actual_ptp_interfaces = actual_capabilities.get("ptp_interfaces", [])
            ptp_page.validate_no_ptp_interfaces_in_capabilities(actual_ptp_interfaces)

            logger.info(f"{device_model}: PTP absence validation passed")

        # 9. Device Model-Specific Validation using page object methods
        if device_model == "KRONOS-2R-HVXX-A2F":  # 66.1
            ptp_page.validate_device_66_1_characteristics(
                expected_series, expected_ptp_supported, network_interfaces
            )
            logger.info(
                f"{device_model}: Device 66.1 page validation passed - Series 2, no PTP"
            )

        elif device_model == "KRONOS-3R-HVLV-TCXO-A2F":  # 66.3
            ptp_page.validate_device_66_3_characteristics(
                expected_series, expected_ptp_supported, expected_ptp_interfaces
            )
            logger.info(
                f"{device_model}: Device 66.3 page validation passed - Series 3, PTP enabled"
            )

        elif device_model == "KRONOS-3R-HVXX-TCXO-44A":  # 66.6
            ptp_page.validate_device_66_6_characteristics(
                expected_series, expected_ptp_supported, expected_ptp_interfaces
            )
            logger.info(
                f"{device_model}: Device 66.6 page validation passed - Series 3, PTP enabled"
            )

        # 10. Performance Validation Against Baselines using page object method
        performance_data = ptp_page.get_performance_expectations()
        if performance_data:
            page_performance = performance_data.get("page_load_performance", {})
            typical_time = page_performance.get("typical_time", "")
            if typical_time:
                logger.info(
                    f"{device_model}: Page load performance baseline: {typical_time}"
                )

        # 11. Final Validation Results using page object method
        final_status = ptp_page.generate_ptp_capability_detection_results(
            device_model,
            expected_series,
            expected_ptp_supported,
            expected_ptp_interfaces,
            network_interfaces,
            timeout_multiplier,
        )

        # 12. Comprehensive Logging and Reporting
        logger.info(
            f"{device_model}: PTP page capability detection completed successfully"
        )
        logger.info(
            f"{device_model}: Database validation: PTP supported={expected_ptp_supported}, interfaces={len(expected_ptp_interfaces)}"
        )
        logger.info(
            f"{device_model}: Page object validation: Capability consistency verified"
        )
        logger.info(f"{device_model}: Cross-validation results: {final_status}")

        # 13. Success Validation using page object validation
        ptp_page.validate_device_series_range(expected_series)
        ptp_page.validate_device_info_consistency(
            device_info, device_model, expected_series
        )

        # Cross-validation test using page object method
        ptp_page.test_ptp_page_capability_cross_validation()

        logger.info(f"{device_model}: PTP page capability detection validation passed")
        print(f"PTP PAGE CAPABILITY DETECTION COMPLETED: {device_model}")
        print(f"Series: {expected_series}, PTP Support: {expected_ptp_supported}")
        print(f"Interfaces: {expected_ptp_interfaces}, Page Validation: PASSED")

    except Exception as e:
        logger.error(
            f"{device_model}: PTP page capability detection encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"PTP page capability detection failed for {device_model}: {e}")
