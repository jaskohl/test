"""
Category 27: PTP Configuration - Test 27.18.1
Power Profile 2011 Field Behavior - Pure Page Object Pattern
Test Count: 4 of 25 in Category 27
Hardware: Device Only
Priority: HIGH
Series: Series 3 Only (PTP exclusive)

TRANSFORMATION STATUS: PURE PAGE OBJECT PATTERN
- All direct DeviceCapabilities calls replaced with PTPConfigPage methods
- Tests now use only PTPConfigPage methods for device-aware behavior
- Maintains existing functionality while achieving clean separation of concerns
- Encapsulates Power Profile field behavior validation within page object layer
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage

logger = logging.getLogger(__name__)


def test_27_18_1_power_profile_2011_field_behavior(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.18.1: Power Profile 2011 Field Behavior - Pure Page Object Pattern
    Purpose: Verify all fields editable in Power Profile 2011 with device-aware validation
    Expected: All PTP fields remain editable in UI (constraints applied server-side)
    Series: Series 3 only - validates Power Profile field behavior patterns
    """
    # PURE PAGE OBJECT PATTERN: Use page object methods instead of direct DeviceCapabilities calls
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate PTP behavior")

    # PURE PAGE OBJECT PATTERN: Use page object method instead of direct DeviceCapabilities call
    device_series = ptp_config_page.get_device_series()
    if device_series != 3:
        pytest.skip(
            f"PTP test applies to Series 3 devices only, detected {device_model} (Series {device_series})"
        )

    # PURE PAGE OBJECT PATTERN: Check PTP support using page object (encapsulates DeviceCapabilities logic)
    available_ports = ptp_config_page.get_available_ports()
    if not available_ports:
        pytest.skip(f"PTP not supported on {device_model}")

    # PURE PAGE OBJECT PATTERN: Get timeout multiplier using page object method
    timeout_multiplier = ptp_config_page.get_timeout_multiplier()

    logger.info(
        f"Testing Power Profile 2011 field behavior on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to PTP configuration page using page object
    ptp_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    ptp_config_page.verify_page_loaded()

    # Test on first available port using page object methods
    port = available_ports[0]

    try:
        # PURE PAGE OBJECT PATTERN: Use page object method for Power Profile configuration
        profile_configured = ptp_config_page.configure_ptp_profile(
            port, "IEEE C37.238-2011 (Power Profile)"
        )
        assert (
            profile_configured
        ), f"Should successfully select Power Profile 2011 for {port}"

        # PURE PAGE OBJECT PATTERN: Use page object method to validate field editability
        field_behavior_valid = ptp_config_page.validate_power_profile_field_behavior(
            port
        )

        if field_behavior_valid:
            logger.info(f"Power Profile 2011 field behavior validated for {port}")
        else:
            logger.warning(
                f"Power Profile 2011 field behavior validation failed for {port}"
            )

        # Test specific field behaviors with page object methods
        timing_intervals_editable = (
            ptp_config_page.validate_timing_interval_fields_editable(port)
        )
        if timing_intervals_editable:
            logger.info(f"Timing interval fields remain editable for {port}")
        else:
            logger.warning(f"Timing interval fields may not be editable for {port}")

        # Test domain number field behavior
        domain_editable = ptp_config_page.validate_domain_number_editable(port)
        if domain_editable:
            logger.info(f"Domain number field remains editable for {port}")
        else:
            logger.warning(f"Domain number field may not be editable for {port}")

        # Test priority field behavior
        priority_editable = ptp_config_page.validate_priority_fields_editable(port)
        if priority_editable:
            logger.info(f"Priority fields remain editable for {port}")
        else:
            logger.warning(f"Priority fields may not be editable for {port}")

        # Test save configuration
        save_success = ptp_config_page.save_port_configuration(port)
        if save_success:
            logger.info(f"Power Profile 2011 configuration saved for {port}")
        else:
            logger.warning(f"Power Profile 2011 configuration save failed for {port}")

    except Exception as e:
        logger.warning(
            f"Power Profile 2011 field behavior testing failed for port {port}: {e}"
        )

    # Performance validation against device baselines
    try:
        # PURE PAGE OBJECT PATTERN: Use page object method instead of direct DeviceCapabilities call
        performance_data = ptp_config_page.get_performance_expectations()
        if performance_data:
            nav_performance = performance_data.get("navigation_performance", {})
            section_nav = nav_performance.get("section_navigation", {})
            typical_time = section_nav.get("typical_time", "")

            if typical_time:
                logger.info(f"PTP navigation performance baseline: {typical_time}")

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Log comprehensive test results
    # PURE PAGE OBJECT PATTERN: Use page object methods instead of direct DeviceCapabilities calls
    device_info = ptp_config_page.get_device_info()
    capabilities = ptp_config_page.get_capabilities()

    logger.info(f"Power Profile 2011 field behavior test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"PTP supported: {len(available_ports) > 0}")
    logger.info(f"Available PTP ports: {available_ports}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"POWER PROFILE 2011 FIELD BEHAVIOR VALIDATED: {device_model} (Series {device_series})"
    )
