"""
Test 27.22.2: Default L2 Profile Delay Mechanism
Purpose: Verify delay mechanism configuration in Default L2 Profile
Series: Series 3 Only
Based on test_27_ptp_config.py line 949 - MODERNIZED v3.0
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


"""
Test 27.22.2: Default L2 Profile Delay Mechanism
Purpose: Verify delay mechanism configuration in Default L2 Profile
Series: Series 3 Only
"""


def test_27_22_2_default_l2_profile_delay_mechanism(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.22.2: Default L2 Profile Delay Mechanism
    Purpose: Verify delay mechanism configuration in Default L2 Profile
    Series: Series 3 Only
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
        f"Testing Default L2 Profile delay mechanism on {device_model} with {timeout_multiplier}x timeout multiplier"
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

    # Select Default L2 Profile
    result = ptp_config_page.configure_ptp_profile(port, "Default Profile (802.3)")
    assert result, f"Should successfully select Default L2 Profile for {port}"

    # Configure delay mechanism to P2P
    delay_select = ptp_config_page.page.locator(
        f"select[name='delay_mechanism_{port}']"
    )
    if delay_select.is_visible():
        delay_select.select_option("P2P")
        assert (
            delay_select.input_value() == "P2P"
        ), f"Delay mechanism should be set to P2P for {port}"
        # Save configuration
        result = ptp_config_page.save_port_configuration(port)
        assert result, f"Should successfully save PTP configuration for {port}"
        # Verify persistence
        page_data = ptp_config_page.get_page_data(port)
        assert (
            page_data.get("delay_mechanism") == "P2P"
        ), f"Delay mechanism should persist for {port}"
