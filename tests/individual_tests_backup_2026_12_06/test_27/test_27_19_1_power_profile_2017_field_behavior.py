"""
Test 27.19.1: IEEE C37.238-2017 Power Profile Field Behavior
Purpose: Verify all fields editable in Power Profile 2017 (device UI reality)
Series: Series 3 Only
Device Behavior: All PTP fields remain editable in UI - constraints applied server-side
MODERNIZED: DeviceCapabilities integration with timeout multipliers

Based on test_27_ptp_config.py line 417 - MODERNIZED v3.0
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_27_19_1_power_profile_2017_field_behavior(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.19.1: IEEE C37.238-2017 Power Profile Field Behavior
    Purpose: Verify all fields editable in Power Profile 2017 (device UI reality)
    Series: Series 3 Only
    Device Behavior: All PTP fields remain editable in UI - constraints applied server-side
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
        f"Testing Power Profile 2017 field behavior on {device_model} with {timeout_multiplier}x timeout multiplier"
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

    # Select IEEE C37.238-2017 Power Profile
    result = ptp_config_page.configure_ptp_profile(
        port, "IEEE C37.238-2017 (Power Profile)"
    )
    assert result, f"Should successfully select Power Profile 2017 for {port}"

    # Device UI keeps ALL fields editable - constraints applied server-side
    # Verify all timing intervals remain editable (matches device behavior)
    timing_fields = [
        f"log_announce_interval_{port}",
        f"log_sync_interval_{port}",
        f"log_min_delay_req_interval_{port}",
        f"announce_receipt_timeout_{port}",
    ]
    for field_name in timing_fields:
        field = ptp_config_page.page.locator(f"input[name='{field_name}']")
        if field.is_visible():
            assert not field.get_attribute(
                "readonly"
            ), f"{field_name} remains editable in UI for Power Profile 2017 ({port})"
    # Verify priorities and domain remain editable
    priority1_input = ptp_config_page.page.locator(f"input[name='priority_1_{port}']")
    if priority1_input.is_visible():
        assert not priority1_input.get_attribute(
            "readonly"
        ), f"priority_1 should be editable in Power Profile 2017 for {port}"
    domain_input = ptp_config_page.page.locator(f"input[name='domain_number_{port}']")
    if domain_input.is_visible():
        assert not domain_input.get_attribute(
            "readonly"
        ), f"domain_number should be editable in Power Profile 2017 for {port}"
