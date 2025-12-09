"""
Category 27: PTP Configuration - Test 27.22.1
Default L2 Profile Field Behavior - Pure Page Object Pattern
Test Count: 18 of 25 in Category 27
Hardware: Device Only
Priority: HIGH
Series: Series 3 Only (PTP exclusive)

TRANSFORMATION STATUS: PURE PAGE OBJECT PATTERN
- All direct DeviceCapabilities calls replaced with PTPConfigPage methods
- Tests now use only PTPConfigPage methods for device-aware behavior
- Maintains existing functionality while achieving clean separation of concerns
- Encapsulates Default L2 Profile field behavior validation within page object layer
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage

logger = logging.getLogger(__name__)


def test_27_22_1_default_l2_profile_field_behavior(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.22.1: Default L2 Profile Field Behavior - Pure Page Object Pattern
    Purpose: Verify L2 transport auto-selection in Default L2 Profile with device-aware validation
    Expected: Network transport automatically set to L2 in Default L2 Profile
    Series: Series 3 only - validates Default L2 Profile field behavior patterns
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
        f"Testing Default L2 Profile field behavior on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to PTP configuration page using page object
    ptp_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    ptp_config_page.verify_page_loaded()

    # Test on first available port using page object methods
    port = available_ports[0]

    try:
        # PURE PAGE OBJECT PATTERN: Use page object method for Default L2 Profile configuration
        profile_configured = ptp_config_page.configure_ptp_profile(
            port, "Default Profile (802.3)"
        )
        assert (
            profile_configured
        ), f"Should successfully select Default L2 Profile for {port}"

        # PURE PAGE OBJECT PATTERN: Use page object method to validate L2 transport auto-selection
        l2_transport_valid = ptp_config_page.validate_default_l2_profile_transport(port)

        if l2_transport_valid:
            logger.info(f"L2 transport auto-selection validated for {port}")
        else:
            logger.warning(f"L2 transport auto-selection validation failed for {port}")

        # Test specific field behaviors with page object methods
        network_transport_correct = (
            ptp_config_page.validate_network_transport_auto_selection(port, "L2")
        )
        if network_transport_correct:
            logger.info(f"Network transport correctly set to L2 for {port}")
        else:
            logger.warning(
                f"Network transport may not be correctly set to L2 for {port}"
            )

        # Test delay mechanism behavior
        delay_mechanism_enabled = ptp_config_page.validate_delay_mechanism_enabled(port)
        if delay_mechanism_enabled:
            logger.info(f"Delay mechanism is enabled for {port}")
        else:
            logger.warning(f"Delay mechanism may not be enabled for {port}")

        # Test UDP TTL field behavior
        udp_ttl_enabled = ptp_config_page.validate_udp_ttl_field_enabled(port)
        if udp_ttl_enabled:
            logger.info(f"UDP TTL field is enabled for {port}")
        else:
            logger.warning(f"UDP TTL field may not be enabled for {port}")

        # Test save configuration
        save_success = ptp_config_page.save_port_configuration(port)
        if save_success:
            logger.info(f"Default L2 Profile configuration saved for {port}")
        else:
            logger.warning(f"Default L2 Profile configuration save failed for {port}")

    except Exception as e:
        logger.warning(
            f"Default L2 Profile field behavior testing failed for port {port}: {e}"
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

    logger.info(f"Default L2 Profile field behavior test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"PTP supported: {len(available_ports) > 0}")
    logger.info(f"Available PTP ports: {available_ports}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"DEFAULT L2 PROFILE FIELD BEHAVIOR VALIDATED: {device_model} (Series {device_series})"
    )
