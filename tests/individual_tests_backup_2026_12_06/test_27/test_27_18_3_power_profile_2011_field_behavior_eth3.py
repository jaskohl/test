"""
Test 27.18.3: IEEE C37.238-2011 Power Profile Field Behavior (eth3)
Purpose: Verify all fields editable in Power Profile 2011 (device UI reality)
Series: Series 3 Only
Device Behavior: All PTP fields remain editable in UI - constraints applied server-side
Based on test_27_ptp_config.py line 1230 - MODERNIZED v3.0
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


"""
Test 27.18.3: IEEE C37.238-2011 Power Profile Field Behavior (eth3)

Purpose: Verify all fields editable in Power Profile 2011 (device UI reality)
Series: Series 3 Only
Device Behavior: All PTP fields remain editable in UI - constraints applied server-side
"""


def test_27_18_3_power_profile_2011_field_behavior_eth3(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """Test 27.18.3: IEEE C37.238-2011 Power Profile Field Behavior (eth3)"""
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
    if "eth3" in available_ptp_interfaces:
        port = "eth3"
    elif available_ptp_interfaces:
        port = available_ptp_interfaces[0]  # Use first available port
    else:
        pytest.skip("No available PTP ports on this device")

    # MODERNIZED: Apply timeout multiplier for device-aware testing
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    logger.info(
        f"Testing Power Profile 2011 field behavior on {port} for {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to PTP page
    ptp_config_page.page.goto(f"{base_url}/ptp")
    time.sleep(2 * timeout_multiplier)
    # Use heading role instead of text to avoid strict mode violation
    ptp_heading = ptp_config_page.page.get_by_role("heading", name="PTP")
    expect(ptp_heading).to_be_visible()

    # Select IEEE C37.238-2011 Power Profile
    result = ptp_config_page.configure_ptp_profile(
        port, "IEEE C37.238-2011 (Power Profile)"
    )
    assert result, f"Should successfully select Power Profile 2011 for {port}"

    # Device UI keeps ALL fields editable - constraints applied server-side
    # Verify timing intervals remain editable (matches device behavior)
    announce_input = ptp_config_page.page.locator(
        f"input[name='log_announce_interval_{port}']"
    )
    if announce_input.is_visible():
        assert not announce_input.get_attribute(
            "readonly"
        ), f"log_announce_interval remains editable in UI for Power Profile 2011 ({port})"
    sync_input = ptp_config_page.page.locator(f"input[name='log_sync_interval_{port}']")
    if sync_input.is_visible():
        assert not sync_input.get_attribute(
            "readonly"
        ), f"log_sync_interval remains editable in UI for Power Profile 2011 ({port})"
    delay_req_input = ptp_config_page.page.locator(
        f"input[name='log_min_delay_req_interval_{port}']"
    )
    if delay_req_input.is_visible():
        assert not delay_req_input.get_attribute(
            "readonly"
        ), f"log_min_delay_req_interval remains editable in UI for Power Profile 2011 ({port})"
    # Verify domain number remains editable
    domain_input = ptp_config_page.page.locator(f"input[name='domain_number_{port}']")
    if domain_input.is_visible():
        assert not domain_input.get_attribute(
            "readonly"
        ), f"domain_number should be editable in Power Profile 2011 for {port}"
    # Verify priorities remain editable
    priority1_input = ptp_config_page.page.locator(f"input[name='priority_1_{port}']")
    if priority1_input.is_visible():
        assert not priority1_input.get_attribute(
            "readonly"
        ), f"priority_1 should be editable in Power Profile 2011 for {port}"
