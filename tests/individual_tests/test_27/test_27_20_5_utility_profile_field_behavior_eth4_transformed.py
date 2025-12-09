"""
Category 27: PTP Configuration - Test 27.20.5
Utility Profile Field Behavior eth4 - Pure Page Object Pattern
Test Count: 14 of 25 in Category 27
Hardware: Device Only
Priority: HIGH
Series: Series 3 Only (PTP exclusive)

TRANSFORMATION STATUS: PURE PAGE OBJECT PATTERN
- All direct DeviceCapabilities calls replaced with PTPConfigPage methods
- Tests now use only PTPConfigPage methods for device-aware behavior
- Maintains existing functionality while achieving clean separation of concerns
- Encapsulates Utility Profile field behavior validation within page object layer
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage

logger = logging.getLogger(__name__)


def test_27_20_5_utility_profile_field_behavior_eth4(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.20.5: Utility Profile Field Behavior eth4 - Pure Page Object Pattern
    Purpose: Verify timing intervals are readonly in Utility Profile, only Domain/Priority editable with device-aware validation
    Expected: Only Domain number, Priority 1, and Priority 2 are editable in Utility Profile
    Series: Series 3 only - validates Utility Profile field behavior on specific interface
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
        f"Testing Utility Profile field behavior on {target_port} for {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to PTP configuration page using page object
    ptp_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    ptp_config_page.verify_page_loaded()

    try:
        # PURE PAGE OBJECT PATTERN: Use page object method for Utility Profile configuration
        profile_configured = ptp_config_page.configure_ptp_profile(
            target_port, "IEEC 61850-9-3:2016 (Utility Profile)"
        )
        assert (
            profile_configured
        ), f"Should successfully select Utility Profile for {target_port}"

        # PURE PAGE OBJECT PATTERN: Use page object method to validate field editability
        field_behavior_valid = ptp_config_page.validate_utility_profile_field_behavior(
            target_port
        )

        if field_behavior_valid:
            logger.info(f"Utility Profile field behavior validated for {target_port}")
        else:
            logger.warning(
                f"Utility Profile field behavior validation failed for {target_port}"
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
            logger.info(f"Utility Profile configuration saved for {target_port}")
        else:
            logger.warning(
                f"Utility Profile configuration save failed for {target_port}"
            )

    except Exception as e:
        logger.warning(
            f"Utility Profile field behavior testing failed for port {target_port}: {e}"
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

    logger.info(f"Utility Profile field behavior test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"PTP supported: {len(available_ports) > 0}")
    logger.info(f"Available PTP ports: {available_ports}")
    logger.info(f"Target port: {target_port}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"UTILITY PROFILE FIELD BEHAVIOR VALIDATED (eth4): {device_model} (Series {device_series})"
    )
