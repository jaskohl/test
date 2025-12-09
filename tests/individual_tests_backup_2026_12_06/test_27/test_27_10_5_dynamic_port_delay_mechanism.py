"""
PTP Configuration Test Suite - Individual Test
Test 27.10.5: Dynamic Port Delay Mechanism
Test Count: 1 test
Hardware: Device Only
Priority: HIGH
Series: Series 3 Only (PTP exclusive)
Based on COMPLETE_TEST_LIST.md Section 27.10.5
Modernized with DeviceCapabilities integration following established patterns.
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_27_10_5_dynamic_port_delay_mechanism(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """Test 27.10.5: All available ports support delay mechanism selection"""
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
        f"Testing PTP delay mechanism on {device_model} with {timeout_multiplier}x timeout multiplier"
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
    ), f"Should have at least 2 PTP ports on {device_model}, found {len(static_ptp_interfaces)}: {static_ptp_interfaces}"

    # Test delay mechanism on each available port from static capabilities
    for port in static_ptp_interfaces:
        logger.info(f"Testing delay mechanism on {port} for device {device_model}")
        # CRITICAL: Select Custom profile first to enable delay mechanism
        result = ptp_config_page.configure_ptp_profile(port, "Custom")
        assert result, f"Should successfully select Custom profile for {port}"
        # Test delay mechanism is now enabled using page object
        delay_select = ptp_config_page.page.locator(
            f"select[name='delay_mechanism_{port}']"
        )
        expect(delay_select).to_be_visible()
        expect(delay_select).to_be_enabled()
        # Test both options are available
        options = delay_select.locator("option").all_text_contents()
        assert "P2P" in options, f"P2P option should be available for {port}"
        assert "E2E" in options, f"E2E option should be available for {port}"
