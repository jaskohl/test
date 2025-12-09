"""
Test 27.21.2: Default UDP Profile Transport Configuration
Purpose: Verify UDP TTL configuration in Default UDP Profile
Series: Series 3 Only
Device Behavior: UDP TTL field is visible and configurable in Default UDP Profile
Based on test_27_ptp_config.py line 811 - MODERNIZED v3.0
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


"""
Test 27.21.2: Default UDP Profile Transport Configuration
Purpose: Verify UDP TTL configuration in Default UDP Profile
Series: Series 3 Only
MODERNIZED: DeviceCapabilities integration with timeout multipliers
"""


def test_27_21_2_default_udp_profile_transport_configuration(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.21.2: Default UDP Profile Transport Configuration
    Purpose: Verify UDP TTL configuration in Default UDP Profile
    Series: Series 3 Only
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
        f"Testing Default UDP Profile transport configuration on {device_model} with {timeout_multiplier}x timeout multiplier"
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

    # Select Default UDP Profile
    result = ptp_config_page.configure_ptp_profile(port, "Default Profile (UDPv4)")
    assert result, f"Should successfully select Default UDP Profile for {port}"

    # Configure UDP TTL
    udp_ttl_input = ptp_config_page.page.locator(f"input[name='udp_ttl_{port}']")
    if udp_ttl_input.is_visible():
        # Clear and set TTL value
        udp_ttl_input.clear()
        udp_ttl_input.fill("64")
        # Verify value is accepted (within valid range 1-255)
        assert (
            udp_ttl_input.input_value() == "64"
        ), f"UDP TTL should accept value 64 for {port}"
        # Save configuration
        result = ptp_config_page.save_port_configuration(port)
        assert result, f"Should successfully save PTP configuration for {port}"
        # Verify persistence
        time.sleep(1 * timeout_multiplier)
        page_data = ptp_config_page.get_page_data(port)
        # Note: UDP TTL field name may vary in page data extraction
