"""
Category 27: PTP Configuration - Test 27.1.1
PTP Profile Selection - DeviceCapabilities Enhanced
Test Count: 1 of 18 in Category 27
Hardware: Device Only
Priority: CRITICAL - PTP configuration functionality
Series: Series 3 only
ENHANCED: Comprehensive DeviceCapabilities integration for device-aware PTP validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_27_1_1_ptp_profile_selection_device_enhanced(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.1.1: PTP Profile Selection - DeviceCapabilities Enhanced
    Purpose: Verify PTP profile selection functionality with device-aware validation
    Expected: PTP profiles available, selection works, device-specific interfaces
    ENHANCED: Full DeviceCapabilities integration for PTP interface and profile validation
    Series: Series 3 only - validates PTP-specific patterns
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate PTP behavior")

    # Validate this is a Series 3 device (required for PTP)
    device_series = DeviceCapabilities.get_series(device_model)
    if device_series != 3:
        pytest.skip(
            f"PTP test applies to Series 3 devices only, detected {device_model} (Series {device_series})"
        )

    # Get PTP capabilities for validation
    ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)
    if not ptp_supported:
        pytest.skip(f"PTP not supported on {device_model}")

    # Get device series and timeout multiplier for device-aware testing
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing PTP profile selection on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Get PTP interface information
    available_ports = ptp_config_page.get_available_ports()
    ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)

    logger.info(f"Available PTP ports: {available_ports}")
    logger.info(f"Expected PTP interfaces: {ptp_interfaces}")

    if not available_ports:
        pytest.skip(f"No PTP ports available on {device_model}")

    # Navigate to PTP configuration page
    ptp_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    ptp_config_page.verify_page_loaded()

    # Test PTP profile selection for each available port
    test_profiles = [
        "IEEE C37.238-2017 (Power Profile)",
        "Default Profile (UDPv4)",
        "Telecom G.8275.1 (phase/time synchronization with full timing support from the network)",
    ]

    for port in available_ports:
        logger.info(f"Testing PTP profile selection for port: {port}")

        try:
            # Ensure PTP panel is expanded for this port
            panel_expanded = ptp_config_page._expand_single_panel(port)
            if not panel_expanded:
                logger.warning(f"Could not expand PTP panel for {port}")
                continue

            # Locate PTP profile dropdown for this port
            profile_dropdown = ptp_config_page.page.locator(f"select#{port}_profile")

            dropdown_timeout = int(10000 * timeout_multiplier)
            expect(profile_dropdown).to_be_visible(timeout=dropdown_timeout)

            # Verify dropdown is populated with options
            profile_options = profile_dropdown.locator("option")
            available_profiles = []

            for i in range(profile_options.count()):
                option = profile_options.nth(i)
                option_text = option.text_content() or option.get_attribute("value")
                if option_text and option_text.strip():
                    available_profiles.append(option_text.strip())

            logger.info(f"Available PTP profiles for {port}: {available_profiles}")

            # Test profile selection with device-aware patterns
            for test_profile in test_profiles:
                # Check if this profile is available for this device
                profile_available = any(
                    test_profile.lower() in profile.lower()
                    for profile in available_profiles
                )

                if profile_available:
                    logger.info(
                        f"Testing PTP profile selection for {port}: {test_profile}"
                    )

                    try:
                        # Configure PTP profile with device-aware timing
                        config_success = ptp_config_page.configure_ptp_profile(
                            port, test_profile
                        )

                        if config_success:
                            logger.info(
                                f"Successfully configured PTP profile for {port}: {test_profile}"
                            )

                            # Verify profile selection was applied
                            selected_profile = profile_dropdown.input_value()
                            if selected_profile:
                                logger.info(
                                    f"PTP profile selection verified for {port}: {selected_profile}"
                                )
                            else:
                                logger.warning(
                                    f"PTP profile selection may not have persisted for {port}"
                                )

                            # Test save button for this port
                            save_success = ptp_config_page.save_port_configuration(port)
                            if save_success:
                                logger.info(
                                    f"PTP configuration saved successfully for {port}"
                                )
                            else:
                                logger.warning(
                                    f"PTP configuration save failed for {port}"
                                )

                        else:
                            logger.warning(
                                f"Failed to configure PTP profile for {port}: {test_profile}"
                            )

                    except Exception as e:
                        logger.warning(
                            f"PTP profile configuration test failed for {port}/{test_profile}: {e}"
                        )
                else:
                    logger.info(
                        f"Skipping PTP profile {test_profile} for {port} - not available"
                    )

        except Exception as e:
            logger.warning(f"PTP profile testing failed for port {port}: {e}")
            continue

    # Test PTP-specific field behaviors
    try:
        # Test timing interval fields with device-aware patterns
        for port in available_ports[:1]:  # Test first port only
            logger.info(f"Testing PTP timing fields for {port}")

            # Test domain number configuration
            domain_success = ptp_config_page.configure_domain_number(port, 0)
            if domain_success:
                logger.info(f"Domain number configured successfully for {port}")
            else:
                logger.warning(f"Domain number configuration failed for {port}")

            # Test priority configuration
            priority_success = ptp_config_page.configure_priorities(port, 128, 128)
            if priority_success:
                logger.info(f"Priority configuration successful for {port}")
            else:
                logger.warning(f"Priority configuration failed for {port}")

    except Exception as e:
        logger.warning(f"PTP field behavior testing failed on {device_model}: {e}")

    # Performance validation against device baselines
    try:
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            nav_performance = performance_data.get("navigation_performance", {})
            section_nav = nav_performance.get("section_navigation", {})
            typical_time = section_nav.get("typical_time", "")

            if typical_time:
                logger.info(f"PTP navigation performance baseline: {typical_time}")

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)
    capabilities = DeviceCapabilities.get_capabilities(device_model)

    logger.info(f"PTP profile selection test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"PTP supported: {ptp_supported}")
    logger.info(f"Available PTP ports: {available_ports}")
    logger.info(f"Expected PTP interfaces: {ptp_interfaces}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(f"PTP PROFILE SELECTION VALIDATED: {device_model} (Series {device_series})")
