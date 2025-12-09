"""
Test 15.3.1: Detect Series 3 PTP Variant - Pure Page Object Pattern
Category: 15 - Device Capability Detection Tests
Test Count: Part of 12 tests in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Series 3 Only
IMPROVED: Pure page object architecture with device-aware PTP variant detection
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.ptp_config_page import PtpConfigPage


def test_15_3_1_detect_ptp_variant(unlocked_config_page: Page, base_url: str, request):
    """
    Test 15.3.1: Detect Series 3 PTP Variant (Pure Page Object Pattern)
    Purpose: Determine Series 3 hardware variant from PTP forms using pure page object architecture
    Expected: Variant based on form count and available ports with device-aware validation
    Series: Series 3 Only
    IMPROVED: Pure page object pattern with device-aware PTP variant detection
    """
    # 1. Comprehensive Device Context Validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot determine PTP variant")

    logger = logging.getLogger(__name__)

    try:
        # Initialize PTP configuration page object
        ptp_page = PtpConfigPage(unlocked_config_page, device_model)

        logger.info(f"{device_model}: Starting PTP variant detection")

        # 2. Device Database Cross-Validation using page object encapsulation
        expected_series = ptp_page.get_expected_device_series()
        if expected_series != 3:
            pytest.skip(
                f"Variant detection only applies to Series 3, detected Series {expected_series}"
            )

        # 3. Comprehensive Capability Validation using page object methods
        ptp_supported = ptp_page.is_ptp_supported_from_database()
        ptp_interfaces = ptp_page.get_ptp_interfaces_from_database()
        network_interfaces = ptp_page.get_network_interfaces_from_database()
        timeout_multiplier = ptp_page.get_timeout_multiplier()

        # 4. PTP Support Validation using page object validation
        assert ptp_supported == True, f"Device {device_model} should support PTP"
        assert (
            len(ptp_interfaces) > 0
        ), f"Device {device_model} should have PTP interfaces"

        logger.info(f"{device_model}: Expected series from database: {expected_series}")
        logger.info(
            f"{device_model}: PTP supported according to database: {ptp_supported}"
        )
        logger.info(f"{device_model}: PTP interfaces from database: {ptp_interfaces}")
        logger.info(
            f"{device_model}: Network interfaces from database: {network_interfaces}"
        )

        # 5. Device-Aware Navigation using page object method
        ptp_page.navigate_to_page()

        # Validate page loaded successfully using page object method
        ptp_page.wait_for_page_load()

        logger.info(f"{device_model}: PTP page loaded successfully")

        # 6. PTP Form Detection using page object method
        ptp_forms_result = ptp_page.detect_ptp_form_count()
        total_forms = ptp_forms_result["total_forms"]
        ptp_forms = ptp_forms_result["ptp_forms"]

        logger.info(f"{device_model}: Total forms found: {total_forms}")
        logger.info(f"{device_model}: PTP forms (excluding modal): {ptp_forms}")

        # 7. Comprehensive Form Count Validation using page object validation
        ptp_page.validate_ptp_form_count_range(ptp_forms)

        # 8. Interface-Form Count Cross-Validation using page object validation
        expected_ptp_forms = len(ptp_interfaces)
        ptp_page.validate_interface_form_count_consistency(
            ptp_forms, expected_ptp_forms
        )

        logger.info(
            f"{device_model}: PTP form count matches expected interface count: {expected_ptp_forms}"
        )

        # 9. Comprehensive Interface Validation using page object methods
        found_profiles = ptp_page.validate_ptp_interface_profiles(ptp_interfaces)

        assert (
            len(found_profiles) > 0
        ), f"Should find PTP profiles for available interfaces {ptp_interfaces}, found: {found_profiles}"

        # 10. Device Model-Specific Variant Validation using page object methods
        if device_model == "KRONOS-3R-HVLV-TCXO-A2F":  # 66.3
            ptp_page.validate_device_66_3_ptp_variant()
            logger.info(
                f"{device_model}: Device 66.3 PTP variant validated - 3+ interfaces expected"
            )

        elif device_model == "KRONOS-3R-HVXX-TCXO-44A":  # 66.6
            ptp_page.validate_device_66_6_ptp_variant()
            logger.info(
                f"{device_model}: Device 66.6 PTP variant validated - 4+ interfaces expected"
            )

        elif device_model == "KRONOS-3R-HVXX-TCXO-A2X":  # 190.47
            ptp_page.validate_device_190_47_ptp_variant()
            logger.info(
                f"{device_model}: Device 190.47 PTP variant validated - 3+ interfaces expected"
            )

        # 11. Interface Consistency Validation using page object validation
        ptp_page.validate_ptp_network_interface_consistency(
            ptp_interfaces, network_interfaces
        )

        logger.info(f"{device_model}: Interface consistency validation passed")

        # 12. Variant Classification using page object method
        variant_type = ptp_page.classify_ptp_variant(ptp_forms)

        # 13. Final Validation Results using page object method
        final_status = ptp_page.generate_ptp_variant_detection_results(
            device_model,
            expected_series,
            ptp_supported,
            ptp_interfaces,
            ptp_forms,
            network_interfaces,
            variant_type,
            found_profiles,
            timeout_multiplier,
        )

        # 14. Comprehensive Logging and Reporting
        logger.info(f"{device_model}: PTP variant detection completed successfully")
        logger.info(f"{device_model}: Detected variant: {variant_type}")
        logger.info(f"{device_model}: PTP forms: {ptp_forms}")
        logger.info(f"{device_model}: Available interfaces: {ptp_interfaces}")
        logger.info(f"{device_model}: Found profile selectors: {found_profiles}")
        logger.info(f"{device_model}: Variant detection results: {final_status}")

        # 15. Success Validation using page object validation
        ptp_page.validate_ptp_variant_detection_success(
            expected_series, ptp_supported, ptp_interfaces, found_profiles
        )

        # Cross-validation test using page object method
        ptp_page.test_ptp_variant_cross_validation()

        logger.info(f"{device_model}: PTP variant detection validation passed")
        print(f"PTP VARIANT DETECTION COMPLETED: {device_model} - {variant_type}")
        print(
            f"Forms: {ptp_forms}, Interfaces: {ptp_interfaces}, Profiles: {found_profiles}"
        )

    except Exception as e:
        logger.error(
            f"{device_model}: PTP variant detection test encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"PTP variant detection test failed for {device_model}: {e}")
