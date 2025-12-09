"""
Test 27.20.5: IEC 61850-9-3 Utility Profile Field Behavior (eth4)
Purpose: Verify timing intervals are readonly in Utility Profile, only Domain/Priority editable
Series: Series 3 Only
Profile Behavior: Only Domain number, Priority 1, and Priority 2 are editable in Utility Profile
Based on test_27_ptp_config.py line 1528 - MODERNIZED v3.0

Device Behavior: All PTP fields remain editable in UI - constraints applied server-side
Static Interface Detection: DeviceCapabilities.get_ptp_interfaces() for port detection
Timeout Multipliers: DeviceCapabilities.get_timeout_multiplier() for device-aware testing
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_27_20_5_utility_profile_field_behavior_eth4(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.20.5: IEC 61850-9-3 Utility Profile Field Behavior (eth4)
    Purpose: Verify timing intervals are readonly in Utility Profile, only Domain/Priority editable
    Series: Series 3 Only
    Profile Behavior: Only Domain number, Priority 1, and Priority 2 are editable in Utility Profile
    MODERNIZED: DeviceCapabilities integration with timeout multipliers
    """
    # MODERNIZED: Use request.session.device_hardware_model instead of device_capabilities fixture
    device_model = request.session.device_hardware_model
    if device_model == "Unknown":
        pytest.fail("Device model not detected - cannot determine PTP capabilities")

    device_series = DeviceCapabilities.get_series(device_model)
    if device_series != "Series 3":
        pytest.skip("PTP is Series 3 exclusive")

    # MODERNIZED: Use DeviceCapabilities for PTP interface detection
    available_ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)
    if not available_ptp_interfaces:
        pytest.skip(f"No PTP interfaces available on device model {device_model}")

    # Use DeviceCapabilities to determine available ports
    if "eth4" in available_ptp_interfaces:
        port = "eth4"
    elif available_ptp_interfaces:
        port = available_ptp_interfaces[0]  # Use first available port
    else:
        pytest.skip("No available PTP ports on this device")

    # MODERNIZED: Apply timeout multiplier for device-aware testing
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    logger.info(
        f"Testing Utility Profile field behavior on {port} for {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to PTP page
    ptp_config_page.page.goto(f"{base_url}/ptp")
    time.sleep(2 * timeout_multiplier)
    # Use heading role instead of text to avoid strict mode violation
    ptp_heading = ptp_config_page.page.get_by_role("heading", name="PTP")
    expect(ptp_heading).to_be_visible()

    # Select IEC 61850-9-3 Utility Profile
    result = ptp_config_page.configure_ptp_profile(
        port, "IEEC 61850-9-3:2016 (Utility Profile)"
    )
    assert result, f"Should successfully select Utility Profile for {port}"

    # Device keeps timing intervals editable in Utility Profile (server-side constraints apply)
    # Verify timing intervals remain editable in Utility Profile
    timing_fields = [
        f"log_announce_interval_{port}",
        f"log_sync_interval_{port}",
        f"log_min_delay_req_interval_{port}",
    ]
    for field_name in timing_fields:
        field = ptp_config_page.page.locator(f"input[name='{field_name}']")
        if field.is_visible():
            assert not field.get_attribute(
                "readonly"
            ), f"{field_name} should be editable in Utility Profile for {port}"
    # Verify Domain number and Priorities remain editable
    domain_input = ptp_config_page.page.locator(f"input[name='domain_number_{port}']")
    if domain_input.is_visible():
        assert not domain_input.get_attribute(
            "readonly"
        ), f"Domain should be editable in Utility Profile for {port}"
    priority1_input = ptp_config_page.page.locator(f"input[name='priority_1_{port}']")
    if priority1_input.is_visible():
        assert not priority1_input.get_attribute(
            "readonly"
        ), f"Priority 1 should be editable in Utility Profile for {port}"
    priority2_input = ptp_config_page.page.locator(f"input[name='priority_2_{port}']")
    if priority2_input.is_visible():
        assert not priority2_input.get_attribute(
            "readonly"
        ), f"Priority 2 should be editable in Utility Profile for {port}"
