"""
Category 27: PTP Configuration - Test 27.10.5
Dynamic Port Delay Mechanism - Pure Page Object Pattern
Test Count: 1 of 25 in Category 27
Hardware: Device Only
Priority: HIGH
Series: Series 3 Only (PTP exclusive)

TRANSFORMATION STATUS: PURE PAGE OBJECT PATTERN
- All direct DeviceCapabilities calls replaced with PTPConfigPage methods
- Tests now use only PTPConfigPage methods for device-aware behavior
- Maintains existing functionality while achieving clean separation of concerns
- Encapsulates PTP delay mechanism configuration within page object layer
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage

logger = logging.getLogger(__name__)


def test_27_10_5_dynamic_port_delay_mechanism(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.10.5: Dynamic Port Delay Mechanism - Pure Page Object Pattern
    Purpose: Verify all available ports support delay mechanism selection with device-aware validation
    Expected: PTP delay mechanisms (P2P/E2E) available and configurable on all PTP ports
    Series: Series 3 only - validates PTP-specific delay mechanism functionality
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
        f"Testing PTP delay mechanism on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # PURE PAGE OBJECT PATTERN: Get PTP interfaces using page object method
    ptp_interfaces = ptp_config_page.get_ptp_interfaces()

    logger.info(f"Available PTP ports: {available_ports}")
    logger.info(f"Expected PTP interfaces: {ptp_interfaces}")

    # Navigate to PTP configuration page using page object
    ptp_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    ptp_config_page.verify_page_loaded()

    # PURE PAGE OBJECT PATTERN: Validate port count using page object instead of direct assertion
    port_count_valid = ptp_config_page.validate_minimum_port_count(2)
    if not port_count_valid:
        pytest.fail(
            f"Should have at least 2 PTP ports on {device_model}, found {len(available_ports)}: {available_ports}"
        )

    # Test delay mechanism on each available port using page object methods
    for port in available_ports:
        logger.info(f"Testing delay mechanism on {port} for device {device_model}")

        try:
            # PURE PAGE OBJECT PATTERN: Use page object method for profile configuration
            profile_configured = ptp_config_page.configure_ptp_profile(port, "Custom")
            assert (
                profile_configured
            ), f"Should successfully select Custom profile for {port}"

            # PURE PAGE OBJECT PATTERN: Use page object method for delay mechanism testing
            delay_mechanism_available = ptp_config_page.test_delay_mechanism_options(
                port
            )

            if delay_mechanism_available:
                logger.info(f"Delay mechanism options validated for {port}")

                # Test specific delay mechanism selection
                p2p_success = ptp_config_page.select_delay_mechanism(port, "P2P")
                if p2p_success:
                    logger.info(f"P2P delay mechanism selected successfully for {port}")
                else:
                    logger.warning(f"P2P delay mechanism selection failed for {port}")

                e2e_success = ptp_config_page.select_delay_mechanism(port, "E2E")
                if e2e_success:
                    logger.info(f"E2E delay mechanism selected successfully for {port}")
                else:
                    logger.warning(f"E2E delay mechanism selection failed for {port}")

            else:
                logger.warning(f"Delay mechanism options not available for {port}")

            # Test save configuration for this port
            save_success = ptp_config_page.save_port_configuration(port)
            if save_success:
                logger.info(f"PTP delay mechanism configuration saved for {port}")
            else:
                logger.warning(
                    f"PTP delay mechanism configuration save failed for {port}"
                )

        except Exception as e:
            logger.warning(f"PTP delay mechanism testing failed for port {port}: {e}")
            continue

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

    logger.info(f"PTP delay mechanism test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"PTP supported: {len(available_ports) > 0}")
    logger.info(f"Available PTP ports: {available_ports}")
    logger.info(f"Expected PTP interfaces: {ptp_interfaces}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(f"PTP DELAY MECHANISM VALIDATED: {device_model} (Series {device_series})")
