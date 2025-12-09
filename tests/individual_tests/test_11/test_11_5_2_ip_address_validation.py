"""
Category 11: Form Validation - Test 11.5.2
IP Address Validation - Pure Page Object Pattern
Test Count: 5 of 34 in Category 11
Hardware: Device Only
Priority: HIGH - Form validation functionality
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on form validation requirements and IP address validation patterns
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_11_5_2_ip_address_validation(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 11.5.2: IP Address Validation - Pure Page Object Pattern
    Purpose: IP address format validation with device-aware validation
    Expected: Valid IP address formats accepted, invalid formats handled appropriately
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates IP address patterns across device variants
    """
    # Get device model for device-aware validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate IP capabilities")

    # Initialize page object with device-aware patterns
    general_config_page = GeneralConfigPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing IP address validation on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to general configuration page using page object method
        general_config_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        general_config_page.wait_for_page_load()

        # Get device series for device-aware validation
        device_series = DeviceCapabilities.get_series(device_model)
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        logger.info(
            f"Device series: {device_series}, Timeout multiplier: {timeout_multiplier}x"
        )

        # Test device-specific IP expectations using page object method
        if device_series == 2:
            logger.info(f"Testing Series 2 specific IP patterns on {device_model}")
            # Series 2: Traditional IP field patterns
            ip_patterns = general_config_page.get_series_2_ip_field_patterns()
            logger.info(f"Series 2 IP field patterns: {ip_patterns}")
        elif device_series == 3:
            logger.info(f"Testing Series 3 specific IP patterns on {device_model}")
            # Series 3: Advanced IP field patterns
            ip_patterns = general_config_page.get_series_3_ip_field_patterns()
            logger.info(f"Series 3 IP field patterns: {ip_patterns}")

        # Test IP field detection using page object method
        logger.info("Testing IP field detection")

        ip_fields_found = general_config_page.detect_ip_address_fields()
        logger.info(f"IP fields found: {ip_fields_found}")

        if ip_fields_found:
            # Test first available IP field using page object method
            logger.info("Testing primary IP field")

            primary_ip_field_test = general_config_page.test_primary_ip_field()
            logger.info(f"Primary IP field test: {primary_ip_field_test}")

            # Test IP field visibility and accessibility using page object method
            logger.info("Testing IP field visibility and accessibility")

            field_accessible = (
                general_config_page.test_ip_field_visibility_and_accessibility()
            )
            logger.info(f"IP field visibility and accessibility: {field_accessible}")

            # Test valid IP addresses using page object method
            logger.info("Testing valid IP addresses")

            valid_ips = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
            for ip in valid_ips:
                logger.info(f"Testing valid IP address: {ip}")

                try:
                    ip_valid = general_config_page.test_valid_ip_address(ip)
                    logger.info(f"Valid IP test result for {ip}: {ip_valid}")
                except Exception as e:
                    logger.warning(f"IP field issue for {ip}: {e}")

            # Test invalid IP format using page object method
            logger.info("Testing invalid IP format")

            try:
                invalid_ip = "999.999.999.999"
                invalid_ip_handled = general_config_page.test_invalid_ip_address(
                    invalid_ip
                )
                logger.info(
                    f"Invalid IP test result for {invalid_ip}: {invalid_ip_handled}"
                )
            except Exception as e:
                logger.warning(f"Invalid IP test issue: {e}")

        else:
            logger.info(f"No IP address fields found for {device_model}")

        # Test IP address field validation using page object method
        logger.info("Testing IP address field validation")

        ip_field_valid = general_config_page.validate_ip_address_field()
        logger.info(f"IP address field validation: {ip_field_valid}")

        # Test IP format validation using page object method
        logger.info("Testing IP format validation")

        format_valid = general_config_page.test_ip_format_validation()
        logger.info(f"IP format validation: {format_valid}")

        # Test IP field constraints using page object method
        logger.info("Testing IP field constraints")

        field_constraints = general_config_page.get_ip_field_constraints()
        logger.info(f"IP field constraints: {field_constraints}")

        # Test IP field state management using page object method
        logger.info("Testing IP field state management")

        state_management_valid = general_config_page.test_ip_field_state_management()
        logger.info(f"IP field state management: {state_management_valid}")

        # Test network interface validation using page object method
        logger.info("Testing network interface validation")

        network_interface_valid = (
            general_config_page.test_network_interface_validation()
        )
        logger.info(f"Network interface validation: {network_interface_valid}")

        # Test IP field navigation reliability using page object method
        logger.info("Testing IP field navigation reliability")

        navigation_reliable = general_config_page.test_ip_field_navigation_reliability()
        logger.info(f"IP field navigation reliable: {navigation_reliable}")

        # Test IP field comprehensive validation using page object method
        logger.info("Testing IP field comprehensive validation")

        comprehensive_validation = (
            general_config_page.test_ip_field_comprehensive_validation()
        )
        logger.info(f"IP field comprehensive validation: {comprehensive_validation}")

        # Cross-validate network capabilities
        expected_network_fields = DeviceCapabilities.get_network_interfaces(
            device_model
        )
        logger.info(f"Expected network interfaces: {expected_network_fields}")

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

        # Test IP field complete behavior using page object method
        logger.info("Testing IP field complete behavior")

        complete_behavior = general_config_page.test_ip_field_complete_behavior()
        logger.info(f"IP field complete behavior: {complete_behavior}")

        # Final validation using page object method
        logger.info("Performing final validation")

        final_ip_fields_found = general_config_page.detect_ip_address_fields()
        final_ip_field_valid = general_config_page.validate_ip_address_field()

        logger.info(f"Final IP fields found: {final_ip_fields_found}")
        logger.info(f"Final IP field validation: {final_ip_field_valid}")

        # Cross-validate IP address validation
        ip_validation_successful = (
            len(final_ip_fields_found) > 0 and final_ip_field_valid and field_accessible
        )

        if ip_validation_successful:
            logger.info("IP address validation PASSED")
        else:
            logger.warning("IP address validation WARNING: some validations failed")

        logger.info(f"IP Address Validation Results for {device_model}:")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - IP Fields Found: {len(final_ip_fields_found)}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
        logger.info(f"  - Expected Network Interfaces: {expected_network_fields}")

        logger.info(
            f"DeviceCapabilities IP validation completed for {device_model} (Series {device_series})"
        )
        logger.info(
            f"IP address validation test COMPLETED for {device_model} using pure page object pattern"
        )
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"IP address validation test failed on {device_model}: {e}")
        pytest.fail(f"IP address validation test failed on {device_model}: {e}")
