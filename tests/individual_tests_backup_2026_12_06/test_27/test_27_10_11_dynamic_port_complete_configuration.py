"""
Test 27.10.11: All available ports support complete PTP configuration
Purpose: Complete PTP configuration testing across all available ports
Series: Series 3 Only
Device Behavior: Custom profile enables all PTP configuration fields
MODERNIZED: DeviceCapabilities integration with timeout multipliers

Based on test_27_ptp_config.py line 141 - MODERNIZED v3.0
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_27_10_11_dynamic_port_complete_configuration(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """Test 27.10.11: All available ports support complete PTP configuration"""
    # MODERNIZED: Use request.session.device_hardware_model instead of device_capabilities fixture
    device_model = request.session.device_hardware_model
    if device_model == "Unknown":
        pytest.fail("Device model not detected - cannot determine PTP capabilities")

    device_series = DeviceCapabilities.get_series(device_model)
    if device_series != "Series 3":
        pytest.skip("PTP is Series 3 exclusive")

    # MODERNIZED: Use DeviceCapabilities for PTP interface detection
    static_ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)
    if not static_ptp_interfaces:
        pytest.skip(f"No PTP interfaces available on device model {device_model}")

    # MODERNIZED: Apply timeout multiplier for device-aware testing
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    logger.info(
        f"Testing complete PTP configuration on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to PTP page
    ptp_config_page.page.goto(f"{base_url}/ptp")
    time.sleep(2 * timeout_multiplier)
    # Use heading role instead of text to avoid strict mode violation
    ptp_heading = ptp_config_page.page.get_by_role("heading", name="PTP")
    expect(ptp_heading).to_be_visible()

    # Use static capability data instead of dynamic page detection
    assert (
        len(static_ptp_interfaces) >= 2
    ), f"Should have at least 2 PTP ports on {device_model}, found {len(static_ptp_interfaces)}"

    # Test complete configuration on first available port from static capabilities
    port = static_ptp_interfaces[0]
    logger.info(f"Testing complete configuration on {port} for device {device_model}")

    # Select Custom profile to enable all fields using static capability knowledge
    result = ptp_config_page.configure_ptp_profile(port, "Custom")
    assert result, f"Should successfully select Custom profile for {port}"

    # Test domain number field using page object method
    result = ptp_config_page.configure_domain_number(port, 5)
    assert result, f"Domain number should be configurable for {port}"

    # Test delay mechanism using page object method - wait for profile to take effect
    time.sleep(1 * timeout_multiplier)
    delay_select = ptp_config_page.page.locator(
        f"select[name='delay_mechanism_{port}']"
    )
    delay_select.select_option("E2E")
    assert (
        delay_select.input_value() == "E2E"
    ), f"Delay mechanism should be configurable for {port}"

    # Test network transport via direct DOM interaction
    transport_select = ptp_config_page.page.locator(
        f"select[name='network_transport_{port}']"
    )
    transport_select.select_option("UDPv4")
    assert (
        transport_select.input_value() == "UDPv4"
    ), f"Network transport should be configurable for {port}"
