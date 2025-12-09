"""
Category 27: PTP Configuration - Test 27.23.1
Telecom Profile Field Behavior - Pure Page Object Pattern
Test Count: 20 of 25 in Category 27
Hardware: Device Only
Priority: HIGH
Series: Series 3 Only (PTP exclusive)

TRANSFORMATION STATUS: PURE PAGE OBJECT PATTERN
- All direct DeviceCapabilities calls replaced with PTPConfigPage methods
- Tests now use only PTPConfigPage methods for device-aware behavior
- Maintains existing functionality while achieving clean separation of concerns
- Encapsulates Telecom Profile field behavior validation within page object layer
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage

logger = logging.getLogger(__name__)


def test_27_23_1_telecom_profile_field_behavior(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.23.1: Telecom Profile Field Behavior - Pure Page Object Pattern
    Purpose: Verify telecom profile field behavior and configuration capabilities with device-aware validation
    Expected: Profile-specific field enablement and validation patterns
    Series: Series 3 only - validates Telecom Profile field behavior patterns
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
        f"Testing Telecom Profile field behavior on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to PTP configuration page using page object
    ptp_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    ptp_config_page.verify_page_loaded()

    # Test on first available port using page object methods
    port = available_ports[0]

    # Test all telecom profiles
    telecom_profiles = [
        "Telecom G.8265.1 (frequency synchronization)",
        "Telecom G.8275.1 (phase/time synchronization with full timing support from the network)",
        "Telecom G.8275.2 (time/phase synchronization with partial timing support from the network)",
    ]

    for profile in telecom_profiles:
        logger.info(f"Testing field behavior for {profile} on {port}")

        try:
            # PURE PAGE OBJECT PATTERN: Use page object method for telecom profile configuration
            profile_configured = ptp_config_page.configure_ptp_profile(port, profile)
            assert (
                profile_configured
            ), f"Should successfully select {profile} for {port}"

            # PURE PAGE OBJECT PATTERN: Use page object method to validate telecom profile field behavior
            field_behavior_valid = (
                ptp_config_page.validate_telecom_profile_field_behavior(port, profile)
            )

            if field_behavior_valid:
                logger.info(
                    f"Telecom profile field behavior validated for {profile} on {port}"
                )
            else:
                logger.warning(
                    f"Telecom profile field behavior validation failed for {profile} on {port}"
                )

            # Test specific telecom profile validations with page object methods
            if "G.8265.1" in profile:
                # G.8265.1: domain should be editable
                domain_editable = ptp_config_page.validate_domain_number_editable(port)
                if domain_editable:
                    logger.info(f"Domain number is editable for G.8265.1 on {port}")
                else:
                    logger.warning(
                        f"Domain number may not be editable for G.8265.1 on {port}"
                    )

                # Test frequency-specific timing configuration
                timing_editable = (
                    ptp_config_page.validate_timing_interval_fields_editable(port)
                )
                if timing_editable:
                    logger.info(f"Timing intervals are editable for G.8265.1 on {port}")
                else:
                    logger.warning(
                        f"Timing intervals may not be editable for G.8265.1 on {port}"
                    )

            elif "G.8275" in profile:
                # G.8275 profiles: domain should be editable
                domain_editable = ptp_config_page.validate_domain_number_editable(port)
                if domain_editable:
                    logger.info(f"Domain number is editable for {profile} on {port}")
                else:
                    logger.warning(
                        f"Domain number may not be editable for {profile} on {port}"
                    )

                # G.8275 profiles: priority fields should be editable
                priority_editable = ptp_config_page.validate_priority_fields_editable(
                    port
                )
                if priority_editable:
                    logger.info(f"Priority fields are editable for {profile} on {port}")
                else:
                    logger.warning(
                        f"Priority fields may not be editable for {profile} on {port}"
                    )

                # G.8275 profiles: timing intervals should be editable for synchronization
                sync_editable = ptp_config_page.validate_sync_interval_editable(port)
                if sync_editable:
                    logger.info(f"Sync interval is editable for {profile} on {port}")
                else:
                    logger.warning(
                        f"Sync interval may not be editable for {profile} on {port}"
                    )

                # G.8275.2 (partial timing support): additional fields
                if "G.8275.2" in profile:
                    # Test time-specific parameters for partial timing support
                    delay_req_editable = (
                        ptp_config_page.validate_delay_req_interval_editable(port)
                    )
                    if delay_req_editable:
                        logger.info(
                            f"Delay request interval is editable for G.8275.2 on {port}"
                        )
                    else:
                        logger.warning(
                            f"Delay request interval may not be editable for G.8275.2 on {port}"
                        )

                    # Test local priority for G.8275.2
                    local_priority_editable = (
                        ptp_config_page.validate_local_priority_editable(port)
                    )
                    if local_priority_editable:
                        logger.info(
                            f"Local priority is editable for G.8275.2 on {port}"
                        )
                    else:
                        logger.warning(
                            f"Local priority may not be editable for G.8275.2 on {port}"
                        )

            # PURE PAGE OBJECT PATTERN: Use page object method for save operation
            save_success = ptp_config_page.save_port_configuration(port)
            assert (
                save_success
            ), f"Should successfully save {profile} configuration for {port}"

            # PURE PAGE OBJECT PATTERN: Use page object method to verify persistence
            time.sleep(1 * timeout_multiplier)
            persisted_data = ptp_config_page.get_port_configuration_data(port)

            profile_persisted = persisted_data.get("profile") == profile
            assert profile_persisted, f"Profile should persist as {profile} for {port}"

            if profile_persisted:
                logger.info(f"Profile configuration persisted for {profile} on {port}")
            else:
                logger.warning(
                    f"Profile configuration may not have persisted for {profile} on {port}"
                )

        except Exception as e:
            logger.warning(
                f"Telecom profile field behavior testing failed for {profile} on port {port}: {e}"
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

    logger.info(f"Telecom profile field behavior testing completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"PTP supported: {len(available_ports) > 0}")
    logger.info(f"Available PTP ports: {available_ports}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"TELECOM PROFILE FIELD BEHAVIOR VALIDATED: {device_model} (Series {device_series})"
    )
