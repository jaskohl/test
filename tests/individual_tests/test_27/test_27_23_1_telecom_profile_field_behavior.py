"""
Test 27.23.1: Telecom Profile Field Behavior
Purpose: Verify telecom profile field behavior and configuration capabilities
Series: Series 3 Only
Device Behavior: Profile-specific field enablement and validation patterns
Based on test_27_ptp_config.py line 1021 - MODERNIZED v3.0
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


"""Test telecom profile field behavior and configuration validation."""


def test_27_23_1_telecom_profile_field_behavior(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.23.1: Telecom Profile Field Behavior
    Purpose: Verify telecom profile field behavior and configuration capabilities
    Series: Series 3 Only
    Device Behavior: Profile-specific field enablement and validation patterns
    MODERNIZED: DeviceCapabilities integration with timeout multipliers
    """
    # MODERNIZED: Use request.session.device_hardware_model instead of device_capabilities fixture
    device_model = request.session.device_hardware_model
    if device_model == "Unknown":
        pytest.fail("Device model not detected - cannot determine PTP capabilities")

    device_series = DeviceCapabilities.get_series(device_model)
    if device_series != "Series 3":
        pytest.skip("PTP is Series 3 exclusive")

    # MODERNIZED: Apply timeout multiplier for device-aware testing
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    logger.info(
        f"Testing Telecom Profile field behavior on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to PTP page
    ptp_config_page.page.goto(f"{base_url}/ptp")
    time.sleep(2 * timeout_multiplier)
    # Use heading role instead of text to avoid strict mode violation
    ptp_heading = ptp_config_page.page.get_by_role("heading", name="PTP")
    expect(ptp_heading).to_be_visible()

    # Get available ports using DeviceCapabilities
    static_ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)
    if not static_ptp_interfaces:
        pytest.skip(f"No PTP interfaces available on device model {device_model}")

    assert len(static_ptp_interfaces) >= 1, "At least one PTP port should be available"
    # Test on first available port
    port = static_ptp_interfaces[0]

    # Test all telecom profiles
    telecom_profiles = [
        "Telecom G.8265.1 (frequency synchronization)",
        "Telecom G.8275.1 (phase/time synchronization with full timing support from the network)",
        "Telecom G.8275.2 (time/phase synchronization with partial timing support from the network)",
    ]

    for profile in telecom_profiles:
        logger.info(f"Testing field behavior for {profile} on {port}")

        # Select telecom profile
        result = ptp_config_page.configure_ptp_profile(port, profile)
        assert result, f"Should successfully select {profile} for {port}"

        # Test G.8265.1 (frequency synchronization) specific behavior
        if "G.8265.1" in profile:
            # G.8265.1: domain should be editable
            domain_input = ptp_config_page.page.locator(
                f"input[name='domain_number_{port}']"
            )
            if domain_input.is_visible():
                assert not domain_input.get_attribute(
                    "readonly"
                ), f"domain_number should be editable for G.8265.1 on {port}"

            # Test frequency-specific timing configuration
            announce_input = ptp_config_page.page.locator(
                f"input[name='log_announce_interval_{port}']"
            )
            if announce_input.is_visible():
                assert not announce_input.get_attribute(
                    "readonly"
                ), f"log_announce_interval should be editable for G.8265.1 on {port}"

        # Test G.8275 profiles (time/phase synchronization)
        elif "G.8275" in profile:
            # G.8275 profiles: domain should be editable
            domain_input = ptp_config_page.page.locator(
                f"input[name='domain_number_{port}']"
            )
            if domain_input.is_visible():
                assert not domain_input.get_attribute(
                    "readonly"
                ), f"domain_number should be editable for {profile} on {port}"

            # G.8275 profiles: dataset comparison should be enabled
            dataset_select = ptp_config_page.page.locator(
                f"select[name='dataset_comparison_{port}']"
            )
            if dataset_select.count() > 0 and dataset_select.is_visible():
                assert (
                    dataset_select.is_enabled()
                ), f"Dataset comparison should be enabled for {profile} on {port}"

            # G.8275 profiles: priority fields should be editable
            priority1_input = ptp_config_page.page.locator(
                f"input[name='priority_1_{port}']"
            )
            if priority1_input.is_visible():
                assert not priority1_input.get_attribute(
                    "readonly"
                ), f"priority_1 should be editable for {profile} on {port}"

            priority2_input = ptp_config_page.page.locator(
                f"input[name='priority_2_{port}']"
            )
            if priority2_input.is_visible():
                assert not priority2_input.get_attribute(
                    "readonly"
                ), f"priority_2 should be editable for {profile} on {port}"

            # G.8275 profiles: timing intervals should be editable for synchronization
            sync_input = ptp_config_page.page.locator(
                f"input[name='log_sync_interval_{port}']"
            )
            if sync_input.is_visible():
                assert not sync_input.get_attribute(
                    "readonly"
                ), f"log_sync_interval should be editable for {profile} on {port}"

            announce_input = ptp_config_page.page.locator(
                f"input[name='log_announce_interval_{port}']"
            )
            if announce_input.is_visible():
                assert not announce_input.get_attribute(
                    "readonly"
                ), f"log_announce_interval should be editable for {profile} on {port}"

            # G.8275.2 (partial timing support): additional fields
            if "G.8275.2" in profile:
                # Test time-specific parameters for partial timing support
                delay_req_input = ptp_config_page.page.locator(
                    f"input[name='log_min_delay_req_interval_{port}']"
                )
                if delay_req_input.is_visible():
                    assert not delay_req_input.get_attribute(
                        "readonly"
                    ), f"log_min_delay_req_interval should be editable for G.8275.2 on {port}"

                # Test local priority for G.8275.2
                local_priority_input = ptp_config_page.page.locator(
                    f"input[name='local_priority_{port}']"
                )
                if (
                    local_priority_input.count() > 0
                    and local_priority_input.is_visible()
                ):
                    assert not local_priority_input.get_attribute(
                        "readonly"
                    ), f"local_priority should be editable for G.8275.2 on {port}"

        # Common telecom profile validations
        # Verify that profile can be saved
        result = ptp_config_page.save_port_configuration(port)
        assert result, f"Should successfully save {profile} configuration for {port}"

        # Verify persistence by checking configuration
        time.sleep(1 * timeout_multiplier)
        page_data = ptp_config_page.get_page_data(port)
        assert (
            page_data.get("profile") == profile
        ), f"Profile should persist as {profile} for {port}"

    logger.info(f"Telecom profile field behavior testing completed for {device_model}")
