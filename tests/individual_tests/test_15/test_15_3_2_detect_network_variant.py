"""
Test 15.3.2: Detect Series 3 Network Variant - Pure Page Object Pattern
Category: 15 - Device Capability Detection Tests
Test Count: Part of 12 tests in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Series 3 Only
IMPROVED: Pure page object architecture with device-aware network variant detection
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.network_config_page import NetworkConfigPage


def test_15_3_2_detect_network_variant(
    unlocked_config_page: Page, base_url: str, device_series: str, request
):
    """
    Test 15.3.2: Detect Series 3 Network Variant (Pure Page Object Pattern)
    Purpose: Determine Series 3 network variant from network forms using pure page object architecture
    Expected: Variant detection based on network configuration with device-aware validation
    Series: Series 3 Only
    IMPROVED: Pure page object pattern with device-aware network variant detection
    """
    # 1. Comprehensive Device Context Validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot determine network variant")

    logger = logging.getLogger(__name__)

    try:
        # Initialize network configuration page object
        network_page = NetworkConfigPage(unlocked_config_page, device_model)

        logger.info(f"{device_model}: Starting network variant detection")

        # 2. Device Database Cross-Validation using page object encapsulation
        expected_series = network_page.get_expected_device_series()
        if expected_series != 3:
            pytest.skip(
                f"Variant detection only applies to Series 3, detected Series {expected_series}"
            )

        # 3. Comprehensive Capability Validation using page object methods
        network_interfaces = network_page.get_network_interfaces_from_database()
        timeout_multiplier = network_page.get_timeout_multiplier()
        capabilities = network_page.get_device_capabilities()

        logger.info(f"{device_model}: Expected series from database: {expected_series}")
        logger.info(
            f"{device_model}: Network interfaces from database: {network_interfaces}"
        )
        logger.info(f"{device_model}: Device capabilities: {capabilities}")
        logger.info(f"{device_model}: Timeout multiplier: {timeout_multiplier}x")

        # 4. Series-Specific Network Interface Validation using page object validation
        assert (
            len(network_interfaces) >= 4
        ), f"Series 3 should have 4+ network interfaces, found {len(network_interfaces)}"
        assert (
            "eth0" in network_interfaces
        ), "Series 3 should have eth0 management interface"

        # 5. Device-Aware Navigation using page object method
        network_page.navigate_to_page()

        # Validate page loaded successfully using page object method
        network_page.wait_for_page_load()

        logger.info(f"{device_model}: Network page loaded successfully")

        # 6. Network Form Detection using page object method
        network_forms_result = network_page.detect_network_form_count()
        total_forms = network_forms_result["total_forms"]
        network_forms = network_forms_result["network_forms"]

        logger.info(f"{device_model}: Total forms found: {total_forms}")
        logger.info(f"{device_model}: Network forms (excluding modal): {network_forms}")

        # 7. Comprehensive Form Count Validation using page object validation
        network_page.validate_network_form_count_positive(network_forms)

        # 8. Check for redundancy mode field (HSR/PRP support) using page object method
        has_redundancy = network_page.check_redundancy_mode_support()

        logger.info(
            f"{device_model}: Redundancy mode (HSR/PRP) support detected: {has_redundancy}"
        )

        # 9. Network Interface Validation Against Database using page object validation
        expected_interface_count = len(network_interfaces)
        network_page.validate_network_form_interface_consistency(
            network_forms, expected_interface_count
        )

        logger.info(
            f"{device_model}: Network form count matches database expectations: {network_forms} >= {expected_interface_count}"
        )

        # 10. Variant Classification using page object method
        variant_type = network_page.classify_network_variant(
            network_forms, has_redundancy
        )

        # 11. Device Model-Specific Network Validation using page object methods
        if device_model == "KRONOS-3R-HVLV-TCXO-A2F":  # 66.3
            network_page.validate_device_66_3_network_variant()
            logger.info(
                f"{device_model}: Device 66.3 network validation passed - 4+ forms expected"
            )

        elif device_model == "KRONOS-3R-HVXX-TCXO-44A":  # 66.6
            network_page.validate_device_66_6_network_variant()
            logger.info(
                f"{device_model}: Device 66.6 network validation passed - 5+ forms expected"
            )

        elif device_model == "KRONOS-3R-HVXX-TCXO-A2X":  # 190.47
            network_page.validate_device_190_47_network_variant()
            logger.info(
                f"{device_model}: Device 190.47 network validation passed - 4+ forms expected"
            )

        # 12. Network Interface-Specific Validation using page object methods
        found_interfaces = network_page.validate_network_interface_configurations(
            network_interfaces
        )

        # 13. Interface Coverage Validation using page object validation
        network_page.validate_network_interface_coverage(
            found_interfaces, network_interfaces
        )

        logger.info(
            f"{device_model}: Network interface coverage: {len(found_interfaces)}/{len(network_interfaces)} interfaces found"
        )

        # 14. Redundancy Feature Validation using page object methods
        if has_redundancy:
            redundancy_validation = network_page.validate_redundancy_features()

            logger.info(
                f"{device_model}: Redundancy mode has {redundancy_validation['option_count']} options"
            )

            # Validate redundancy is supported by device capabilities using page object validation
            network_page.validate_redundancy_capability_support(capabilities)

        # 15. Additional Network Feature Validation using page object methods
        vlan_count = network_page.count_vlan_configuration_elements()
        if vlan_count > 0:
            logger.info(
                f"{device_model}: VLAN configuration found: {vlan_count} VLAN elements"
            )

        # Check for QoS or traffic shaping
        qos_count = network_page.count_qos_configuration_elements()
        if qos_count > 0:
            logger.info(
                f"{device_model}: QoS configuration found: {qos_count} QoS elements"
            )

        # 16. Final Validation Results using page object method
        final_status = network_page.generate_network_variant_detection_results(
            device_model,
            expected_series,
            network_interfaces,
            network_forms,
            found_interfaces,
            has_redundancy,
            variant_type,
            timeout_multiplier,
        )

        # 17. Comprehensive Logging and Reporting
        logger.info(f"{device_model}: Network variant detection completed successfully")
        logger.info(f"{device_model}: Detected variant: {variant_type}")
        logger.info(f"{device_model}: Network forms: {network_forms}")
        logger.info(f"{device_model}: Network interfaces: {network_interfaces}")
        logger.info(f"{device_model}: Found interfaces: {found_interfaces}")
        logger.info(f"{device_model}: Redundancy support: {has_redundancy}")
        logger.info(f"{device_model}: Network variant results: {final_status}")

        # 18. Success Validation using page object validation
        network_page.validate_network_variant_detection_success(
            expected_series, network_interfaces, found_interfaces, network_forms
        )

        # Cross-validation test using page object method
        network_page.test_network_variant_cross_validation()

        logger.info(f"{device_model}: Network variant detection validation passed")
        print(f"NETWORK VARIANT DETECTION COMPLETED: {device_model} - {variant_type}")
        print(
            f"Forms: {network_forms}, Interfaces: {network_interfaces}, Found: {found_interfaces}"
        )

    except Exception as e:
        logger.error(
            f"{device_model}: Network variant detection test encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"Network variant detection test failed for {device_model}: {e}")
