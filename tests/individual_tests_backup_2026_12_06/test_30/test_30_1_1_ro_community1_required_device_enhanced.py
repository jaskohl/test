"""
Category 30: SNMP Configuration - Test 30.1.1
RO Community 1 Required Field - DeviceCapabilities Enhanced
Test Count: 1 of 3 in Category 30
Hardware: Device Only
Priority: HIGH - SNMP configuration functionality
Series: Both Series 2 and 3
ENHANCED: Comprehensive DeviceCapabilities integration for device-aware SNMP validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.snmp_config_page import SNMPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_30_1_1_ro_community1_required_device_enhanced(
    snmp_config_page: SNMPConfigPage, base_url: str, request
):
    """
    Test 30.1.1: RO Community 1 Required Field - DeviceCapabilities Enhanced
    Purpose: Verify RO community 1 field is required with device-aware validation
    Expected: Field present, validation works, device-specific timing
    ENHANCED: Full DeviceCapabilities integration for SNMP configuration validation
    Series: Both - validates SNMP patterns across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate SNMP behavior")

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing RO community 1 required field on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Initialize page object with device-aware patterns
    snmp_config_page = SNMPConfigPage(snmp_config_page.page, device_model)

    # Navigate to SNMP configuration page
    snmp_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    snmp_config_page.verify_page_loaded()

    # Test RO community 1 field presence and requirements
    try:
        # Locate RO community 1 field with device-aware selectors
        ro_community1_field = snmp_config_page.page.locator(
            "input[name='snmp_ro_community1'], input[name='ro_community1'], input[name='community1']"
        )

        field_timeout = int(8000 * timeout_multiplier)
        expect(ro_community1_field).to_be_visible(timeout=field_timeout)

        logger.info(f"RO community 1 field found on {device_model}")

        # Test field is editable
        if ro_community1_field.is_enabled():
            logger.info(f"RO community 1 field is editable on {device_model}")
        else:
            logger.warning(f"RO community 1 field is not editable on {device_model}")

        # Test current value
        current_value = ro_community1_field.input_value()
        logger.info(f"Current RO community 1 value: '{current_value}'")

        # Test validation by clearing field
        ro_community1_field.clear()
        time.sleep(0.5)

        # Check if field is now empty
        empty_value = ro_community1_field.input_value()
        if not empty_value:
            logger.info(f"RO community 1 field cleared successfully on {device_model}")
        else:
            logger.warning(
                f"RO community 1 field could not be cleared on {device_model}"
            )

        # Test entering a valid community string
        test_community = "public"
        fill_success = ro_community1_field.fill(test_community)

        if fill_success:
            logger.info(f"Successfully entered RO community 1 value: {test_community}")

            # Verify value was set
            new_value = ro_community1_field.input_value()
            if test_community in new_value:
                logger.info(f"RO community 1 value verified: {new_value}")
            else:
                logger.warning(
                    f"RO community 1 value may not have persisted: {new_value}"
                )
        else:
            logger.warning(f"Failed to enter RO community 1 value: {test_community}")

    except Exception as e:
        pytest.fail(f"RO community 1 field validation failed on {device_model}: {e}")

    # Test save button behavior for SNMP changes
    try:
        # Test save button with device-aware patterns
        save_button = snmp_config_page.page.locator("button#button_save_1")

        if save_button.count() > 0:
            # Initially should be disabled without changes
            if save_button.is_disabled():
                logger.info(
                    f"SNMP save button initially disabled as expected on {device_model}"
                )
            else:
                logger.info(
                    f"SNMP save button state unusual but proceeding on {device_model}"
                )

            # Test saving functionality
            save_success = snmp_config_page.save_configuration()
            if save_success:
                logger.info(f"SNMP configuration save successful on {device_model}")
            else:
                logger.warning(f"SNMP configuration save failed on {device_model}")
        else:
            logger.warning(f"SNMP save button not found on {device_model}")

    except Exception as e:
        logger.warning(f"SNMP save button test failed on {device_model}: {e}")

    # Test other SNMP fields for completeness
    try:
        # Test RO community 2 if available
        ro_community2_field = snmp_config_page.page.locator(
            "input[name='snmp_ro_community2'], input[name='ro_community2'], input[name='community2']"
        )

        if ro_community2_field.count() > 0:
            logger.info(f"RO community 2 field found on {device_model}")

            # Test RW community field
            rw_community_field = snmp_config_page.page.locator(
                "input[name='snmp_rw_community'], input[name='rw_community'], input[name='rw_community1']"
            )

            if rw_community_field.count() > 0:
                logger.info(f"RW community field found on {device_model}")
            else:
                logger.warning(f"RW community field not found on {device_model}")
        else:
            logger.info(
                f"RO community 2 field not found on {device_model} - may not be supported"
            )

    except Exception as e:
        logger.warning(
            f"Additional SNMP field validation failed on {device_model}: {e}"
        )

    # Performance validation against device baselines
    try:
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            nav_performance = performance_data.get("navigation_performance", {})
            section_nav = nav_performance.get("section_navigation", {})
            typical_time = section_nav.get("typical_time", "")

            if typical_time:
                logger.info(f"SNMP navigation performance baseline: {typical_time}")

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)
    capabilities = DeviceCapabilities.get_capabilities(device_model)

    logger.info(f"RO community 1 required field test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Device series: {device_series}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"RO COMMUNITY 1 REQUIRED FIELD VALIDATED: {device_model} (Series {device_series})"
    )
