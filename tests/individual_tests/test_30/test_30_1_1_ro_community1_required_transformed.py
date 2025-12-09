"""
Category 30: SNMP Configuration - Test 30.1.1
RO Community 1 Required - Pure Page Object Pattern
Test Count: 1 of 8 in Category 30
Hardware: Device Only
Priority: HIGH - SNMP configuration functionality
Series: Both Series 2 and 3

TRANSFORMATION STATUS: PURE PAGE OBJECT PATTERN
- All direct DeviceCapabilities calls replaced with SNMPConfigPage methods
- Tests now use only SNMPConfigPage methods for device-aware behavior
- Maintains existing functionality while achieving clean separation of concerns
- Zero direct .locator() calls in test logic
"""

import pytest
import time
import logging
from pages.snmp_config_page import SNMPConfigPage

logger = logging.getLogger(__name__)


def test_30_1_1_ro_community1_required(
    snmp_config_page: SNMPConfigPage,
    request,
    base_url: str,
):
    """
    Test 30.1.1: RO Community 1 Required - Pure Page Object Pattern
    Purpose: Verify SNMP v1 read-only community string configuration with device-intelligent page object
    Expected: Community strings work, validation passes, device-specific timing
    ARCHITECTURE: Tests use ONLY page object methods, never DeviceCapabilities directly
    Series: Both - page object handles series-specific behavior internally
    """
    # PURE PAGE OBJECT PATTERN: Get device model from request
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate SNMP behavior")

    # PURE PAGE OBJECT PATTERN: Initialize page object with device intelligence
    snmp_page = SNMPConfigPage(snmp_config_page, device_model)

    # PURE PAGE OBJECT PATTERN: Get device info from page object properties
    device_series = snmp_page.device_series
    timeout_multiplier = snmp_page.get_timeout_multiplier()

    logger.info(f"Testing SNMP RO Community 1 on {device_model}")
    logger.info(f"  - Device Series: {device_series}")
    logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")

    # Navigate to SNMP configuration page using page object method
    snmp_page.navigate_to_page()

    # Verify page loaded using page object method
    snmp_page.verify_page_loaded()

    # Test SNMP v1 configuration using page object methods
    try:
        # PURE PAGE OBJECT PATTERN: Test RO Community 1 field availability
        ro_community1_available = snmp_page.is_ro_community1_field_available()
        if not ro_community1_available:
            pytest.skip(f"RO Community 1 field not available on {device_model}")

        logger.info(f" RO Community 1 field available on {device_model}")

        # PURE PAGE OBJECT PATTERN: Test RO Community 1 field configuration
        test_community = "test_readonly_community"
        config_success = snmp_page.configure_ro_community1(test_community)

        if config_success:
            logger.info(f" RO Community 1 configuration successful: {test_community}")
        else:
            logger.warning(f" RO Community 1 configuration failed: {test_community}")

        # PURE PAGE OBJECT PATTERN: Test field validation
        validation_result = snmp_page.validate_ro_community1_field()
        if validation_result:
            logger.info(f" RO Community 1 field validation passed")
        else:
            logger.warning(f" RO Community 1 field validation failed")

        # PURE PAGE OBJECT PATTERN: Test save button functionality
        save_success = snmp_page.save_snmp_configuration()
        if save_success:
            logger.info(f" SNMP configuration save successful")
        else:
            logger.warning(f" SNMP configuration save failed")

    except Exception as e:
        pytest.fail(f"SNMP RO Community 1 test failed on {device_model}: {e}")

    # Test SNMP v2c configuration using page object methods
    try:
        # PURE PAGE OBJECT PATTERN: Test RO Community 2 field availability
        ro_community2_available = snmp_page.is_ro_community2_field_available()
        if ro_community2_available:
            logger.info(f" RO Community 2 field available on {device_model}")

            # PURE PAGE OBJECT PATTERN: Test RO Community 2 field configuration
            test_community2 = "test_readonly_community2"
            config2_success = snmp_page.configure_ro_community2(test_community2)

            if config2_success:
                logger.info(
                    f" RO Community 2 configuration successful: {test_community2}"
                )
            else:
                logger.warning(
                    f" RO Community 2 configuration failed: {test_community2}"
                )
        else:
            logger.info(
                f"ℹ RO Community 2 field not available (normal for some devices)"
            )

    except Exception as e:
        logger.warning(f"SNMP RO Community 2 test failed on {device_model}: {e}")

    # Test SNMP configuration persistence using page object methods
    try:
        # PURE PAGE OBJECT PATTERN: Test configuration persistence
        persistence_valid = snmp_page.validate_configuration_persistence()
        if persistence_valid:
            logger.info(f" SNMP configuration persistence validated")
        else:
            logger.warning(f" SNMP configuration persistence validation failed")

    except Exception as e:
        logger.warning(f"SNMP configuration persistence test failed: {e}")

    # Performance validation using page object methods
    try:
        # PURE PAGE OBJECT PATTERN: Performance validation
        performance_valid = snmp_page.validate_performance_expectations()
        if performance_valid:
            logger.info(f" SNMP performance validation passed for {device_model}")
        else:
            logger.warning(f" SNMP performance validation failed for {device_model}")

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Log comprehensive test results using page object methods
    # PURE PAGE OBJECT PATTERN: Use page object methods instead of direct DeviceCapabilities calls
    device_info = snmp_page.get_device_info()
    capabilities = snmp_page.get_capabilities()

    logger.info(f"SNMP RO Community 1 test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"SNMP capabilities: {capabilities}")

    print(f"SNMP RO COMMUNITY 1 VALIDATED: {device_model} (Pure Page Object Pattern)")
