"""
Test 27.21.1: Default UDP Profile Field Behavior
Purpose: Verify UDP transport auto-selection in Default UDP Profile
Series: Series 3 Only
Device Behavior: Network transport automatically set to UDPv4
Based on test_27_ptp_config.py line 747 - MODERNIZED v3.0
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


"""
Test 27.21.1: Default UDP Profile Field Behavior
Purpose: Verify UDP transport auto-selection in Default UDP Profile
Series: Series 3 Only
Profile Behavior: Network transport automatically set to UDPv4
MODERNIZED: DeviceCapabilities integration with timeout multipliers
"""


def test_27_21_1_default_udp_profile_field_behavior(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.21.1: Default UDP Profile Field Behavior
    Purpose: Verify UDP transport auto-selection in Default UDP Profile
    Series: Series 3 Only
    Profile Behavior: Network transport automatically set to UDPv4
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
        f"Testing Default UDP Profile field behavior on {device_model} with {timeout_multiplier}x timeout multiplier"
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

    # Select Default Profile (UDPv4)
    result = ptp_config_page.configure_ptp_profile(port, "Default Profile (UDPv4)")
    assert result, f"Should successfully select Default UDP Profile for {port}"

    # Verify network transport is automatically set to UDPv4
    transport_select = ptp_config_page.page.locator(
        f"select[name='network_transport_{port}']"
    )
    if transport_select.is_visible():
        selected_value = transport_select.input_value()
        assert (
            selected_value == "UDPv4"
        ), f"Network transport should be UDPv4 in Default UDP Profile for {port}"

    # Verify UDP TTL field is visible and editable
    udp_ttl_input = ptp_config_page.page.locator(f"input[name='udp_ttl_{port}']")
    if udp_ttl_input.is_visible():
        assert not udp_ttl_input.get_attribute(
            "readonly"
        ), f"UDP TTL should be editable in Default UDP Profile for {port}"
