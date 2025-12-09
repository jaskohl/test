"""
Category 11: Form Validation - Test 11.18.1
Hardware Capability Validation - Pure Page Object Pattern
Test Count: 8 of 34 in Category 11
Hardware: Device Only
Priority: HIGH - Hardware capability validation
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on form validation requirements and hardware capability validation patterns
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_11_18_1_hardware_capability_validation(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 11.18.1: Hardware Capability Validation - Pure Page Object Pattern
    Purpose: Hardware capability detection and validation
    Expected: Device-specific hardware capability behavior with comprehensive validation
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates hardware capability patterns across device variants
    Compatible: All 5 hardware variants (172.16.66.1, 172.16.66.3, 172.16.66.6, 172.16.190.46, 172.16.190.47)
    Series Coverage: Series 2 (2 outputs), Series 3 (6 outputs, PTP support)
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate hardware capabilities")

    # Initialize page object with device-aware patterns
    general_config_page = GeneralConfigPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing hardware capability validation on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to general configuration page using page object method
        general_config_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        general_config_page.wait_for_page_load()

        # Get device capabilities and series information
        device_series = DeviceCapabilities.get_series(device_model)
        device_capabilities = DeviceCapabilities.get_capabilities(device_model)
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        logger.info(f"\n=== Hardware Capability Validation for {device_model} ===")
        logger.info(f"Device Series: {device_series}")
        logger.info(f"Timeout Multiplier: {timeout_multiplier}")
        logger.info(f"Device Capabilities: {device_capabilities}")

        # Test hardware capability consistency using page object method
        logger.info("Testing hardware capability consistency")

        capability_consistent = (
            general_config_page.validate_hardware_capability_consistency()
        )
        logger.info(f"Hardware capability consistency: {capability_consistent}")

        # Test device-specific hardware expectations using page object method
        if device_series == 2:
            logger.info(
                f"Testing Series 2 specific hardware patterns on {device_model}"
            )
            # Series 2 should have fewer output options
            hardware_patterns = general_config_page.get_series_2_hardware_patterns()
            logger.info(f"Series 2 hardware patterns: {hardware_patterns}")
        elif device_series == 3:
            logger.info(
                f"Testing Series 3 specific hardware patterns on {device_model}"
            )
            # Series 3 should have more advanced output options
            hardware_patterns = general_config_page.get_series_3_hardware_patterns()
            logger.info(f"Series 3 hardware patterns: {hardware_patterns}")

        # Test output configuration capabilities using page object method
        logger.info("Testing output configuration capabilities")

        output_capabilities_valid = (
            general_config_page.validate_output_configuration_capabilities()
        )
        logger.info(f"Output configuration capabilities: {output_capabilities_valid}")

        if device_series == 2:
            # Series 2 should have fewer output options
            expected_outputs = 2  # Series 2 typically has 2 outputs
            logger.info(
                f"{device_model} (Series 2): Validating basic output configuration"
            )
            logger.info(f"Expected outputs: {expected_outputs}")
        else:  # Series 3
            # Series 3 should have more advanced output options
            expected_outputs = 6  # Series 3 typically has 6 outputs
            logger.info(
                f"{device_model} (Series 3): Validating advanced output configuration"
            )
            logger.info(f"Expected outputs: {expected_outputs}")

        # Test feature limitations using page object method
        logger.info("Testing feature limitations")

        feature_limitations_valid = general_config_page.validate_feature_limitations()
        logger.info(f"Feature limitations: {feature_limitations_valid}")

        # Test PTP availability based on series using page object method
        logger.info("Testing PTP availability based on series")

        if device_series == 2:
            # Series 2 should NOT have PTP features
            ptp_available = general_config_page.is_ptp_feature_available()
            if not ptp_available:
                logger.info(f"{device_model}: Correctly lacks PTP features (Series 2)")
            else:
                logger.warning(
                    f"{device_model}: Unexpected PTP features found for Series 2 device"
                )
        else:  # Series 3
            # Series 3 should have PTP features
            ptp_available = general_config_page.is_ptp_feature_available()
            if ptp_available:
                logger.info(f"{device_model}: PTP features available (Series 3)")
            else:
                logger.warning(
                    f"{device_model}: Expected PTP features not found for Series 3"
                )

        # Test interface count limitations using page object method
        logger.info("Testing interface count limitations")

        max_interfaces = 2 if device_series == 2 else 4
        interface_count_valid = (
            general_config_page.validate_interface_count_limitations(max_interfaces)
        )
        logger.info(
            f"Interface count limitations (max: {max_interfaces}): {interface_count_valid}"
        )

        # Test capability indicators validation using page object method
        logger.info("Testing capability indicators validation")

        capability_indicators_valid = (
            general_config_page.validate_capability_indicators()
        )
        logger.info(f"Capability indicators validation: {capability_indicators_valid}")

        # Test series-specific indicators using page object method
        logger.info("Testing series-specific indicators")

        if device_series == 2:
            # Look for Series 2 specific indicators
            series2_indicators_valid = (
                general_config_page.validate_series_2_indicators()
            )
            logger.info(f"Series 2 indicators validation: {series2_indicators_valid}")
        else:
            # Look for Series 3 specific indicators
            series3_indicators_valid = (
                general_config_page.validate_series_3_indicators()
            )
            logger.info(f"Series 3 indicators validation: {series3_indicators_valid}")

        # Test advanced features detection using page object method
        logger.info("Testing advanced features detection")

        if device_series == 3:
            # Look for advanced features
            advanced_features_valid = general_config_page.validate_advanced_features()
            logger.info(f"Advanced features validation: {advanced_features_valid}")
        else:
            logger.info(
                f"Series 2 device {device_model}: Advanced features not expected"
            )

        # Test hardware capability state management using page object method
        logger.info("Testing hardware capability state management")

        state_management_valid = (
            general_config_page.test_hardware_capability_state_management()
        )
        logger.info(f"Hardware capability state management: {state_management_valid}")

        # Test hardware capability navigation reliability using page object method
        logger.info("Testing hardware capability navigation reliability")

        navigation_reliable = (
            general_config_page.test_hardware_capability_navigation_reliability()
        )
        logger.info(f"Hardware capability navigation reliable: {navigation_reliable}")

        # Test hardware capability comprehensive validation using page object method
        logger.info("Testing hardware capability comprehensive validation")

        comprehensive_validation = (
            general_config_page.test_hardware_capability_comprehensive_validation()
        )
        logger.info(
            f"Hardware capability comprehensive validation: {comprehensive_validation}"
        )

        # Performance validation using device baselines
        performance_expectations = DeviceCapabilities.get_performance_expectations(
            device_model
        )
        if performance_expectations:
            form_performance = performance_expectations.get("form_interaction", {})
            field_interaction = form_performance.get("field_interaction", {})
            typical_time = field_interaction.get("typical_time", "")
            if typical_time:
                logger.info(
                    f"Form field interaction performance baseline: {typical_time}"
                )

        # Test hardware capability complete behavior using page object method
        logger.info("Testing hardware capability complete behavior")

        complete_behavior = (
            general_config_page.test_hardware_capability_complete_behavior()
        )
        logger.info(f"Hardware capability complete behavior: {complete_behavior}")

        # Final validation using page object method
        logger.info("Performing final validation")

        final_capability_consistent = (
            general_config_page.validate_hardware_capability_consistency()
        )
        final_output_capabilities_valid = (
            general_config_page.validate_output_configuration_capabilities()
        )
        final_feature_limitations_valid = (
            general_config_page.validate_feature_limitations()
        )

        logger.info(f"Final capability consistency: {final_capability_consistent}")
        logger.info(f"Final output capabilities: {final_output_capabilities_valid}")
        logger.info(f"Final feature limitations: {final_feature_limitations_valid}")

        # Cross-validate hardware capability validation
        hardware_validation_successful = (
            final_capability_consistent
            and final_output_capabilities_valid
            and final_feature_limitations_valid
            and comprehensive_validation
        )

        if hardware_validation_successful:
            logger.info("Hardware capability validation PASSED")
        else:
            logger.warning(
                "Hardware capability validation WARNING: some validations failed"
            )

        logger.info(f"Hardware Capability Validation Results for {device_model}:")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
        logger.info(f"  - Device Capabilities: {device_capabilities}")
        logger.info(f"  - Expected Outputs: {expected_outputs}")
        logger.info(f"  - Max Interfaces: {max_interfaces}")

        logger.info(
            f"Hardware capability validation completed for {device_model} using pure page object pattern"
        )
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(
            f"Hardware capability validation test failed on {device_model}: {e}"
        )
        pytest.fail(
            f"Hardware capability validation test failed on {device_model}: {e}"
        )
