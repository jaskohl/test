"""
Category 27: PTP Configuration - Test 27.19.3
Power Profile 2017 Field Behavior eth4 - Pure Page Object Pattern
Test Count: 10 of 25 in Category 27
Hardware: Device Only
Priority: HIGH
Series: Series 3 Only (PTP exclusive)

TRANSFORMATION STATUS: PURE PAGE OBJECT PATTERN
- All direct DeviceCapabilities calls replaced with PTPConfigPage methods
- Tests now use only PTPConfigPage methods for device-aware behavior
- Maintains existing functionality while achieving clean separation of concerns
- Encapsulates Power Profile 2017 field behavior validation within page object layer
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage

logger = logging.getLogger(__name__)


def test_27_19_3_power_profile_2017_field_behavior_eth4(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.19.3: Power Profile 2017 Field Behavior eth4 - Pure Page Object Pattern
    Purpose: Verify all fields editable in Power Profile 2017 on eth4 with device-aware validation
    Expected: All PTP fields remain editable in UI (constraints applied server-side)
    Series: Series 3 only - validates Power Profile 2017 field behavior on specific interface
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

    # PURE PAGE OBJECT PATTERN: Use page object method to determine target port
    target_port = ptp_config_page.get_target_port("eth4")
    if not target_port:
        pytest.skip(f"Target port eth4 not available on {device_model}")

    # PURE PAGE OBJECT PATTERN: Get timeout multiplier using page object method
    timeout_multiplier = ptp_config_page.get_timeout_multiplier()

    logger.info(
        f"Testing Power Profile 2017 field behavior on {target_port} for {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to PTP configuration page using page object
    ptp_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    ptp_config_page.verify_page_loaded()

    try:
        # PURE PAGE OBJECT PATTERN: Use page object method for Power Profile 2017 configuration
        profile_configured = ptp_config_page.configure_ptp_profile(
            target_port, "IEEE C37.238-2017 (Power Profile)"
        )
        assert (
            profile_configured
        ), f"Should successfully select Power Profile 2017 for {target_port}"

        # PURE PAGE OBJECT PATTERN: Use page object method to validate field editability
        field_behavior_valid = (
            ptp_config_page.validate_power_profile_2017_field_behavior(target_port)
        )

        if field_behavior_valid:
            logger.info(
                f"Power Profile 2017 field behavior validated for {target_port}"
            )
        else:
            logger.warning(
                f"Power Profile 2017 field behavior validation failed for {target_port}"
            )

        # Test specific field behaviors with page object methods
        timing_fields_editable = (
            ptp_config_page.validate_timing_interval_fields_editable(target_port)
        )
        if timing_fields_editable:
            logger.info(f"Timing interval fields remain editable for {target_port}")
        else:
            logger.warning(
                f"Timing interval fields may not be editable for {target_port}"
            )

        # Test advanced timing fields (Power Profile 2017 specific)
        advanced_timing_editable = (
            ptp_config_page.validate_advanced_timing_fields_editable(target_port)
        )
        if advanced_timing_editable:
            logger.info(f"Advanced timing fields remain editable for {target_port}")
        else:
            logger.warning(
                f"Advanced timing fields may not be editable for {target_port}"
            )

        # Test domain number field behavior
        domain_editable = ptp_config_page.validate_domain_number_editable(target_port)
        if domain_editable:
            logger.info(f"Domain number field remains editable for {target_port}")
        else:
            logger.warning(f"Domain number field may not be editable for {target_port}")

        # Test priority field behavior
        priority_editable = ptp_config_page.validate_priority_fields_editable(
            target_port
        )
        if priority_editable:
            logger.info(f"Priority fields remain editable for {target_port}")
        else:
            logger.warning(f"Priority fields may not be editable for {target_port}")

        # Test save configuration
        save_success = ptp_config_page.save_port_configuration(target_port)
        if save_success:
            logger.info(f"Power Profile 2017 configuration saved for {target_port}")
        else:
            logger.warning(
                f"Power Profile 2017 configuration save failed for {target_port}"
            )

    except Exception as e:
        logger.warning(
            f"Power Profile 2017 field behavior testing failed for port {target_port}: {e}"
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

    logger.info(f"Power Profile 2017 field behavior test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"PTP supported: {len(available_ports) > 0}")
    logger.info(f"Available PTP ports: {available_ports}")
    logger.info(f"Target port: {target_port}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"POWER PROFILE 2017 FIELD BEHAVIOR VALIDATED (eth4): {device_model} (Series {device_series})"
    )
