"""
Test 27.18.2: IEEE C37.238-2011 Power Profile Domain Configuration
Purpose: Verify domain number configuration works in Power Profile 2011
Series: Series 3 Only
FIXED: Added rollback logic to restore original PTP configuration
MODERNIZED: DeviceCapabilities integration with timeout multipliers

Based on test_27_ptp_config.py line 337 - MODERNIZED v3.0
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_27_18_2_power_profile_2011_domain_configuration(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.18.2: IEEE C37.238-2011 Power Profile Domain Configuration
    Purpose: Verify domain number configuration works in Power Profile 2011
    Series: Series 3 Only
    FIXED: Added rollback logic to restore original PTP configuration
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
        f"Testing Power Profile 2011 domain configuration on {device_model} with {timeout_multiplier}x timeout multiplier"
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

    # Get original configuration for rollback
    original_data = ptp_config_page.get_page_data(port)
    try:
        # Select Power Profile 2011
        result = ptp_config_page.configure_ptp_profile(
            port, "IEEE C37.238-2011 (Power Profile)"
        )
        assert result, f"Should successfully select Power Profile 2011 for {port}"
        # Configure domain number
        result = ptp_config_page.configure_domain_number(port, 100)
        assert result, f"Should successfully configure domain number for {port}"
        # Save configuration
        result = ptp_config_page.save_port_configuration(port)
        assert result, f"Should successfully save PTP configuration for {port}"
        # Verify persistence by reloading page and checking data
        time.sleep(1 * timeout_multiplier)
        page_data = ptp_config_page.get_page_data(port, reload_page=True)
        assert (
            page_data.get("domain_number") == "100"
        ), f"Domain number should persist after save for {port}"
    finally:
        # Rollback: Restore original PTP configuration
        if original_data.get("profile"):
            ptp_config_page.configure_ptp_profile(port, original_data["profile"])
        if original_data.get("domain_number"):
            ptp_config_page.configure_domain_number(
                port, int(original_data["domain_number"])
            )
        if original_data.get("priority_1") and original_data.get("priority_2"):
            ptp_config_page.configure_priorities(
                port,
                int(original_data["priority_1"]),
                int(original_data["priority_2"]),
            )
        ptp_config_page.save_port_configuration(port)
        time.sleep(1 * timeout_multiplier)
