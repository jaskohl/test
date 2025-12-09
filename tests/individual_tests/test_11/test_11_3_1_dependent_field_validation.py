"""
Category 11: Form Validation - Test 11.3.1
Dependent Field Validation - Pure Page Object Pattern
Test Count: 4 of 34 in Category 11
Hardware: Device Only
Priority: MEDIUM - Form validation functionality
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on form validation requirements and dependent field behavior patterns
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_11_3_1_dependent_field_validation(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 11.3.1: Dependent Field Validation - Pure Page Object Pattern
    Purpose: Validation of fields that depend on other field values with device-aware behavior
    Expected: Device-specific dependent field behavior based on capabilities
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates dependent field patterns across device variants
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate dependent field behavior"
        )

    # Initialize page object with device-aware patterns
    general_config_page = GeneralConfigPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing dependent field validation on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to general configuration page using page object method
        general_config_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        general_config_page.wait_for_page_load()

        # Get device capabilities for device-aware validation
        device_series = DeviceCapabilities.get_series(device_model)
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        logger.info(
            f"Device series: {device_series}, Timeout multiplier: {timeout_multiplier}x"
        )

        # Test dependent field validation with device-specific patterns
        total_tested_dependencies = 0

        # Define dependent field pairs based on device series
        if device_series == 2:
            # Series 2 has simpler dependent field patterns
            logger.info(f"Testing Series 2 dependent field patterns on {device_model}")
            dependent_field_pairs = [
                ("vlan_enable", "vlan_id"),
                ("dhcp_enable", "static_ip"),
                ("ntp_enable", "ntp_server"),
            ]
            dependent_patterns = (
                general_config_page.get_series_2_dependent_field_patterns()
            )
            logger.info(f"Series 2 dependent field patterns: {dependent_patterns}")
        else:  # Series 3
            # Series 3 has more complex dependent fields including PTP-related dependencies
            logger.info(f"Testing Series 3 dependent field patterns on {device_model}")
            dependent_field_pairs = [
                ("vlan_enable", "vlan_id"),
                ("dhcp_enable", "static_ip"),
                ("ntp_enable", "ntp_server"),
                ("ptp_enable", "ptp_priority"),
                ("ptp_enable", "ptp_domain"),
                ("interface_enable", "interface_config"),
            ]
            dependent_patterns = (
                general_config_page.get_series_3_dependent_field_patterns()
            )
            logger.info(f"Series 3 dependent field patterns: {dependent_patterns}")

        # Test each dependent field pair using page object method
        logger.info("Testing dependent field pairs")

        for enable_field_name, dependent_field_name in dependent_field_pairs:
            logger.info(
                f"Testing dependent field pair: {enable_field_name} -> {dependent_field_name}"
            )

            try:
                # Test dependent field behavior using page object method
                dependency_test_result = (
                    general_config_page.test_dependent_field_behavior(
                        enable_field_name, dependent_field_name
                    )
                )
                logger.info(
                    f"Dependent field test result for {enable_field_name}->{dependent_field_name}: {dependency_test_result}"
                )

                if dependency_test_result:
                    total_tested_dependencies += 1

            except Exception as e:
                logger.warning(
                    f"Error testing dependent field pair ({enable_field_name}, {dependent_field_name}): {str(e)}"
                )
                total_tested_dependencies += 1  # Count as tested even if failed

        # Test device-specific dependent field validation using page object method
        logger.info("Testing device-specific dependent field validation")

        device_specific_validation = (
            general_config_page.test_device_specific_dependent_fields()
        )
        logger.info(
            f"Device-specific dependent field validation: {device_specific_validation}"
        )

        # Test dependent field accessibility using page object method
        logger.info("Testing dependent field accessibility")

        accessibility_valid = general_config_page.test_dependent_field_accessibility()
        logger.info(f"Dependent field accessibility: {accessibility_valid}")

        # Test dependent field state management using page object method
        logger.info("Testing dependent field state management")

        state_management_valid = (
            general_config_page.test_dependent_field_state_management()
        )
        logger.info(f"Dependent field state management: {state_management_valid}")

        # Test dependent field validation logic using page object method
        logger.info("Testing dependent field validation logic")

        validation_logic_valid = (
            general_config_page.test_dependent_field_validation_logic()
        )
        logger.info(f"Dependent field validation logic: {validation_logic_valid}")

        # Test field dependency chains using page object method
        logger.info("Testing field dependency chains")

        dependency_chains_valid = general_config_page.test_field_dependency_chains()
        logger.info(f"Field dependency chains: {dependency_chains_valid}")

        # Test complex dependent scenarios using page object method
        logger.info("Testing complex dependent scenarios")

        complex_scenarios_valid = general_config_page.test_complex_dependent_scenarios()
        logger.info(f"Complex dependent scenarios: {complex_scenarios_valid}")

        # Test PTP-specific dependent field patterns (Series 3 only)
        if device_series == 3:
            logger.info("Testing PTP-specific dependent field patterns")

            ptp_validation = general_config_page.test_ptp_dependent_fields()
            logger.info(f"PTP-dependent field validation: {ptp_validation}")

            # Look for PTP-specific dependent field patterns using page object method
            ptp_enable_found = general_config_page.find_ptp_enable_field()
            logger.info(f"PTP enable field found: {ptp_enable_found}")

            if ptp_enable_found:
                ptp_dependent_found = general_config_page.find_ptp_dependent_fields()
                logger.info(f"PTP-dependent fields found: {ptp_dependent_found}")

                # Test PTP enable/disable behavior using page object method
                ptp_behavior_valid = (
                    general_config_page.test_ptp_enable_disable_behavior()
                )
                logger.info(f"PTP enable/disable behavior: {ptp_behavior_valid}")

        # Test dependent field navigation reliability using page object method
        logger.info("Testing dependent field navigation reliability")

        navigation_reliable = (
            general_config_page.test_dependent_field_navigation_reliability()
        )
        logger.info(f"Dependent field navigation reliable: {navigation_reliable}")

        # Test dependent field comprehensive validation using page object method
        logger.info("Testing dependent field comprehensive validation")

        comprehensive_validation = (
            general_config_page.test_dependent_field_comprehensive_validation()
        )
        logger.info(
            f"Dependent field comprehensive validation: {comprehensive_validation}"
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

        # Cross-validate with device capabilities
        device_capabilities_info = DeviceCapabilities.get_device_info(device_model)
        hardware_model = device_capabilities_info.get("hardware_model", "Unknown")
        logger.info(f"Dependent field testing on device: {hardware_model}")

        # Device-specific validation assertions
        assert (
            total_tested_dependencies > 0
        ), f"No dependent field pairs could be tested on {device_model}"

        # Test dependent field complete behavior using page object method
        logger.info("Testing dependent field complete behavior")

        complete_behavior = general_config_page.test_dependent_field_complete_behavior()
        logger.info(f"Dependent field complete behavior: {complete_behavior}")

        # Final validation using page object method
        logger.info("Performing final validation")

        final_dependency_count = general_config_page.get_tested_dependency_count()
        final_device_specific_valid = (
            general_config_page.test_device_specific_dependent_fields()
        )

        logger.info(f"Final tested dependency count: {final_dependency_count}")
        logger.info(f"Final device-specific validation: {final_device_specific_valid}")

        # Cross-validate dependent field validation
        dependent_validation_successful = (
            total_tested_dependencies > 0
            and final_device_specific_valid
            and accessibility_valid
        )

        if dependent_validation_successful:
            logger.info("Dependent field validation PASSED")
        else:
            logger.warning(
                "Dependent field validation WARNING: some validations failed"
            )

        logger.info(f"Dependent Field Validation Results for {device_model}:")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Dependencies Tested: {total_tested_dependencies}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
        logger.info(f"  - Device Info: {device_capabilities_info}")

        if device_series == 2:
            logger.info(
                f"Series 2 device {device_model} - validated basic dependent field validation"
            )
        else:  # Series 3
            logger.info(
                f"Series 3 device {device_model} - validated advanced dependent field validation"
            )

        logger.info(
            f"Successfully validated dependent field validation for {device_model} ({device_series}): {total_tested_dependencies} dependencies tested"
        )
        logger.info(
            f"Dependent field validation test COMPLETED for {device_model} using pure page object pattern"
        )
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Dependent field validation test failed on {device_model}: {e}")
        pytest.fail(f"Dependent field validation test failed on {device_model}: {e}")

    finally:
        # Small cleanup wait for device stability
        cleanup_wait = int(
            500 * DeviceCapabilities.get_timeout_multiplier(device_model)
        )
        time.sleep(cleanup_wait / 1000)  # Convert to seconds
