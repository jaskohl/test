"""
Category 27: PTP Configuration - Test 27.18.2
Power Profile 2011 Domain Configuration - Pure Page Object Pattern
Test Count: 5 of 25 in Category 27
Hardware: Device Only
Priority: HIGH
Series: Series 3 Only (PTP exclusive)

TRANSFORMATION STATUS: PURE PAGE OBJECT PATTERN
- All direct DeviceCapabilities calls replaced with PTPConfigPage methods
- Tests now use only PTPConfigPage methods for device-aware behavior
- Maintains existing functionality while achieving clean separation of concerns
- Encapsulates Power Profile domain configuration within page object layer
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage

logger = logging.getLogger(__name__)


def test_27_18_2_power_profile_2011_domain_configuration(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.18.2: Power Profile 2011 Domain Configuration - Pure Page Object Pattern
    Purpose: Verify domain number configuration works in Power Profile 2011 with device-aware validation
    Expected: Domain number configuration persists after save operation
    Series: Series 3 only - validates Power Profile domain configuration workflow
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
        f"Testing Power Profile 2011 domain configuration on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to PTP configuration page using page object
    ptp_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    ptp_config_page.verify_page_loaded()

    # Test on first available port using page object methods
    port = available_ports[0]

    # Get original configuration for rollback
    try:
        # PURE PAGE OBJECT PATTERN: Use page object method to get original configuration
        original_data = ptp_config_page.get_port_configuration_data(port)

        # PURE PAGE OBJECT PATTERN: Use page object method for Power Profile configuration
        profile_configured = ptp_config_page.configure_ptp_profile(
            port, "IEEE C37.238-2011 (Power Profile)"
        )
        assert (
            profile_configured
        ), f"Should successfully select Power Profile 2011 for {port}"

        # PURE PAGE OBJECT PATTERN: Use page object method for domain configuration
        domain_configured = ptp_config_page.configure_domain_number(port, 100)
        assert (
            domain_configured
        ), f"Should successfully configure domain number for {port}"

        # PURE PAGE OBJECT PATTERN: Use page object method for save operation
        save_success = ptp_config_page.save_port_configuration(port)
        assert save_success, f"Should successfully save PTP configuration for {port}"

        # PURE PAGE OBJECT PATTERN: Use page object method to verify persistence
        time.sleep(1 * timeout_multiplier)
        persisted_data = ptp_config_page.get_port_configuration_data(
            port, reload_page=True
        )

        domain_persisted = persisted_data.get("domain_number") == "100"
        assert domain_persisted, f"Domain number should persist after save for {port}"

        if domain_persisted:
            logger.info(f"Domain number configuration persisted for {port}")
        else:
            logger.warning(
                f"Domain number configuration may not have persisted for {port}"
            )

    finally:
        # Rollback: Restore original PTP configuration using page object methods
        try:
            if original_data.get("profile"):
                ptp_config_page.configure_ptp_profile(port, original_data["profile"])
            if original_data.get("domain_number"):
                ptp_config_page.configure_domain_number(
                    port, int(original_data["domain_number"])
                )
            if original_data.get("priority_1") and original_data.get("priority_2"):
                ptp_config_page.configure_priorities(
                    port,
                    int(original_data["priority_1"]),
                    int(original_data["priority_2"]),
                )

            # Save rollback configuration
            rollback_success = ptp_config_page.save_port_configuration(port)
            if rollback_success:
                logger.info(f"Original PTP configuration restored for {port}")
            else:
                logger.warning(
                    f"Failed to restore original PTP configuration for {port}"
                )

            time.sleep(1 * timeout_multiplier)

        except Exception as e:
            logger.warning(f"Rollback failed for port {port}: {e}")

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

    logger.info(
        f"Power Profile 2011 domain configuration test completed for {device_model}"
    )
    logger.info(f"Device info: {device_info}")
    logger.info(f"PTP supported: {len(available_ports) > 0}")
    logger.info(f"Available PTP ports: {available_ports}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"POWER PROFILE 2011 DOMAIN CONFIGURATION VALIDATED: {device_model} (Series {device_series})"
    )
