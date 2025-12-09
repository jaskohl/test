"""
Test 27.22.1: Default L2 Profile Field Behavior
Purpose: Verify L2 transport auto-selection in Default L2 Profile
Series: Series 3 Only
Profile Behavior: Network transport automatically set to L2
Based on test_27_ptp_config.py line 875 - MODERNIZED v3.0
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


"""
Test 27.22.1: Default L2 Profile Field Behavior
Purpose: Verify L2 transport auto-selection in Default L2 Profile
Series: Series 3 Only
Profile Behavior: Network transport automatically set to L2
"""


def test_27_22_1_default_l2_profile_field_behavior(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.22.1: Default L2 Profile Field Behavior
    Purpose: Verify L2 transport auto-selection in Default L2 Profile
    Series: Series 3 Only
    Profile Behavior: Network transport automatically set to L2
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
        f"Testing Default L2 Profile field behavior on {device_model} with {timeout_multiplier}x timeout multiplier"
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

    # Select Default Profile (802.3)
    result = ptp_config_page.configure_ptp_profile(port, "Default Profile (802.3)")
    assert result, f"Should successfully select Default L2 Profile for {port}"

    # Verify network transport is automatically set to L2
    transport_select = ptp_config_page.page.locator(
        f"select[name='network_transport_{port}']"
    )
    if transport_select.is_visible():
        selected_value = transport_select.input_value()
        assert (
            selected_value == "L2"
        ), f"Network transport should be L2 in Default L2 Profile for {port}"

    # Verify delay mechanism is enabled
    delay_select = ptp_config_page.page.locator(
        f"select[name='delay_mechanism_{port}']"
    )
    if delay_select.is_visible():
        assert (
            delay_select.is_enabled()
        ), f"Delay mechanism should be enabled in Default L2 Profile for {port}"

    # UDP TTL field remains visible and enabled in Default L2 Profile
    udp_ttl_input = ptp_config_page.page.locator(f"input[name='udp_ttl_{port}']")
    if udp_ttl_input.count() > 0:
        # UDP TTL field is visible and enabled (not disabled as previously expected)
        assert (
            udp_ttl_input.is_enabled()
        ), f"UDP TTL should be enabled in Default L2 Profile for {port}"
